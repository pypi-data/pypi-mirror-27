# encoding: utf-8
from __future__ import absolute_import, division, print_function

import numpy as np
import pytest as pt
from numpy.testing import (assert_almost_equal, assert_array_almost_equal)

import mpnum.factory as factory
import mpnum.mparray as mp
import mpnum.special as mpsp
from mpnum._testing import assert_mpa_identical
from mpnum.utils import truncated_svd

MP_INNER_PARAMETERS = [(10, 10, 5), (20, 2, 10)]
MP_SUMUP_PARAMETERS = [(6, 2, 5000, 10, 200), (10, 2, 5000, 5, 20)]


############################
#  special.inner_prod_mps  #
############################
@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_inner_prod_mps(nr_sites, local_dim, rank, dtype, rgen):
    mpa1 = factory.random_mpa(nr_sites, local_dim, 1, dtype=dtype,
                              randstate=rgen, normalized=True)
    mpa2 = factory.random_mpa(nr_sites, local_dim, rank, dtype=dtype,
                              randstate=rgen, normalized=True)

    res_slow = mp.inner(mpa1, mpa2)
    res_fast = mpsp.inner_prod_mps(mpa1, mpa2)
    assert_almost_equal(res_slow, res_fast)

    try:
        mpsp.inner_prod_mps(mpa2, mpa1)
    except AssertionError:
        pass
    else:
        if rank > 1:
            raise AssertionError(
                "inner_prod_mps should only accept r=1 in first argument")

    mpa1 = factory.random_mpo(nr_sites, local_dim, 1)
    try:
        mpsp.inner_prod_mps(mpa1, mpa1)
    except AssertionError:
        pass
    else:
        raise AssertionError("inner_prod_mps should only accept ndims=1")


@pt.mark.benchmark(group="inner")
@pt.mark.parametrize('nr_sites, local_dim, rank', MP_INNER_PARAMETERS)
def test_inner_fast(nr_sites, local_dim, rank, benchmark, rgen):
    mpa1 = factory.random_mpa(nr_sites, local_dim, 1, dtype=np.float_,
                              randstate=rgen, normalized=True)
    mpa2 = factory.random_mpa(nr_sites, local_dim, rank, dtype=np.float_,
                              randstate=rgen, normalized=True)

    benchmark(mpsp.inner_prod_mps, mpa1, mpa2)


@pt.mark.benchmark(group="inner")
@pt.mark.parametrize('nr_sites, local_dim, rank', MP_INNER_PARAMETERS)
def test_inner_slow(nr_sites, local_dim, rank, benchmark, rgen):
    mpa1 = factory.random_mpa(nr_sites, local_dim, 1, dtype=np.float_,
                              randstate=rgen)
    mpa2 = factory.random_mpa(nr_sites, local_dim, rank, dtype=np.float_,
                              randstate=rgen)

    benchmark(mp.inner, mpa1, mpa2)


########################
#  special.sumup_prod  #
########################
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_sumup(nr_sites, local_dim, rank, rgen):
    rank = rank if rank is not np.nan else 1
    mpas = [factory.random_mpa(nr_sites, local_dim, 1, dtype=np.float_,
                               randstate=rgen)
            for _ in range(10 * rank)]
    weights = rgen.randn(len(mpas))

    # parameters chosen such that only one round of compression occurs
    summed_fast = mpsp.sumup(mpas, rank, weights=weights, svdfunc=truncated_svd)
    #  summed_slow = mp.sumup(mpa * w for mpa, w in zip(mpas, weights))
    summed_slow = mp.sumup(mpas, weights=weights)
    summed_slow.compress('svd', rank=rank, direction='right',
                         canonicalize=False)

    assert_mpa_identical(summed_fast, summed_slow)

    try:
        mpsp.sumup(mpas, rank, weights=np.ones(rank))
    except AssertionError:
        pass
    else:
        raise AssertionError("sumup did not catch unbalanced arguments")


#  @pt.mark.long
#  @pt.mark.benchmark(group="sumup", max_time=10)
#  @pt.mark.parametrize('nr_sites, local_dim, samples, target_r, max_r', MP_SUMUP_PARAMETERS)
#  def test_sumup_fast(nr_sites, local_dim, samples, target_, max_, rgen, benchmark):
#      mpas = [factory.random_mpa(nr_sites, local_dim, 1, dtype=np.float_, randstate=rgen)
#              for _ in range(samples)]
#      weights = rgen.randn(len(mpas))

#      benchmark(mpsp.sumup, mpas, weights=weights, target_=target_,
#                max_=max_)


#  @pt.mark.long
#  @pt.mark.benchmark(group="sumup", max_time=10)
#  @pt.mark.parametrize('nr_sites, local_dim, samples, target_, _', MP_SUMUP_PARAMETERS)
#  def test_sumup_slow(nr_, local_dim, samples, target_, _, rgen, benchmark):
#      mpas = [factory.random_mpa(nr_sites, local_dim, 1, dtype=np.float_, randstate=rgen)
#              for _ in range(samples)]
#      weights = rgen.randn(len(mpas))
#
#      benchmark(mpsp.sumup, mpas, weights=weights, target_bdim=target_bdim,
#                max_bdim=max_bdim)
#
#
#  @pt.mark.long
#  @pt.mark.benchmark(group="sumup", max_time=10)
#  @pt.mark.parametrize('nr_sites, local_dim, samples, target_bdim, _',
#                       MP_SUMUP_PARAMETERS)
#  def test_sumup_slow(nr_, local_dim, samples, target_bdim, _, rgen, benchmark):
#      mpas = [factory.random_mpa(nr_sites, local_dim, 1, dtype=np.float_,
#                                 randstate=rgen)
#              for _ in range(samples)]
#      weights = rgen.randn(len(mpas))
#
#      @benchmark
#      def sumup_slow():
#          summed = mp.sumup(mpa * w for w, mpa in zip(weights, mpas))
#          summed.compress('svd', =target_)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_local_add_sparse(nr_sites, local_dim, rank, dtype, rgen):
    # Just get some random number of summands, these parameters arent used
    # anyway later on
    nr_summands = nr_sites if rank is np.nan else nr_sites * rank
    summands = [factory.random_mpa(1, local_dim, 1, dtype=dtype,
                                   randstate=rgen).lt[0]
                for _ in range(nr_summands)]
    sum_slow = mp._local_add(summands).reshape((nr_summands,
                                                nr_summands * local_dim))
    sum_fast = mpsp._local_add_sparse([s.ravel() for s in summands]).toarray() \

    assert_array_almost_equal(sum_slow, sum_fast)
