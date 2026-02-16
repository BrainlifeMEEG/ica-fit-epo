"""
Compute ICA decomposition on epoched MEG/EEG data.

This app fits an ICA decomposition to epoched MEG/EEG data, with optional filtering.
It saves the ICA object, visualizes components, and generates a comprehensive QC report.

Input:
    - epo: Path to MNE epochs .fif file
    - n_components: Number of ICA components to estimate
    - method: ICA method ('fastica', 'picard', 'infomax', etc.)
    - l_freq/h_freq: Optional bandpass filtering parameters
    - picks_to_plot: Number of components to show detailed plots for

Output:
    - out_dir/ica.fif: ICA decomposition object
    - out_figs/components_topo.png: Topographic plot of ICA components
    - out_figs/component_*.png: Detailed properties for selected components
    - out_report/report_ica.html: QC report with component analysis
    - product.json: Metadata about ICA decomposition
"""

# Copyright (c) 2026 brainlife.io
#
# This app computes ICA decomposition on MNE epoched data
#
# Authors:
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne
from mne.preprocessing import ICA
import matplotlib.pyplot as plt

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    save_figure_with_base64
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# Load configuration
config = load_config()

# == LOAD DATA ==
fname = config['epo']
epo = mne.read_epochs(fname, preload=True)

# == OPTIONAL FILTERING ==
product_items = []

if config.get('l_freq') is not None and config.get('h_freq') is not None:
    epo.filter(l_freq=config['l_freq'], h_freq=config['h_freq'])
    filter_msg = f'Applied bandpass filter: {config["l_freq"]}-{config["h_freq"]} Hz'
    add_info_to_product(product_items, filter_msg)

# == PARSE FIT PARAMETERS ==
fit_params = None
if config.get('fit_params') is not None:
    try:
        fit_params = eval(config['fit_params'])
    except Exception as e:
        print(f'Warning: Could not parse fit_params: {e}')

# == SET UP ICA ==
ica_params = {
    'n_components': int(config.get('n_components', 20)),
    'random_state': config.get('random_state', 42),
    'method': config.get('method', 'fastica'),
}

# Add optional parameters
if config.get('noise_cov') is not None:
    ica_params['noise_cov'] = config['noise_cov']
if fit_params is not None:
    ica_params['fit_params'] = fit_params
if config.get('max_iter') is not None:
    ica_params['max_iter'] = config['max_iter']
if config.get('allow_ref_meg') is not None:
    ica_params['allow_ref_meg'] = config['allow_ref_meg']

ica = ICA(**ica_params)

# == FIT ICA ==
ica.fit(epo)
print(f'ICA fitted on {len(epo)} epochs with {ica.n_components} components')
fit_msg = f'ICA fitted on {len(epo)} epochs with {ica.n_components} components'
add_info_to_product(product_items, fit_msg, 'success')

# == PRINT EXPLAINED VARIANCE ==
explained_var_ratio = ica.get_explained_variance_ratio(epo)
for channel_type, ratio in explained_var_ratio.items():
    msg = f'Fraction of {channel_type} variance explained by all components: {ratio:.4f}'
    print(msg)
    add_info_to_product(product_items, msg)

# == SAVE ICA ==
ica.save(os.path.join('out_dir', 'ica.fif'), overwrite=True)
print(f'ICA saved to out_dir/ica.fif')

# == PLOT COMPONENTS TOPOGRAPHY ==
fig = plt.figure(figsize=(15, 8))
ica.plot_components(show=False)
components_fig_path = os.path.join('out_figs', 'components_topo.png')
components_base64 = save_figure_with_base64(fig, components_fig_path, 
                                             dpi_file=150, dpi_base64=80)
plt.close(fig)

# == PLOT DETAILED COMPONENT PROPERTIES ==
picks_to_plot = config.get('picks_to_plot', 5)
fs = ica.plot_properties(epo, picks=list(range(min(picks_to_plot, ica.n_components))), show=False)
for i, f in enumerate(fs):
    comp_fig_path = os.path.join('out_figs', f'component_{i:02d}.png')
    f.savefig(comp_fig_path, dpi=150)
    plt.close(f)

# == CREATE REPORT ==
report = mne.Report(title='ICA Fitting Report (Epochs)')
report.add_ica(ica, 'ICA Decomposition', inst=epo)
report_path = os.path.join('out_report', 'report_ica.html')
report.save(report_path, overwrite=True)
print(f'Report saved to {report_path}')

# == CREATE PRODUCT.JSON ==
add_image_to_product(product_items, 'ICA Components', base64_data=components_base64)
add_info_to_product(product_items, 
                    f'ICA decomposition successfully computed and saved', 
                    'success')
create_product_json(product_items)



