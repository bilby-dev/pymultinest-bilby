import bilby
import pytest


@pytest.fixture(scope="session")
def sampler():
    return "pymultinest"


@pytest.fixture(scope="session")
def sampler_kwargs():
    return dict(nlive=100)


@pytest.fixture
def outdir(tmp_path):
    return tmp_path / "outdir"


@pytest.fixture
def conversion_function():
    def _conversion_function(parameters, likelihood, prior):
        converted = parameters.copy()
        if "derived" not in converted:
            converted["derived"] = converted["x"] * converted["y"]
        return converted

    return _conversion_function


def run_sampler(
    likelihood, priors, outdir, conversion_function, sampler, npool=None, **kwargs
):
    result = bilby.run_sampler(
        likelihood=likelihood,
        priors=priors,
        sampler=sampler,
        outdir=str(outdir),
        save="hdf5",
        npool=npool,
        conversion_function=conversion_function,
        **kwargs,
    )
    return result


def test_run_sampler(
    bilby_gaussian_likelihood_and_priors,
    outdir,
    conversion_function,
    npool,
    sampler,
    sampler_kwargs,
):
    likelihood, priors = bilby_gaussian_likelihood_and_priors
    result = run_sampler(
        likelihood,
        priors,
        outdir,
        conversion_function,
        sampler,
        npool,
        **sampler_kwargs,
    )
    assert "derived" in result.posterior
