#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
main program for Bokeh server
Created on Sun Apr 21 2017
@author: Dan Cutright, PhD
"""


from __future__ import print_function
from future.utils import listitems
from analysis_tools import DVH, get_study_instance_uids, calc_eud
from utilities import Temp_DICOM_FileSet, get_planes_from_string, get_union
import auth
from sql_connector import DVH_SQL
from sql_to_python import QuerySQL
import numpy as np
import itertools
from datetime import datetime
from os.path import dirname, join
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Legend, CustomJS, HoverTool, Slider, Spacer
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.palettes import Colorblind8 as palette
from bokeh.models.widgets import Select, Button, Div, TableColumn, DataTable, Panel, Tabs, NumberFormatter,\
    RadioButtonGroup, TextInput, RadioGroup, CheckboxButtonGroup, Dropdown, CheckboxGroup, PasswordInput
from dicompylercore import dicomparser, dvhcalc
from bokeh import events
from scipy.stats import ttest_ind, ranksums, normaltest, pearsonr, linregress
from math import pi
import statsmodels.api as sm
import matplotlib.colors as plot_colors
import time
from options import *

# This depends on a user defined function in dvh/auth.py.  By default, this returns True
# It is up to the user/installer to write their own function (e.g., using python-ldap)
# Proper execution of this requires placing Bokeh behind a reverse proxy with SSL setup (HTTPS)
# Please see Bokeh documentation for more information
ACCESS_GRANTED = not AUTH_USER_REQ

SELECT_CATEGORY1_DEFAULT = 'ROI Institutional Category'
SELECT_CATEGORY_DEFAULT = 'Rx Dose'

# Used to keep Query UI clean
ALLOW_SOURCE_UPDATE = True

# This depends on a user defined function in dvh/auth.py.  By default, this returns True
# It is up to the user/installer to write their own function (e.g., using python-ldap)
# Proper execution of this requires placing Bokeh behind a reverse proxy with SSL setup (HTTPS)
# Please see Bokeh documentation for more information
ACCESS_GRANTED = not AUTH_USER_REQ


# Declare variables
colors = itertools.cycle(palette)
current_dvh, current_dvh_group_1, current_dvh_group_2 = [], [], []
anon_id_map = {}
uids_1, uids_2 = [], []

temp_dvh_info = Temp_DICOM_FileSet()
dvh_review_mrns = temp_dvh_info.mrn
if dvh_review_mrns[0] != '':
    dvh_review_rois = temp_dvh_info.get_roi_names(dvh_review_mrns[0]).values()
    dvh_review_mrns.append('')
else:
    dvh_review_rois = ['']


# Bokeh column data sources
source = ColumnDataSource(data=dict(color=[], x=[], y=[], mrn=[],
                                    ep1=[], ep2=[], ep3=[], ep4=[], ep5=[], ep6=[], ep7=[], ep8=[]))
source_selectors = ColumnDataSource(data=dict(row=[1], category1=[''], category2=[''],
                                              group=[''], group_label=[''], not_status=['']))
source_ranges = ColumnDataSource(data=dict(row=[], category=[], min=[], max=[], min_display=[], max_display=[],
                                           group=[], group_label=[], not_status=[]))
source_endpoint_defs = ColumnDataSource(data=dict(row=[], output_type=[], input_type=[], input_value=[],
                                                  label=[], units_in=[], units_out=[]))
source_beams = ColumnDataSource(data=dict())
source_plans = ColumnDataSource(data=dict())
source_rxs = ColumnDataSource(data=dict())


# Categories map of dropdown values, SQL column, and SQL table (and data source for range_categories)
selector_categories = {'ROI Institutional Category': {'var_name': 'institutional_roi', 'table': 'DVHs'},
                       'ROI Physician Category': {'var_name': 'physician_roi', 'table': 'DVHs'},
                       'ROI Type': {'var_name': 'roi_type', 'table': 'DVHs'},
                       'Beam Type': {'var_name': 'beam_type', 'table': 'Beams'},
                       'Dose Grid Resolution': {'var_name': 'dose_grid_res', 'table': 'Plans'},
                       'Gantry Rotation Direction': {'var_name': 'gantry_rot_dir', 'table': 'Beams'},
                       'Radiation Type': {'var_name': 'radiation_type', 'table': 'Beams'},
                       'Patient Orientation': {'var_name': 'patient_orientation', 'table': 'Plans'},
                       'Patient Sex': {'var_name': 'patient_sex', 'table': 'Plans'},
                       'Physician': {'var_name': 'physician', 'table': 'Plans'},
                       'Tx Modality': {'var_name': 'tx_modality', 'table': 'Plans'},
                       'Tx Site': {'var_name': 'tx_site', 'table': 'Plans'},
                       'Normalization': {'var_name': 'normalization_method', 'table': 'Rxs'},
                       'Treatment Machine': {'var_name': 'treatment_machine', 'table': 'Beams'},
                       'Heterogeneity Correction': {'var_name': 'heterogeneity_correction', 'table': 'Plans'},
                       'Scan Mode': {'var_name': 'scan_mode', 'table': 'Beams'},
                       'MRN': {'var_name': 'mrn', 'table': 'Plans'},
                       'UID': {'var_name': 'study_instance_uid', 'table': 'Plans'},
                       'Baseline': {'var_name': 'baseline', 'table': 'Plans'}}
range_categories = {'Age': {'var_name': 'age', 'table': 'Plans', 'units': '', 'source': source_plans},
                    'Beam Energy Min': {'var_name': 'beam_energy_min', 'table': 'Beams', 'units': '', 'source': source_beams},
                    'Beam Energy Max': {'var_name': 'beam_energy_max', 'table': 'Beams', 'units': '', 'source': source_beams},
                    'Birth Date': {'var_name': 'birth_date', 'table': 'Plans', 'units': '', 'source': source_plans},
                    'Planned Fractions': {'var_name': 'fxs', 'table': 'Plans', 'units': '', 'source': source_plans},
                    'Rx Dose': {'var_name': 'rx_dose', 'table': 'Plans', 'units': 'Gy', 'source': source_plans},
                    'Rx Isodose': {'var_name': 'rx_percent', 'table': 'Rxs', 'units': '%', 'source': source_rxs},
                    'Simulation Date': {'var_name': 'sim_study_date', 'table': 'Plans', 'units': '', 'source': source_plans},
                    'Total Plan MU': {'var_name': 'total_mu', 'table': 'Plans', 'units': 'MU', 'source': source_plans},
                    'Fraction Dose': {'var_name': 'fx_dose', 'table': 'Rxs', 'units': 'Gy', 'source': source_rxs},
                    'Beam Dose': {'var_name': 'beam_dose', 'table': 'Beams', 'units': 'Gy', 'source': source_beams},
                    'Beam MU': {'var_name': 'beam_mu', 'table': 'Beams', 'units': '', 'source': source_beams},
                    'Control Point Count': {'var_name': 'control_point_count', 'table': 'Beams', 'units': '', 'source': source_beams},
                    'Collimator Start Angle': {'var_name': 'collimator_start', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Collimator End Angle': {'var_name': 'collimator_end', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Collimator Min Angle': {'var_name': 'collimator_min', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Collimator Max Angle': {'var_name': 'collimator_max', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Collimator Range': {'var_name': 'collimator_range', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Couch Start Angle': {'var_name': 'couch_start', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Couch End Angle': {'var_name': 'couch_end', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Couch Min Angle': {'var_name': 'couch_min', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Couch Max Angle': {'var_name': 'couch_max', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Couch Range': {'var_name': 'couch_range', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Gantry Start Angle': {'var_name': 'gantry_start', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Gantry End Angle': {'var_name': 'gantry_end', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Gantry Min Angle': {'var_name': 'gantry_min', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Gantry Max Angle': {'var_name': 'gantry_max', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'Gantry Range': {'var_name': 'gantry_range', 'table': 'Beams', 'units': 'deg', 'source': source_beams},
                    'SSD': {'var_name': 'ssd', 'table': 'Beams', 'units': 'cm', 'source': source_beams},
                    'ROI Min Dose': {'var_name': 'min_dose', 'table': 'DVHs', 'units': 'Gy', 'source': source},
                    'ROI Mean Dose': {'var_name': 'mean_dose', 'table': 'DVHs', 'units': 'Gy', 'source': source},
                    'ROI Max Dose': {'var_name': 'max_dose', 'table': 'DVHs', 'units': 'Gy', 'source': source},
                    'ROI Volume': {'var_name': 'volume', 'table': 'DVHs', 'units': 'cc', 'source': source},
                    'PTV Distance (Min)': {'var_name': 'dist_to_ptv_min', 'table': 'DVHs', 'units': 'cm', 'source': source},
                    'PTV Distance (Mean)': {'var_name': 'dist_to_ptv_mean', 'table': 'DVHs', 'units': 'cm', 'source': source},
                    'PTV Distance (Median)': {'var_name': 'dist_to_ptv_median', 'table': 'DVHs', 'units': 'cm', 'source': source},
                    'PTV Distance (Max)': {'var_name': 'dist_to_ptv_max', 'table': 'DVHs', 'units': 'cm', 'source': source},
                    'PTV Overlap': {'var_name': 'ptv_overlap', 'table': 'DVHs', 'units': 'cc', 'source': source},
                    'Scan Spots': {'var_name': 'scan_spot_count', 'table': 'Beams', 'units': '', 'source': source_beams},
                    'Beam MU per deg': {'var_name': 'beam_mu_per_deg', 'table': 'Beams', 'units': '', 'source': source_beams},
                    'Beam MU per control point': {'var_name': 'beam_mu_per_cp', 'table': 'Beams', 'units': '', 'source': source_beams}}


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Functions for Querying by categorical data
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def update_select_category2_values():
    new = select_category1.value
    table_new = selector_categories[new]['table']
    var_name_new = selector_categories[new]['var_name']
    new_options = DVH_SQL().get_unique_values(table_new, var_name_new)
    select_category2.options = new_options
    select_category2.value = new_options[0]


def ensure_selector_group_is_assigned(attr, old, new):
    if not group_selector.active:
        group_selector.active = [-old[0] + 1]
    update_selector_source()


def update_selector_source():
    if selector_row.value:
        r = int(selector_row.value) - 1
        group = sum([i+1 for i in group_selector.active])
        group_labels = ['1', '2', '1 & 2']
        group_label = group_labels[group-1]
        not_status = ['', 'Not'][len(selector_not_operator_checkbox.active)]

        patch = {'category1': [(r, select_category1.value)], 'category2': [(r, select_category2.value)],
                 'group': [(r, group)], 'group_label': [(r, group_label)], 'not_status': [(r, not_status)]}
        source_selectors.patch(patch)


def add_selector_row():
    if source_selectors.data['row']:
        temp = source_selectors.data

        for key in list(temp):
            temp[key].append('')
        temp['row'][-1] = len(temp['row'])

        source_selectors.data = temp
        new_options = [str(x+1) for x in range(0, len(temp['row']))]
        selector_row.options = new_options
        selector_row.value = new_options[-1]
        select_category1.value = SELECT_CATEGORY1_DEFAULT
        select_category2.value = select_category2.options[0]
        selector_not_operator_checkbox.active = []
    else:
        selector_row.options = ['1']
        selector_row.value = '1'
        source_selectors.data = dict(row=[1], category1=[''], category2=[''],
                                     group=[''], group_label=[''], not_status=[''])
    update_selector_source()

    clear_source_selection(source_selectors)


def select_category1_ticker(attr, old, new):
    update_select_category2_values()
    update_selector_source()


def select_category2_ticker(attr, old, new):
    update_selector_source()


def selector_not_operator_ticker(attr, old, new):
    update_selector_source()


def selector_row_ticker(attr, old, new):
    if source_selectors.data['category1'] and source_selectors.data['category1'][-1]:
        r = int(selector_row.value) - 1
        category1 = source_selectors.data['category1'][r]
        category2 = source_selectors.data['category2'][r]
        group = source_selectors.data['group'][r]
        not_status = source_selectors.data['not_status'][r]

        select_category1.value = category1
        select_category2.value = category2
        group_selector.active = [[0], [1], [0, 1]][group-1]
        if not_status:
            selector_not_operator_checkbox.active = [0]
        else:
            selector_not_operator_checkbox.active = []


def update_selector_row_on_selection(attr, old, new):
    if new['1d']['indices']:
        selector_row.value = selector_row.options[min(new['1d']['indices'])]


def delete_selector_row():
    if selector_row.value:
        new_selectors_source = source_selectors.data
        index_to_delete = int(selector_row.value) - 1
        new_source_length = len(source_selectors.data['category1']) - 1

        if new_source_length == 0:
            source_selectors.data = dict(row=[], category1=[], category2=[], group=[], group_label=[], not_status=[])
            selector_row.options = ['']
            selector_row.value = ''
            group_selector.active = [0]
            selector_not_operator_checkbox.active = []
            select_category1.value = SELECT_CATEGORY1_DEFAULT
            select_category2.value = select_category2.options[0]
        else:
            for key in list(new_selectors_source):
                new_selectors_source[key].pop(index_to_delete)

            for i in range(index_to_delete, new_source_length):
                new_selectors_source['row'][i] -= 1

            selector_row.options = [str(x+1) for x in range(0, new_source_length)]
            if selector_row.value not in selector_row.options:
                selector_row.value = selector_row.options[-1]
            source_selectors.data = new_selectors_source

        clear_source_selection(source_selectors)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Functions for Querying by numerical data
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def add_range_row():
    if source_ranges.data['row']:
        temp = source_ranges.data

        for key in list(temp):
            temp[key].append('')
        temp['row'][-1] = len(temp['row'])
        source_ranges.data = temp
        new_options = [str(x+1) for x in range(0, len(temp['row']))]
        range_row.options = new_options
        range_row.value = new_options[-1]
        select_category.value = SELECT_CATEGORY_DEFAULT
        group_range.active = [0]
        range_not_operator_checkbox.active = []
    else:
        range_row.options = ['1']
        range_row.value = '1'
        source_ranges.data = dict(row=['1'], category=[''], min=[''], max=[''], min_display=[''], max_display=[''],
                                  group=[''], group_label=[''], not_status=[''])

    update_range_titles(reset_values=True)
    update_range_source()

    clear_source_selection(source_ranges)


def update_range_source():
    if range_row.value:
        table = range_categories[select_category.value]['table']
        var_name = range_categories[select_category.value]['var_name']

        r = int(range_row.value) - 1
        group = sum([i+1 for i in group_range.active])
        group_labels = ['1', '2', '1 & 2']
        group_label = group_labels[group-1]
        not_status = ['', 'Not'][len(range_not_operator_checkbox.active)]

        try:
            min_float = float(text_min.value)
        except ValueError:
            try:
                min_float = float(DVH_SQL().get_min_value(table, var_name))
            except TypeError:
                min_float = ''

        try:
            max_float = float(text_max.value)
        except ValueError:
            try:
                max_float = float(DVH_SQL().get_max_value(table, var_name))
            except TypeError:
                max_float = ''

        if min_float or min_float == 0.:
            min_display = "%s %s" % (str(min_float), range_categories[select_category.value]['units'])
        else:
            min_display = 'None'

        if max_float or max_float == 0.:
            max_display = "%s %s" % (str(max_float), range_categories[select_category.value]['units'])
        else:
            max_display = 'None'

        patch = {'category': [(r, select_category.value)], 'min': [(r, min_float)], 'max': [(r, max_float)],
                 'min_display': [(r, min_display)], 'max_display': [(r, max_display)],
                 'group': [(r, group)], 'group_label': [(r, group_label)], 'not_status': [(r, not_status)]}
        source_ranges.patch(patch)

        group_range.active = [[0], [1], [0, 1]][group - 1]
        text_min.value = str(min_float)
        text_max.value = str(max_float)


def update_range_titles(**kwargs):
    table = range_categories[select_category.value]['table']
    var_name = range_categories[select_category.value]['var_name']
    min_value = DVH_SQL().get_min_value(table, var_name)
    text_min.title = 'Min: ' + str(min_value) + ' ' + range_categories[select_category.value]['units']
    max_value = DVH_SQL().get_max_value(table, var_name)
    text_max.title = 'Max: ' + str(max_value) + ' ' + range_categories[select_category.value]['units']

    if kwargs and 'reset_values' in kwargs and kwargs['reset_values']:
        text_min.value = str(min_value)
        text_max.value = str(max_value)


def range_row_ticker(attr, old, new):
    global ALLOW_SOURCE_UPDATE
    if source_ranges.data['category'] and source_ranges.data['category'][-1]:
        r = int(new) - 1
        category = source_ranges.data['category'][r]
        min_new = source_ranges.data['min'][r]
        max_new = source_ranges.data['max'][r]
        group = source_ranges.data['group'][r]
        not_status = source_ranges.data['not_status'][r]

        ALLOW_SOURCE_UPDATE = False
        select_category.value = category
        text_min.value = str(min_new)
        text_max.value = str(max_new)
        update_range_titles()
        group_range.active = [[0], [1], [0, 1]][group - 1]
        ALLOW_SOURCE_UPDATE = True
        if not_status:
            range_not_operator_checkbox.active = [0]
        else:
            range_not_operator_checkbox.active = []


def select_category_ticker(attr, old, new):
    if ALLOW_SOURCE_UPDATE:
        update_range_titles(reset_values=True)
        update_range_source()


def min_text_ticker(attr, old, new):
    if ALLOW_SOURCE_UPDATE:
        update_range_source()


def max_text_ticker(attr, old, new):
    if ALLOW_SOURCE_UPDATE:
        update_range_source()


def range_not_operator_ticker(attr, old, new):
    if ALLOW_SOURCE_UPDATE:
        update_range_source()


def delete_range_row():
    if range_row.value:
        new_range_source = source_ranges.data
        index_to_delete = int(range_row.value) - 1
        new_source_length = len(source_ranges.data['category']) - 1

        if new_source_length == 0:
            source_ranges.data = dict(row=[], category=[], min=[], max=[], min_display=[], max_display=[],
                                      group=[], group_label=[], not_status=[])
            range_row.options = ['']
            range_row.value = ''
            group_range.active = [0]
            range_not_operator_checkbox.active = []
            select_category.value = SELECT_CATEGORY_DEFAULT
            text_min.value = ''
            text_max.value = ''
        else:
            for key in list(new_range_source):
                new_range_source[key].pop(index_to_delete)

            for i in range(index_to_delete, new_source_length):
                new_range_source['row'][i] -= 1

            range_row.options = [str(x+1) for x in range(0, new_source_length)]
            if range_row.value not in range_row.options:
                range_row.value = range_row.options[-1]
            source_ranges.data = new_range_source

        clear_source_selection(source_ranges)


def ensure_range_group_is_assigned(attrname, old, new):
    if not group_range.active:
        group_range.active = [-old[0] + 1]
    update_range_source()


def update_range_row_on_selection(attr, old, new):
    if new['1d']['indices']:
        range_row.value = range_row.options[min(new['1d']['indices'])]


def clear_source_selection(src):
    src.selected = {'0d': {'glyph': None, 'indices': []},
                    '1d': {'indices': []},
                    '2d': {'indices': {}}}


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Functions for adding DVH endpoints
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def add_endpoint():
    if source_endpoint_defs.data['row']:
        temp = source_endpoint_defs.data

        for key in list(temp):
            temp[key].append('')
        temp['row'][-1] = len(temp['row'])
        source_endpoint_defs.data = temp
        new_options = [str(x+1) for x in range(0, len(temp['row']))]
        ep_row.options = new_options
        ep_row.value = new_options[-1]
    else:
        ep_row.options = ['1']
        ep_row.value = '1'
        source_endpoint_defs.data = dict(row=['1'], output_type=[''], input_type=[''], input_value=[''],
                                         label=[''], units_in=[''], units_out=[''])

    update_ep_source()

    clear_source_selection(source_endpoint_defs)


def update_ep_source():
    if ep_row.value:

        r = int(ep_row.value) - 1

        if 'Dose' in select_ep_type.value:
            input_type, output_type = 'Dose', 'Volume'
            if '%' in select_ep_type.value:
                units_out = '%'
            else:
                units_out = 'Gy'
            units_in = ['cc', '%'][ep_units_in.active]
            label = "D_%s%s" % (ep_text_input.value, units_in)
        else:
            input_type, output_type = 'Volume', 'Dose'
            if '%' in select_ep_type.value:
                units_out = '%'
            else:
                units_out = 'cc'
            units_in = ['Gy', '%'][ep_units_in.active]
            label = "V_%s%s" % (ep_text_input.value, units_in)

        patch = {'output_type': [(r, output_type)], 'input_type': [(r, input_type)],
                 'input_value': [(r, ep_text_input.value)], 'label': [(r, label)],
                 'units_in': [(r, units_in)], 'units_out': [(r, units_out)]}
        source_endpoint_defs.patch(patch)


def ep_units_in_ticker(attr, old, new):
    update_ep_text_input_title()
    update_ep_source()


def update_ep_text_input_title():
    if 'Dose' in select_ep_type.value:
        ep_text_input.title = "Input Volume (%s):" % ['cc', '%'][ep_units_in.active]
    else:
        ep_text_input.title = "Input Dose (%s):" % ['cc', 'Gy'][ep_units_in.active]


def select_ep_type_ticker(attr, old, new):
    if 'Dose' in new:
        ep_units_in.labels = ['cc', '%']
    else:
        ep_units_in.labels = ['Gy', '%']

    update_ep_text_input_title()
    update_ep_source()


def ep_text_input_ticker(attr, old, new):
    update_ep_source()


def delete_ep_row():
    if ep_row.value:
        new_ep_source = source_endpoint_defs.data
        index_to_delete = int(ep_row.value) - 1
        new_source_length = len(source_endpoint_defs.data['output_type']) - 1

        if new_source_length == 0:
            source_endpoint_defs.data = dict(row=[], output_type=[], input_type=[], input_value=[],
                                             label=[], units_in=[], units_out=[])
            ep_row.options = ['']
            ep_row.value = ''
        else:
            for key in list(new_ep_source):
                new_ep_source[key].pop(index_to_delete)

            for i in range(index_to_delete, new_source_length):
                new_ep_source['row'][i] -= 1

            ep_row.options = [str(x+1) for x in range(0, new_source_length)]
            if ep_row.value not in ep_row.options:
                ep_row.value = ep_row.options[-1]
            source_endpoint_defs.data = new_ep_source

        clear_source_selection(source_endpoint_defs)


def update_ep_row_on_selection(attr, old, new):
    if new['1d']['indices']:
        ep_row.value = ep_row.options[min(new['1d']['indices'])]


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Query functions
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!

# This function retuns the list of information needed to execute QuerySQL from
# SQL_to_Python.py (i.e., uids and dvh_condition
# This function can be used for one group at a time, or both groups. Using both groups is useful so that duplicate
# DVHs do not show up in the plot (i.e., if a DVH satisfies both group criteria
def get_query(**kwargs):

    if kwargs and 'group' in kwargs:
        if kwargs['group'] == 1:
            active_groups = ['1']
        elif kwargs['group'] == 2:
            active_groups = ['2']
    else:
        active_groups = ['1', '2']

    # Use to accumulate lists of query strings for each table
    # Will assume each item in list is complete query for that SQL column
    queries = {'plan': [], 'rx': [], 'beam': [], 'dvh': []}

    for active_group in active_groups:

        # Used to group queries by variable, will combine all queries of same variable with an OR operator
        # e.g., queries_by_sql_column['plan'][key] = list of strings, where key is sql column
        queries_by_sql_column = {'Plans': {}, 'Rxs': {}, 'Beams': {}, 'DVHs': {}}

        # Accumulate categorical query strings
        # source_selectors = ColumnDataSource(data=dict(row=[1], category1=[''], category2=[''],
        #                                               group=[''], group_label=[''], not_status=['']))
        data = source_selectors.data
        for r in data['row']:
            if active_group in data['group']:
                var_name = selector_categories[data['category1'][r-1]]['var_name']
                table = selector_categories[data['category1'][r-1]]['table']
                value = selector_categories[data['category2'][r-1]]['var_name']
                if data['not_status'][r-1] == 'Not':
                    operator = "!="
                else:
                    operator = "="

                query_str = "%s %s '%s'" % (var_name, operator, value)

                # Append query_str in query_by_sql_column
                if var_name not in queries_by_sql_column[table]:
                    queries_by_sql_column[table][var_name] = []
                queries_by_sql_column[table][var_name].append(query_str)

        # Accumulate numerical query strings
        # dict(row=[], category=[], min=[], max=[], min_display=[], max_display=[],
        # group=[], group_label=[], not_status=[])
        data = source_ranges.data
        for r in data['row']:
            if active_group in data['group']:
                var_name = range_categories[data['category'][r-1]]['var_name']
                table = range_categories[data['category'][r-1]]['table']

                if data['min'] != '':
                    value_low = data['min']
                else:
                    value_low = query_row[i].min_value
                if query_row[i].text_max.value != '':
                    value_high = query_row[i].text_max.value
                else:
                    value_high = query_row[i].max_value
                if var_name in {'sim_study_date', 'birth_date'}:
                    value_low = "'" + value_low + "'::date"
                    value_high = "'" + value_high + "'::date"
                query_str = var_name + " between " + str(value_low) + " and " + str(value_high)

                # Append query_str in query_by_sql_column
                if var_name not in queries_by_sql_column[table]:
                    queries_by_sql_column[table][var_name] = []
                queries_by_sql_column[table][var_name].append(query_str)


    print(str(datetime.now()), 'getting uids', sep=' ')
    print(str(datetime.now()), 'Plans =', plan_query, sep=' ')
    print(str(datetime.now()), 'Rxs =', rx_query, sep=' ')
    print(str(datetime.now()), 'Beams =', beam_query, sep=' ')

    # Get a list of UIDs that fit the plan, rx, and beam query criteria.  DVH query criteria will not alter the
    # list of UIDs, therefore dvh_query is not needed to get teh UID list
    uids = get_study_instance_uids(Plans=plan_query, Rxs=rx_query, Beams=beam_query)['union']

    # uids: a unique list of all uids that satisfy the criteria
    # dvh_query: the dvh query string for SQL
    return uids, dvh_query


def combine_query_or(query):
    if query[0] and query[1]:
        query = '(' + ') or ('.join(query) + ')'
    elif query[0]:
        query = query[0]
    elif query[1]:
        query = query[1]
    else:
        query = []
    return query


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Selection Filter UI objects
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!
category_options = list(selector_categories)
category_options.sort()

div_selector = Div(text="<b>Query by Categorical Data</b>", width=1000)
div_selector_end = Div(text="<hr>", width=1050)

# Add Current row to source
add_selector_row_button = Button(label="Add Selection Filter", button_type="primary", width=200)
add_selector_row_button.on_click(add_selector_row)

# Row
selector_row = Select(value='1', options=['1'], width=50, title="Row")
selector_row.on_change('value', selector_row_ticker)

# Category 1
select_category1 = Select(value="ROI Institutional Category", options=category_options, width=300, title="Category 1")
select_category1.on_change('value', select_category1_ticker)

# Category 2
cat_2_sql_table = selector_categories[select_category1.value]['table']
cat_2_var_name = selector_categories[select_category1.value]['var_name']
category2_values = DVH_SQL().get_unique_values(cat_2_sql_table, cat_2_var_name)
select_category2 = Select(value=category2_values[0], options=category2_values, width=300, title="Category 2")
select_category2.on_change('value', select_category2_ticker)

# Misc
delete_selector_row_button = Button(label="Delete", button_type="warning", width=100)
delete_selector_row_button.on_click(delete_selector_row)
group_selector = CheckboxButtonGroup(labels=["Group 1", "Group 2"], active=[0], width=180)
group_selector.on_change('active', ensure_selector_group_is_assigned)
selector_not_operator_checkbox = CheckboxGroup(labels=['Not'], active=[])
selector_not_operator_checkbox.on_change('active', selector_not_operator_ticker)

# Selector Category table
columns = [TableColumn(field="row", title="Row", width=60),
           TableColumn(field="category1", title="Selection Category 1", width=280),
           TableColumn(field="category2", title="Selection Category 2", width=280),
           TableColumn(field="group_label", title="Group", width=170),
           TableColumn(field="not_status", title="Apply Not Operator", width=150)]
selection_filter_data_table = DataTable(source=source_selectors,
                                        columns=columns, width=1000, height=150, row_headers=False)
source_selectors.on_change('selected', update_selector_row_on_selection)
update_selector_source()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Range Filter UI objects
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!
category_options = list(range_categories)
category_options.sort()

div_range = Div(text="<b>Query by Numerical Data</b>", width=1000)
div_range_end = Div(text="<hr>", width=1050)

# Add Current row to source
add_range_row_button = Button(label="Add Range Filter", button_type="primary", width=200)
add_range_row_button.on_click(add_range_row)

# Row
range_row = Select(value='', options=[''], width=50, title="Row")
range_row.on_change('value', range_row_ticker)

# Category
select_category = Select(value=SELECT_CATEGORY_DEFAULT, options=category_options, width=240, title="Category")
select_category.on_change('value', select_category_ticker)

# Min and max
text_min = TextInput(value='', title='Min: ', width=180)
text_min.on_change('value', min_text_ticker)
text_max = TextInput(value='', title='Max: ', width=180)
text_max.on_change('value', max_text_ticker)

# Misc
delete_range_row_button = Button(label="Delete", button_type="warning", width=100)
delete_range_row_button.on_click(delete_range_row)
group_range = CheckboxButtonGroup(labels=["Group 1", "Group 2"], active=[0], width=180)
group_range.on_change('active', ensure_range_group_is_assigned)
range_not_operator_checkbox = CheckboxGroup(labels=['Not'], active=[])
range_not_operator_checkbox.on_change('active', range_not_operator_ticker)

# Selector Category table
columns = [TableColumn(field="row", title="Row", width=60),
           TableColumn(field="category", title="Range Category", width=230),
           TableColumn(field="min_display", title="Min", width=170),
           TableColumn(field="max_display", title="Max", width=170),
           TableColumn(field="group_label", title="Group", width=180),
           TableColumn(field="not_status", title="Apply Not Operator", width=150)]
range_filter_data_table = DataTable(source=source_ranges,
                                    columns=columns, width=1000, height=150, row_headers=False)
source_ranges.on_change('selected', update_range_row_on_selection)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DVH Endpoint Filter UI objects
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
div_endpoint = Div(text="<b>Define Endpoints</b>", width=1000)

# Add Current row to source
add_endpoint_row_button = Button(label="Add Endpoint", button_type="primary", width=200)
add_endpoint_row_button.on_click(add_endpoint)

ep_row = Select(value='', options=[''], width=50, title="Row")
ep_options = ["Dose (Gy)", "Dose (%)", "Volume (cc)", "Volume (%)"]
select_ep_type = Select(value=ep_options[0], options=ep_options, width=180, title="Output")
select_ep_type.on_change('value', select_ep_type_ticker)
ep_text_input = TextInput(value='', title="Input Volume (cc):", width=180)
ep_text_input.on_change('value', ep_text_input_ticker)
ep_units_in = RadioButtonGroup(labels=["cc", "%"], active=0, width=100)
ep_units_in.on_change('active', ep_units_in_ticker)
delete_ep_row_button= Button(label="Delete", button_type="warning", width=100)
delete_ep_row_button.on_click(delete_ep_row)

# endpoint  table
columns = [TableColumn(field="row", title="Row", width=60),
           TableColumn(field="label", title="Endpoint", width=180),
           TableColumn(field="units_out", title="Units", width=60)]
ep_data_table = DataTable(source=source_endpoint_defs, columns=columns, width=300, height=150, row_headers=False)

source_endpoint_defs.on_change('selected', update_ep_row_on_selection)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Layout objects
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!
layout_query = column(div_selector,
                      add_selector_row_button,
                      row(selector_row, Spacer(width=10), select_category1, select_category2, group_selector,
                          delete_selector_row_button, Spacer(width=10), selector_not_operator_checkbox),
                      selection_filter_data_table,
                      div_selector_end,
                      div_range,
                      add_range_row_button,
                      row(range_row, Spacer(width=10), select_category, text_min, text_max, group_range,
                          delete_range_row_button, Spacer(width=10), range_not_operator_checkbox),
                      range_filter_data_table,
                      div_range_end,
                      div_endpoint,
                      add_endpoint_row_button,
                      row(ep_row, Spacer(width=10), select_ep_type, ep_text_input, ep_units_in, delete_ep_row_button),
                      ep_data_table)

curdoc().add_root(layout_query)
curdoc().title = "DVH Analytics"
