import os

import bilby
import pytest
from pymultinest_bilby import Pymultinest


@pytest.fixture()
def SamplerClass():
    return Pymultinest


@pytest.fixture()
def outdir(tmp_path):
    return tmp_path / "outdir"


@pytest.fixture()
def create_sampler(SamplerClass, bilby_gaussian_likelihood_and_priors, outdir):
    likelihood, priors = bilby_gaussian_likelihood_and_priors

    def create_fn(**kwargs):
        return SamplerClass(
            likelihood,
            priors,
            outdir=outdir,
            label="test",
            use_ratio=False,
            **kwargs,
        )

    return create_fn


@pytest.fixture
def sampler(create_sampler):
    return create_sampler()


def test_default_kwargs(sampler):
    expected = dict(
        importance_nested_sampling=False,
        resume=True,
        verbose=True,
        sampling_efficiency="parameter",
        n_live_points=500,
        n_params=2,
        n_clustering_params=None,
        wrapped_params=[0, 0],
        multimodal=True,
        const_efficiency_mode=False,
        evidence_tolerance=0.5,
        n_iter_before_update=100,
        null_log_evidence=-1e90,
        max_modes=100,
        mode_tolerance=-1e90,
        seed=-1,
        context=0,
        write_output=True,
        log_zero=-1e100,
        max_iter=0,
        init_MPI=False,
        dump_callback="dumper",
    )

    sampler.kwargs["dump_callback"] = "dumper"
    assert sampler.kwargs["wrapped_params"] == [0, 0]
    assert sampler.kwargs == expected


def test_wrapped_parameters(SamplerClass, bilby_gaussian_likelihood_and_priors, outdir):
    likelihood, priors = bilby_gaussian_likelihood_and_priors
    priors["x"] = bilby.core.prior.Uniform(0, 10, "x", boundary="periodic")
    priors["y"] = bilby.core.prior.Uniform(0, 10, "y", boundary="reflective")

    sampler = SamplerClass(
        likelihood,
        priors,
        outdir=outdir,
        label="test",
        use_ratio=False,
    )

    assert sampler.kwargs["wrapped_params"] == [1, 0]


def test_expected_outputs(SamplerClass, outdir):
    expected = os.path.join(outdir / f"{SamplerClass.short_name}_test", "")
    filenames, dirs = SamplerClass.get_expected_outputs(outdir=outdir, label="test")
    assert expected in dirs
    assert isinstance(filenames, list)


@pytest.mark.parametrize(
    "equiv",
    bilby.core.sampler.base_sampler.NestedSampler.npoints_equiv_kwargs,
)
def test_translate_kwargs(create_sampler, equiv):
    sampler = create_sampler(**{equiv: 123})
    assert sampler.kwargs["n_live_points"] == 123
