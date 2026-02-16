# ICA Fitting on Epoched Data

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.761-blue.svg)](https://doi.org/10.25663/brainlife.app.761)

Brainlife App to compute Independent Component Analysis (ICA) on epoched MEG/EEG data using MNE-Python's `ICA.fit()` method.

## Description

This app performs Independent Component Analysis (ICA) decomposition on epoched MEG/EEG data. ICA is a blind source separation technique that decomposes multivariate signals into independent non-Gaussian components. It is particularly useful for artifact removal from neuroimaging data.

The app:
- Loads MNE-compatible epoched data in FIF format
- Applies optional bandpass filtering before ICA fitting
- Fits the ICA decomposition using the specified algorithm
- Generates comprehensive visualizations of ICA components
- Creates an interactive HTML report for quality control

## Inputs

- **epo**: Path to MNE epochs data file in FIF format (.fif)

## Outputs

- **out_dir/ica.fif**: ICA decomposition object that can be applied to new data
- **out_figs/components_topo.png**: Topographic plot of all ICA components
- **out_figs/component_*.png**: Detailed properties for selected individual components
- **out_report/report_ica.html**: Interactive HTML report with component information
- **product.json**: Metadata file for Brainlife.io interface

## Configuration Parameters

All parameters are specified in `config.json`:

- **n_components** (integer, default: 20): Number of ICA components to estimate. Typically 20-30 for MEG/EEG data.
- **method** (string, default: 'fastica'): ICA algorithm to use. Options: 'fastica', 'picard', 'infomax', 'extended-infomax'
- **max_iter** (integer or 'auto', default: 'auto'): Maximum number of iterations during fitting
- **allow_ref_meg** (boolean, default: false): Whether to include MEG reference channels in ICA decomposition
- **noise_cov** (string, optional): Path to noise covariance matrix for pre-whitening. If empty, channels are z-standardized
- **random_state** (integer, optional): Random seed for reproducibility. If omitted, results will vary
- **fit_params** (string, optional): Python dictionary string of additional parameters for the ICA algorithm (e.g., "dict(extended=True)" for extended Infomax)
- **l_freq** (float, optional): High-pass filter cutoff frequency (Hz). Recommended: 1-2 Hz
- **h_freq** (float, optional): Low-pass filter cutoff frequency (Hz). Recommended: 80-100 Hz
- **picks_to_plot** (integer, default: 5): Number of individual components to show detailed plots for

## Usage

The app is typically run on the Brainlife.io platform through the web interface. To run locally:

```bash
python main.py
```

The `main.py` script reads the `config.json` file to get all parameters and data paths.

## Technical Details

### ICA Algorithms

- **fastica**: Fast ICA algorithm (default), typically fastest
- **picard**: Preconditioned ICA via Deflation, often more stable
- **infomax**: Infomax ICA algorithm
- **extended-infomax**: Extended Infomax (better for sub-Gaussian components)

### Pre-filtering

ICA typically benefits from high-pass filtering before fitting (recommended 1-2 Hz) to remove slow drifts. The app applies optional bandpass filtering specified by `l_freq` and `h_freq`.

### Component Selection

The number of components should be chosen based on:
- Data dimensionality and number of channels
- Available computational resources
- Typical values: 20-30 for full MEG arrays, 15-20 for reduced arrays or EEG

### Pre-whitening

Channels are pre-whitened using PCA before ICA fitting. Optional noise covariance can be specified for improved pre-whitening.


