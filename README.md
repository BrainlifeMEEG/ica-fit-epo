# ICA Fitting on Epoched Data

[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.761-blue.svg)](https://doi.org/10.25663/brainlife.app.761)

## Description

This Brainlife.io app computes an Independent Component Analysis (ICA) decomposition on epoched MEG/EEG data using MNE-Python's `mne.preprocessing.ICA.fit()` method. ICA is a blind source separation technique that decomposes multivariate signals into independent non-Gaussian components, commonly used to isolate artifacts (e.g. eye blinks, cardiac activity) for later removal. The app optionally high/low-pass filters the epochs before fitting, fits the ICA decomposition with the configured algorithm, and reports the fraction of variance explained by all components per channel type. Component exclusion itself is not performed here — it is the job of the downstream `ICA-apply-epo` app.

The app generates:
- The fitted ICA decomposition (`ica.fif`)
- Topographic plots of all ICA components
- Detailed property plots for each fitted component
- An HTML QC report with the ICA decomposition
- A `product.json` summarizing the fit and embedding a component image

## Inputs

- **`epo`** (`neuro/meeg/mne/epochs`): epoched MEG/EEG data to decompose with ICA (required)

## Outputs

- **`out_dir/ica.fif`**: fitted ICA decomposition object
- **`out_figs/components_topo_NN.png`**: topographic plot(s) of all ICA components
- **`out_figs/component_NN.png`**: detailed property plot for each fitted component
- **`out_report/report_ica.html`**: QC report with the ICA decomposition
- **`product.json`**: summary of the fit (explained variance, applied filter) with a component image embedded

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `n_components` | number | `None` | Number of principal components (from the pre-whitening PCA step) passed to the ICA algorithm during fitting. If not provided, defaults to 50, or the rank of the data, whichever is smallest. |
| `l_freq` | number | `None` | Low frequency cut-off for optional high-pass filtering of the epochs before ICA. Filtering is applied if either `l_freq` or `h_freq` is set; the filtered data itself is not saved. |
| `h_freq` | number | `None` | High frequency cut-off for optional low-pass filtering before ICA (see `l_freq`). |
| `method` | string | `"fastica"` | ICA method passed to `ICA(method=...)` (`'fastica'`, `'picard'`, `'infomax'`, etc.). Use `fit_params` for extended-Infomax/Picard options. |
| `noise_cov` | string | `None` | Optional noise covariance used for pre-whitening. If unset, channels are z-standardized by type instead. |
| `random_state` | number | `42` | Seed for the NumPy random number generator, for reproducible fits. |
| `max_iter` | string | `"auto"` | Maximum number of iterations during fit. `'auto'` sets 1000 for `'fastica'` and 500 for `'infomax'`/`'picard'`. |
| `allow_ref_meg` | boolean | `false` | Allow ICA on MEG reference channels. |
| `fit_params` | string | `None` | Additional parameters passed to the ICA estimator (`FastICA`, `picard()`, `infomax()`), as a dict (e.g. `dict(extended=True)`). |

## Usage

### Running on Brainlife.io

1. Select your epoched MEG/EEG `.fif` dataset as the `epo` input.
2. Optionally set `l_freq`/`h_freq` to high/low-pass filter the epochs before fitting.
3. Adjust `n_components`, `method`, `max_iter`, `fit_params`, and the other advanced parameters as needed.
4. Submit the process.

### Local Testing

```bash
# Edit config.json to point "epo" at a real epoched .fif file, then:
python main.py
```

## Technical Details

- Uses MNE-Python's `ICA` class for decomposition.
- Channels are pre-whitened using PCA before ICA fitting; an optional noise covariance can be specified for improved pre-whitening.
- Explained variance ratios are computed per channel type for diagnostic purposes.
- Generates an interactive QC report using `mne.Report`.
- Results are compatible with `ICA-apply-epo` for component exclusion.

## Authors

- Maximilien Chaumon (https://github.com/dnacombo)
- Saeed Zahran (https://github.com/saeedzahranutc)

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2

Gramfort A, Luessi M, Larson E, Engemann DA, Strohmeier D, Brodbeck C, Goj R, Jas M, Brooks T, Parkkonen L, and Hämäläinen MS. MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience, 7(267):1–13, 2013. https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
