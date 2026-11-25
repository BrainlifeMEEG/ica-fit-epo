# ICA Fitting on Epoched Data

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Fits an ICA decomposition to epoched MEG/EEG data with MNE-Python, with optional pre-filtering, and outputs the ICA solution and an HTML QC report with component plots.**

Fits mne.preprocessing.ICA (fastica, picard or infomax) on the epochs, filtering a copy first when l_freq or h_freq is set, and plots topographies and properties of the components. Use it on epoched data before an ICA-apply App to remove artifact components. n_components defaults to 50 or the data rank, whichever is smaller.

| | |
|---|---|
| 📥 **Inputs** | `neuro/meeg/mne/epochs` |
| 📤 **Outputs** | `neuro/meeg/mne/ica` · `report/html` |
| 🐳 **Container** | `brainlifemeeg/mne:1.12.1` |
| ⚙️ **Resources** | 8 CPUs · 20 GB memory · 1 h walltime |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.761](https://doi.org/10.25663/brainlife.app.761) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `data` | `neuro/meeg/mne/epochs` | yes | Epoched MEG/EEG data in MNE epochs .fif format. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/ica` | The fitted ICA object. |
| `out_report` | `report/html` | HTML QC report with the ICA decomposition and component property plots. |

<details>
<summary><b>⚙️ Parameters</b> (9)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `n_components` | number |  | Number of principal components (from the pre-whitening PCA step) that are passed to the ICA algorithm during fitting. If nothing is provided, will default to 50, or the rank of the data, whichever is smallest. |
| `l_freq` | number |  | Low frequency cut-off for high-pass filtering before ICA. default is None (no high-pass filtering). High-pass filtering is recommended on raw data before running ICA. Notice: the filtered data is not saved. You have to use the filtering app if you want to use filtered data subsequently. |
| `h_freq` | number |  | High frequency cut-off for low-pass filtering before ICA. default is None (no low-pass filtering). Notice: the filtered data is not saved. You have to use the filtering app if you want to use filtered data subsequently. |
| `method` | string | `fastica` | The ICA method to use in the fit method. Use the fit_params argument to set additional parameters. Specifically, if you want Extended Infomax, set method='infomax' and fit_params=dict(extended=True) (this also works for method='picard'). Defaults to 'fastica'. |
| `noise_cov` | string |  | Noise covariance used for pre-whitening. If None (default), channels are scaled to unit variance (“z-standardized”) as a group by channel type prior to the whitening by PCA. |
| `random_state` | number | `42` | A seed for the NumPy random number generator (RNG). If None (default), the seed will be obtained from the operating system (see RandomState for details), meaning it will most likely produce different output every time this function or method is run. To achieve reproducible results, pass a value here to explicitly initialize the RNG with a defined state. |
| `max_iter` | string | `auto` | Maximum number of iterations during fit. If 'auto', it will set maximum iterations to 1000 for 'fastica' and to 500 for 'infomax' or 'picard'. The actual number of iterations it took ICA.fit() to complete will be stored in the n_iter_ attribute. |
| `allow_ref_meg` | boolean | `false` | Allow ICA on MEG reference channels. Defaults to False. |
| `fit_params` | string |  | Additional parameters passed to the ICA estimator as specified by method. Allowed entries are determined by the various algorithm implementations: see FastICA, picard(), infomax(). |

</details>

📚 **References used by this App:**
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21:809-813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Gramfort A, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)

<!-- brainlife-app:end -->

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
