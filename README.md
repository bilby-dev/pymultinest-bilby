# pymultinest-bilby

Plugin for using pymultinest with bilby.

This plugin exposes the `pymultinest` sampler via the `bilby.samplers` entry point.
Once installed, you can select it in `bilby.run_sampler` using `sampler='pymultinest'`.

## Installation

## Using pip

The package can be install using pip

```
pip install pymultinest-bilby
```

However, this does not install `multinest`, which must be installed separately
either following the instructions [here](https://johannesbuchner.github.io/PyMultiNest/install.html#prerequisites-for-building-the-libraries) or from conda-forge:

```
conda install conda-forge:multinest
```

## Using conda

Since `multinest` is available via conda-forge, the package can be installed
directly:

```
conda install conda-forge:pymultinest-bilby
```
