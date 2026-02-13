# pymultinest-bilby

Plugin for using pymultinest with bilby.

This plugin exposes the `pymultinest` sampler via the `bilby.samplers` entry point.
Once installed, you can select it in `bilby.run_sampler` using `sampler='pymultinest'`.

## Installation

The package can be install using pip

```
pip install pymultinest-bilby
```

or conda

```
conda install conda-forge:pymultinest-bilby
```
