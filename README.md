<h1 align="center">Setup and fit ICA</h1>

<p align="center">
  Fits an ICA decomposition to epoched MEG/EEG data with MNE-Python, with optional pre-filtering, and outputs the ICA solution and an HTML QC report with component plots.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.761"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.761-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Fits an ICA decomposition to epoched MEG/EEG data with MNE-Python, with optional pre-filtering, and outputs the ICA solution and an HTML QC report with component plots.**

Fits mne.preprocessing.ICA (fastica, picard or infomax) on the epochs, filtering a copy first when l_freq or h_freq is set, and plots topographies and properties of the components. Use it on epoched data before an ICA-apply App to remove artifact components. n_components defaults to 50 or the data rank, whichever is smaller.

| | |
|---|---|
| **Inputs** | `neuro/meeg/mne/epochs` |
| **Outputs** | `neuro/meeg/mne/ica` · `report/html` |
| **Container** | `brainlifemeeg/mne:1.12.1` |
| **Resources** | 8 CPUs · 20 GB memory · 1 h walltime |
| **Run it** | [doi.org/10.25663/brainlife.app.761](https://doi.org/10.25663/brainlife.app.761) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `data` | `neuro/meeg/mne/epochs` | yes | Epoched MEG/EEG data in MNE epochs .fif format. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/ica` | The fitted ICA object. |
| `out_report` | `report/html` | HTML QC report with the ICA decomposition and component property plots. |

<details>
<summary><b>Parameters</b> (9)</summary>

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

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.761](https://doi.org/10.25663/brainlife.app.761), choose `neuro/meeg/mne/epochs` from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/meeg/mne/ica`, `report/html`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlifemeeg/mne:1.12.1`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "epo": "/path/to/data/epo",
       "n_components": "<number>",
       "l_freq": "<number>",
       "h_freq": "<number>",
       "method": "fastica",
       "noise_cov": "",
       "random_state": 42,
       "max_iter": "auto",
       "allow_ref_meg": false,
       "fit_params": ""
   }
   ```

3. Run `./main`.

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

## Local Testing

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

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- Setup and fit ICA. brainlife.io App. [doi:10.25663/brainlife.app.761](https://doi.org/10.25663/brainlife.app.761)
- Gramfort A, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Maximilien Chaumon (https://github.com/dnacombo)
- Saeed Zahran (https://github.com/saeedzahranutc)

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
