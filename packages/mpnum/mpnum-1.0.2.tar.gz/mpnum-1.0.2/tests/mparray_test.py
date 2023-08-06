# encoding: utf-8
# FIXME Is there a better metric to compare two arrays/scalars than
#       assert_(array)_almost_equal? Something that takes magnitude into
#       account?

from __future__ import absolute_import, division, print_function

import functools as ft
import itertools as it

import h5py as h5
import numpy as np
import pytest as pt
from numpy.testing import (assert_almost_equal, assert_array_almost_equal,
                           assert_array_equal)

import mpnum.factory as factory
import mpnum.mparray as mp
from mpnum import utils
from mpnum._testing import (assert_correct_normalization,
                            assert_mpa_almost_equal, assert_mpa_identical,
                            compression_svd)
from six.moves import range, zip


def update_copy_of(target, newvals):
    new = target.copy()
    new.update(newvals)
    return new


###############################################################################
#                         Basic creation & operations                         #
###############################################################################
@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, _', pt.MP_TEST_PARAMETERS)
def test_from_full(nr_sites, local_dim, _, rgen, dtype):
    psi = factory._random_vec(nr_sites, local_dim, randstate=rgen, dtype=dtype)
    mps = mp.MPArray.from_array(psi, 1)
    assert_array_almost_equal(psi, mps.to_array())
    assert mps.dtype == dtype

    op = factory._random_op(nr_sites, local_dim, randstate=rgen, dtype=dtype)
    mpo = mp.MPArray.from_array(op, 2)
    assert_array_almost_equal(op, mpo.to_array())
    assert mpo.dtype == dtype


def test_from_inhomogenous(rgen):
    array = rgen.randn(4, 3, 3, 3)
    mpa = mp.MPArray.from_array(array, ndims=(2, 1, 1))
    assert_array_almost_equal(array, mpa.to_array())
    assert mpa.ndims == (2, 1, 1)
    assert mpa.shape == ((4, 3), (3,), (3,))


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_from_kron(nr_sites, local_dim, rank, dtype):
    ndims = 2
    randfun = factory._randfuncs[dtype]
    factors = tuple(randfun([nr_sites] + ([local_dim] * ndims)))
    op = utils.mkron(*factors)
    op.shape = [local_dim] * (ndims * nr_sites)
    mpo = mp.MPArray.from_kron(factors)
    assert_array_almost_equal(op, mpo.to_array_global())
    assert mpo.dtype == dtype


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, _', pt.MP_TEST_PARAMETERS)
def test_conjugations(nr_sites, local_dim, _, rgen, dtype):
    op = factory._random_op(nr_sites, local_dim, randstate=rgen, dtype=dtype)
    mpo = mp.MPArray.from_array(op, 2)
    assert_array_almost_equal(np.conj(op), mpo.conj().to_array())
    assert mpo.conj().dtype == dtype

    mpo.canonicalize()
    mpo_c = mpo.conj()
    assert_correct_normalization(mpo_c)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, _', pt.MP_TEST_PARAMETERS)
def test_transpose(nr_sites, local_dim, _, rgen, dtype):
    op = factory._random_op(nr_sites, local_dim, randstate=rgen, dtype=dtype)
    mpo = mp.MPArray.from_array(utils.global_to_local(op, nr_sites), 2)

    opT = op.reshape((local_dim**nr_sites,) * 2).T \
        .reshape((local_dim,) * 2 * nr_sites)
    assert_array_almost_equal(opT, (mpo.T).to_array_global())
    assert mpo.T.dtype == dtype

    mpo.canonicalize()
    mpo_T = mpo.T
    assert_correct_normalization(mpo_T)


def test_transpose_axes(rgen):
    ldim = (2, 5, 3)
    axes = (2, 0, 1)
    new_ldim = tuple(ldim[ax] for ax in axes)

    # Easy (to implement) test: One physical site only.
    vec = factory._zrandn(ldim, rgen)
    mps = mp.MPArray.from_array(vec, ndims=len(ldim))
    assert len(mps) == 1

    vec_t = vec.transpose(axes)
    mps_t = mps.transpose(axes)
    mps_t_to_vec = mps_t.to_array()
    assert vec_t.shape == new_ldim
    assert_array_equal(mps_t_to_vec, vec_t)
    assert_correct_normalization(mps_t)

    # Test with 3 sites
    nr_sites = 3
    tensor = factory._zrandn(ldim * nr_sites, rgen)  # local form
    mpa = mp.MPArray.from_array(tensor, ndims=len(ldim))
    assert len(mpa) == nr_sites
    assert mpa.shape == (ldim,) * nr_sites
    # transpose axes in local form
    tensor_axes = tuple(ax + site * len(ldim)
                        for site in range(nr_sites) for ax in axes)
    tensor_t = tensor.transpose(tensor_axes)
    mpa_t = mpa.transpose(axes)
    mpa_t_to_tensor = mpa_t.to_array()
    assert mpa_t.shape == (new_ldim,) * nr_sites
    assert_array_almost_equal(mpa_t_to_tensor, tensor_t)
    assert_correct_normalization(mpa_t)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
def test_dump_and_load(tmpdir, dtype):
    mpa = factory.random_mpa(5, [(4,), (2, 3), (1,), (4,), (4, 3)],
                             (4, 7, 1, 3), dtype=dtype)
    mpa.canonicalize(left=1, right=3)

    with h5.File(str(tmpdir / 'dump_load_test.h5'), 'w') as buf:
        newgroup = buf.create_group('mpa')
        mpa.dump(newgroup)
    with h5.File(str(tmpdir / 'dump_load_test.h5'), 'r') as buf:
        mpa_loaded = mp.MPArray.load(buf['mpa'])
    assert_mpa_identical(mpa, mpa_loaded)

    mpa.dump(str(tmpdir / 'dump_load_test_str.h5'))
    mpa_loaded = mp.MPArray.load(str(tmpdir / 'dump_load_test_str.h5'))
    assert_mpa_identical(mpa, mpa_loaded)


###############################################################################
#                            Algebraic operations                             #
###############################################################################


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_sum(nr_sites, local_dim, rank, rgen, dtype):
    """Compare mpa.sum() with full array computation"""
    mpa = factory.random_mpa(nr_sites, local_dim, rank, rgen, dtype)
    array_sum = mpa.to_array().sum()
    # Test summation over all indices and different argument values.
    assert_almost_equal(mpa.sum(), array_sum)
    assert_almost_equal(mpa.sum(0), array_sum)
    assert_almost_equal(mpa.sum([0]), array_sum)
    assert_almost_equal(mpa.sum([[0]] * nr_sites), array_sum)

    # Test summation over site-dependent indices
    n_plegs = 3 if nr_sites <= 4 and local_dim <= 2 else 2
    mpa = factory.random_mpa(nr_sites, [local_dim] * n_plegs, rank, rgen, dtype)
    # Pseudo-randomly choose how many physical legs to sum over at each site.
    num_sum = ((rgen.choice(range(ndims + 1)), ndims) for ndims in mpa.ndims)
    # Pseudo-randomly choose which physical legs to sum over.
    axes = tuple(
        rgen.choice(range(ndims), num, replace=False) for num, ndims in num_sum)
    array_axes = tuple(n_plegs * pos + a
                       for pos, ax in enumerate(axes) for a in ax)
    mpa_sum = mpa.sum(axes)
    if hasattr(mpa_sum, 'to_array'):  # possibly, no physical legs are left
        mpa_sum = mpa_sum.to_array()
    array_sum = mpa.to_array().sum(array_axes)
    assert_array_almost_equal(mpa_sum, array_sum)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_dot(nr_sites, local_dim, rank, rgen, dtype):
    mpo1 = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                              randstate=rgen, dtype=dtype)
    op1 = mpo1.to_array_global()
    mpo2 = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                              randstate=rgen, dtype=dtype)
    op2 = mpo2.to_array_global()

    # Dotproduct of all 1st physical with 0th physical legs = np.dot
    dot_np = np.tensordot(op1.reshape((local_dim**nr_sites, ) * 2),
                          op2.reshape((local_dim**nr_sites, ) * 2),
                          axes=([1], [0]))
    dot_np = dot_np.reshape(op1.shape)
    dot_mp = mp.dot(mpo1, mpo2, axes=(1, 0)).to_array_global()
    assert_array_almost_equal(dot_np, dot_mp)
    assert dot_mp.dtype == dtype
    # this should also be the default axes
    dot_mp = mp.dot(mpo1, mpo2).to_array_global()
    assert_array_almost_equal(dot_np, dot_mp)

    # Dotproduct of all 0th physical with 1st physical legs = np.dot
    dot_np = np.tensordot(op1.reshape((local_dim**nr_sites, ) * 2),
                          op2.reshape((local_dim**nr_sites, ) * 2),
                          axes=([0], [1]))
    dot_np = dot_np.reshape(op1.shape)
    dot_mp = mp.dot(mpo1, mpo2, axes=(0, 1)).to_array_global()
    assert_array_almost_equal(dot_np, dot_mp)
    assert dot_mp.dtype == dtype
    # this should also be the default axes
    dot_mp = mp.dot(mpo1, mpo2, axes=(-2, -1)).to_array_global()
    assert_array_almost_equal(dot_np, dot_mp)


def test_dot_multiaxes(rgen):
    ldim1 = (2, 2, 3, 2)
    ldim2 = (3, 2, 4)
    ax1 = (0, 2)
    ax2 = (-2, 0)
    assert len(ax1) == len(ax2)

    # Easy (to implement) test: One physical site.
    vec1 = factory._zrandn(ldim1, rgen)
    vec2 = factory._zrandn(ldim2, rgen)
    mpa1 = mp.MPArray.from_array(vec1, ndims=len(ldim1))
    mpa2 = mp.MPArray.from_array(vec2, ndims=len(ldim2))
    assert len(mpa1) == 1
    assert len(mpa2) == 1

    mpa_prod = mp.dot(mpa1, mpa2, axes=(ax1, ax2)).to_array()
    vec_prod = np.tensordot(vec1, vec2, (ax1, ax2))
    assert_array_almost_equal(mpa_prod, vec_prod)

    # Test with 3 sites
    nr_sites = 3
    vec1 = factory._zrandn(ldim1 * nr_sites, rgen)  # local form
    vec2 = factory._zrandn(ldim2 * nr_sites, rgen)  # local form
    mpa1 = mp.MPArray.from_array(vec1, ndims=len(ldim1))
    mpa2 = mp.MPArray.from_array(vec2, ndims=len(ldim2))
    assert len(mpa1) == nr_sites
    assert len(mpa2) == nr_sites
    mpa_prod = mp.dot(mpa1, mpa2, axes=(ax1, ax2)).to_array()
    vec_ax1, vec_ax2 = (
        tuple(ax + site * nldim
              if ax >= 0 else ax - (nr_sites - site - 1) * nldim
              for site in range(nr_sites) for ax in ax_n)
        for ax_n, nldim in ((ax1, len(ldim1)), (ax2, len(ldim2)))
    )
    vec_prod = np.tensordot(vec1, vec2, (vec_ax1, vec_ax2))
    # The problem with vec_prod is: The order of the indices does not
    # match the order of the indices in mpa_prod. We need to change
    # that order:
    nldim1, nldim2 = (len(ldim1) - len(ax1), len(ldim2) - len(ax2))
    assert vec_prod.ndim == nr_sites * (nldim1 + nldim2)
    perm = tuple(
        offset + site * nldim + ax
        for site in range(nr_sites)
        for offset, nldim in ((0, nldim1), (nr_sites * nldim1, nldim2))
        for ax in range(nldim)
    )
    vec_prod = vec_prod.transpose(perm)
    assert_array_almost_equal(mpa_prod, vec_prod)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_partialdot(nr_sites, local_dim, rank, rgen, dtype):
    # Only for at least two sites, we can apply an operator to a part
    # of a chain.
    if nr_sites < 2:
        return
    part_sites = nr_sites // 2
    start_at = min(2, nr_sites // 2)

    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    op = mpo.to_array_global().reshape((local_dim**nr_sites,) * 2)
    mpo_part = factory.random_mpa(part_sites, (local_dim, local_dim), rank,
                                  randstate=rgen, dtype=dtype)
    op_part = mpo_part.to_array_global().reshape((local_dim**part_sites,) * 2)
    op_part_embedded = np.kron(
        np.kron(np.eye(local_dim**start_at), op_part),
        np.eye(local_dim**(nr_sites - part_sites - start_at)))

    prod1 = np.dot(op, op_part_embedded)
    prod2 = np.dot(op_part_embedded, op)
    prod1_mpo = mp.partialdot(mpo, mpo_part, start_at=start_at)
    prod2_mpo = mp.partialdot(mpo_part, mpo, start_at=start_at)
    prod1_mpo = prod1_mpo.to_array_global().reshape((local_dim**nr_sites,) * 2)
    prod2_mpo = prod2_mpo.to_array_global().reshape((local_dim**nr_sites,) * 2)

    assert_array_almost_equal(prod1, prod1_mpo)
    assert_array_almost_equal(prod2, prod2_mpo)
    assert prod1_mpo.dtype == dtype
    assert prod2_mpo.dtype == dtype


def test_partialdot_multiaxes(rgen):
    ldim1 = (2, 2, 3, 2)
    ldim2 = (3, 2, 4)
    ax1 = (0, 2)
    ax2 = (-2, 0)
    assert len(ax1) == len(ax2)

    # Easy (to implement) test: One physical site.
    vec1 = factory._zrandn(ldim1, rgen)
    vec2 = factory._zrandn(ldim2, rgen)
    mpa1 = mp.MPArray.from_array(vec1, ndims=len(ldim1))
    mpa2 = mp.MPArray.from_array(vec2, ndims=len(ldim2))
    assert len(mpa1) == 1
    assert len(mpa2) == 1

    mpa_prod = mp.partialdot(mpa1, mpa2, start_at=0, axes=(ax1, ax2)).to_array()
    vec_prod = np.tensordot(vec1, vec2, (ax1, ax2))
    assert_array_almost_equal(mpa_prod, vec_prod)

    # Test with 3 sites
    nr_sites = 3
    nr_sites_shorter = 2
    start_at = 1
    vec1 = factory._zrandn(ldim1 * nr_sites, rgen)  # local form
    vec2 = factory._zrandn(ldim2 * nr_sites_shorter, rgen)  # local form
    mpa1 = mp.MPArray.from_array(vec1, ndims=len(ldim1))
    mpa2 = mp.MPArray.from_array(vec2, ndims=len(ldim2))
    assert len(mpa1) == nr_sites
    assert len(mpa2) == nr_sites_shorter
    mpa_prod = mp.partialdot(mpa1, mpa2, start_at, axes=(ax1, ax2)).to_array()
    vec_ax1, vec_ax2 = (
        tuple(ax + (startsite + site) * nldim
              if ax >= 0 else ax - (nr_sites_shorter - site - 1) * nldim
              for site in range(nr_sites_shorter) for ax in ax_n)
        for ax_n, nldim, startsite in
        ((ax1, len(ldim1), start_at), (ax2, len(ldim2), 0))
    )
    vec_prod = np.tensordot(vec1, vec2, (vec_ax1, vec_ax2))
    # The problem with vec_prod is: The order of the indices does not
    # match the order of the indices in mpa_prod. We need to change
    # that order:
    nldim1, nldim2 = (len(ldim1) - len(ax1), len(ldim2) - len(ax2))
    assert vec_prod.ndim == (start_at * len(ldim1)
                             + nr_sites_shorter * (nldim1 + nldim2))
    # For sites before start_at, the axes of `vec1` remain unchanged.
    perm = tuple(range(len(ldim1) * start_at))
    # For site start_at and following sites, we need to fix the order
    # of sites. We use the same scheme as `test_dot_multiaxes` above.
    perm2 = tuple(
        offset + site * nldim + ax
        for site in range(nr_sites_shorter)
        for offset, nldim in ((0, nldim1), (nr_sites_shorter * nldim1, nldim2))
        for ax in range(nldim)
    )
    # Now we displace that permutation by the number of unchanged
    # sites at the beginning:
    perm += tuple(len(perm) + ax for ax in perm2)
    vec_prod = vec_prod.transpose(perm)
    assert_array_almost_equal(mpa_prod, vec_prod)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_inner_vec(nr_sites, local_dim, rank, rgen, dtype):
    mp_psi1 = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen,
                                 dtype=dtype)
    psi1 = mp_psi1.to_array().ravel()
    mp_psi2 = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen,
                                 dtype=dtype)
    psi2 = mp_psi2.to_array().ravel()

    inner_np = np.vdot(psi1, psi2)
    inner_mp = mp.inner(mp_psi1, mp_psi2)
    assert_almost_equal(inner_mp, inner_np)
    assert inner_mp.dtype == dtype


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_inner_mat(nr_sites, local_dim, rank, rgen, dtype):
    mpo1 = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                              randstate=rgen, dtype=dtype)
    op1 = mpo1.to_array_global().reshape((local_dim**nr_sites, ) * 2)
    mpo2 = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                              randstate=rgen, dtype=dtype)
    op2 = mpo2.to_array_global().reshape((local_dim**nr_sites, ) * 2)

    inner_np = np.trace(np.dot(op1.conj().transpose(), op2))
    inner_mp = mp.inner(mpo1, mpo2)
    assert_almost_equal(inner_mp, inner_np)
    assert inner_mp.dtype == dtype


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_sandwich(nr_sites, local_dim, rank, rgen, dtype):
    mps = factory.random_mpa(nr_sites, local_dim, rank,
                             randstate=rgen, dtype=dtype, normalized=True)
    mps2 = factory.random_mpa(nr_sites, local_dim, rank,
                              randstate=rgen, dtype=dtype, normalized=True)
    mpo = factory.random_mpa(nr_sites, [local_dim] * 2, rank,
                             randstate=rgen, dtype=dtype)
    mpo.canonicalize()
    mpo /= mp.trace(mpo)

    vec = mps.to_array().ravel()
    op = mpo.to_array_global().reshape([local_dim**nr_sites] * 2)
    res_arr = np.vdot(vec, np.dot(op, vec))
    res_mpo = mp.inner(mps, mp.dot(mpo, mps))
    res_sandwich = mp.sandwich(mpo, mps)
    assert_almost_equal(res_mpo, res_arr)
    assert_almost_equal(res_sandwich, res_arr)

    vec2 = mps2.to_array().ravel()
    res_arr = np.vdot(vec2, np.dot(op, vec))
    res_mpo = mp.inner(mps2, mp.dot(mpo, mps))
    res_sandwich = mp.sandwich(mpo, mps, mps2)
    assert_almost_equal(res_mpo, res_arr)
    assert_almost_equal(res_sandwich, res_arr)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_norm(nr_sites, local_dim, rank, dtype, rgen):
    mp_psi = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen,
                                dtype=dtype)
    psi = mp_psi.to_array()

    assert_almost_equal(mp.inner(mp_psi, mp_psi), mp.norm(mp_psi)**2)
    assert_almost_equal(np.sum(psi.conj() * psi), mp.norm(mp_psi)**2)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_normdist(nr_sites, local_dim, rank, dtype, rgen):
    psi1 = factory.random_mpa(nr_sites, local_dim, rank, dtype=dtype,
                              randstate=rgen)
    psi2 = factory.random_mpa(nr_sites, local_dim, rank, dtype=dtype,
                              randstate=rgen)

    assert_almost_equal(mp.normdist(psi1, psi2), mp.norm(psi1 - psi2))


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank, keep_width',
                     [(6, 2, 4, 3), (4, 3, 5, 2)])
def test_partialtrace(nr_sites, local_dim, rank, keep_width, rgen, dtype):
    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    op = mpo.to_array_global()

    for site in range(nr_sites - keep_width + 1):
        traceout = tuple(range(site)) \
            + tuple(range(site + keep_width, nr_sites))
        axes = [(0, 1) if site in traceout else None for site in range(nr_sites)]
        red_mpo = mp.partialtrace(mpo, axes=axes)
        red_from_op = utils.partial_trace(op, traceout)
        assert_array_almost_equal(red_mpo.to_array_global(), red_from_op,
                                  err_msg="not equal at site {}".format(site))
        assert red_mpo.dtype == dtype


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim', [(4, 3)])
def test_partialtrace_axes(nr_sites, local_dim, rgen, dtype):
    mpa = factory.random_mpa(nr_sites, (local_dim,) * 3, 1,
                             randstate=rgen, dtype=dtype)

    # Verify that an exception is raised if `axes` does not refer to a
    # physical leg.
    valid = [(0, 2), (-3, -2)]
    invalid = [(0, 3), (-4, 2), (-4, 3)]
    for axes in valid:
        mp.partialtrace(mpa, axes=axes)
    for axes in invalid:
        with pt.raises(AssertionError) as exc:
            mp.partialtrace(mpa, axes=(0, 3))
        assert exc.value.args == ('Too few legs',), "Wrong assertion"


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_trace(nr_sites, local_dim, rank, rgen, dtype):
    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    op = mpo.to_array_global().reshape((local_dim**nr_sites,) * 2)

    mpo_trace = mp.trace(mpo)
    assert_almost_equal(np.trace(op), mpo_trace)
    assert np.array(mpo_trace).dtype == dtype


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_add_and_subtr(nr_sites, local_dim, rank, rgen, dtype):
    mpo1 = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                              randstate=rgen, dtype=dtype)
    op1 = mpo1.to_array_global()
    mpo2 = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                              randstate=rgen, dtype=dtype)
    op2 = mpo2.to_array_global()

    assert_array_almost_equal(op1 + op2, (mpo1 + mpo2).to_array_global())
    assert_array_almost_equal(op1 - op2, (mpo1 - mpo2).to_array_global())
    assert (mpo1 + mpo2).dtype == dtype
    assert (mpo1 + mpo2).dtype == dtype

    mpo1 += mpo2
    assert_array_almost_equal(op1 + op2, mpo1.to_array_global())
    assert mpo1.dtype == dtype


@pt.mark.parametrize('nr_sites, local_dim, rank', [(3, 2, 2)])
def test_operations_typesafety(nr_sites, local_dim, rank, rgen):
    # create a real MPA
    mpo1 = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                              randstate=rgen, dtype=np.float_)
    mpo2 = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                              randstate=rgen, dtype=np.complex_)

    assert mpo1.dtype == np.float_
    assert mpo2.dtype == np.complex_

    assert (mpo1 + mpo1).dtype == np.float_
    assert (mpo1 + mpo2).dtype == np.complex_
    assert (mpo2 + mpo1).dtype == np.complex_

    assert mp.sumup((mpo1, mpo1)).dtype == np.float_
    assert mp.sumup((mpo1, mpo2)).dtype == np.complex_
    assert mp.sumup((mpo2, mpo1)).dtype == np.complex_

    assert (mpo1 - mpo1).dtype == np.float_
    assert (mpo1 - mpo2).dtype == np.complex_
    assert (mpo2 - mpo1).dtype == np.complex_

    mpo1 += mpo2
    assert mpo1.dtype == np.complex_


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_sumup(nr_sites, local_dim, rank, rgen, dtype):
    mpas = [factory.random_mpa(nr_sites, local_dim, 3, dtype=dtype, randstate=rgen)
            for _ in range(rank if rank is not np.nan else 1)]
    sum_naive = ft.reduce(mp.MPArray.__add__, mpas)
    sum_mp = mp.sumup(mpas)

    assert_array_almost_equal(sum_naive.to_array(), sum_mp.to_array())
    assert all(r <= 3 * rank for r in sum_mp.ranks)
    assert(sum_mp.dtype is dtype)

    weights = rgen.randn(len(mpas))
    summands = [w * mpa for w, mpa in zip(weights, mpas)]
    sum_naive = ft.reduce(mp.MPArray.__add__, summands)
    sum_mp = mp.sumup(mpas, weights=weights)
    assert_array_almost_equal(sum_naive.to_array(), sum_mp.to_array())
    assert all(r <= 3 * rank for r in sum_mp.ranks)
    assert(sum_mp.dtype is dtype)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_mult_mpo_scalar(nr_sites, local_dim, rank, rgen, dtype):
    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    # FIXME Change behavior of to_array
    # For nr_sites == 1, changing `mpo` below will change `op` as
    # well, unless we call .copy().
    op = mpo.to_array_global().copy()
    scalar = rgen.randn()

    assert_array_almost_equal(scalar * op, (scalar * mpo).to_array_global())

    mpo *= scalar
    assert_array_almost_equal(scalar * op, mpo.to_array_global())
    assert mpo.dtype == dtype
    assert (1.j * mpo).dtype == np.complex_


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_div_mpo_scalar(nr_sites, local_dim, rank, rgen):
    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             dtype=np.complex_, randstate=rgen)
    # FIXME Change behavior of to_array
    # For nr_sites == 1, changing `mpo` below will change `op` as
    # well, unless we call .copy().
    op = mpo.to_array_global().copy()
    scalar = rgen.randn() + 1.j * rgen.randn()

    assert_array_almost_equal(op / scalar, (mpo / scalar).to_array_global())

    mpo /= scalar
    assert_array_almost_equal(op / scalar, mpo.to_array_global())


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_chain(nr_sites, local_dim, rank, rgen, dtype):
    # This test produces at most `nr_sites` by tensoring two
    # MPOs. This doesn't work for :code:`nr_sites = 1`.
    if nr_sites < 2:
        return

    # NOTE: Everything here is in local form!!!
    mpo = factory.random_mpa(nr_sites // 2, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    op = mpo.to_array()

    # Test with 2-factors with full form
    mpo_double = mp.chain((mpo, mpo))
    op_double = np.tensordot(op, op, axes=(tuple(), ) * 2)
    assert len(mpo_double) == 2 * len(mpo)
    assert_array_almost_equal(op_double, mpo_double.to_array())
    assert_array_equal(mpo_double.ranks, mpo.ranks + (1,) + mpo.ranks)
    assert mpo.dtype == dtype

    # Test 3-factors iteratively (since full form would be too large!!
    diff = mp.chain((mpo, mpo, mpo)) - mp.chain((mpo, mp.chain((mpo, mpo))))
    diff.canonicalize()
    assert len(diff) == 3 * len(mpo)
    assert mp.norm(diff) < 1e-6


# local_dim, rank
MP_TEST_PARAMETERS_INJECT = [(2, 4), (3, 3), (2, 5), (2, 1), (1, 2)]


@pt.mark.parametrize('local_dim, rank', MP_TEST_PARAMETERS_INJECT)
def test_inject(local_dim, rank):
    """mp.inject() vs. computation with full arrays"""
    # rank is np.nan for nr_sites = 1 (first argument,
    # ignored). We require a value for rank.
    if np.isnan(rank):
        return

    # ndims = 3 is hardcoded below (argument to .transpose()).
    # Uniform local dimension is also hardcoded below (arguments to
    # .reshape()).
    ndims = 3
    local_dim = (local_dim,) * ndims

    a, b, c = factory._zrandn((3, 2) + local_dim)
    # We don't use b[1, :]
    b = b[0, :]
    # Here, only global order (as given by np.kron()).
    abbc0 = utils.mkron(a[0, :], b, b, c[0, :])
    abbc1 = utils.mkron(a[1, :], b, b, c[1, :])
    abbc = (abbc0 + abbc1).reshape(4 * local_dim)
    ac0 = np.kron(a[0, :], c[0, :])
    ac1 = np.kron(a[1, :], c[1, :])
    ac = (ac0 + ac1).reshape(2 * local_dim)
    ac_mpo = mp.MPArray.from_array(utils.global_to_local(ac, sites=2), ndims)
    abbc_mpo = mp.inject(ac_mpo, pos=1, num=2, inject_ten=b)
    abbc_mpo2 = mp.inject(ac_mpo, pos=[1], num=[2], inject_ten=[b])
    abbc_mpo3 = mp.inject(ac_mpo, pos=[1], num=None, inject_ten=[[b, b]])
    assert_array_almost_equal(abbc, abbc_mpo.to_array_global())
    assert_array_almost_equal(abbc, abbc_mpo2.to_array_global())
    assert_array_almost_equal(abbc, abbc_mpo3.to_array_global())

    # Here, only local order.
    ac = factory._zrandn(local_dim * 2)
    b = factory._zrandn(local_dim)
    acb = np.tensordot(ac, b, axes=((), ()))
    abc = acb.transpose((0, 1, 2, 6, 7, 8, 3, 4, 5))
    ac_mpo = mp.MPArray.from_array(ac, ndims)
    abc_mpo = mp.inject(ac_mpo, pos=1, num=1, inject_ten=b)
    # Keep local order
    abc_from_mpo = abc_mpo.to_array()
    assert_array_almost_equal(abc, abc_from_mpo)

    # ndims = 2 is hardcoded below (argument to .transpose()).
    # Uniform local dimension is also hardcoded below (arguments to
    # .reshape()).
    ndims = 2
    local_dim = (local_dim[0],) * ndims

    a, c = factory._zrandn((2, 2) + local_dim)
    b = np.eye(local_dim[0])
    # Here, only global order (as given by np.kron()).
    abbc0 = utils.mkron(a[0, :], b, b, c[0, :])
    abbc1 = utils.mkron(a[1, :], b, b, c[1, :])
    abbc = (abbc0 + abbc1).reshape(4 * local_dim)
    ac0 = np.kron(a[0, :], c[0, :])
    ac1 = np.kron(a[1, :], c[1, :])
    ac = (ac0 + ac1).reshape(2 * local_dim)
    ac_mpo = mp.MPArray.from_array(utils.global_to_local(ac, sites=2), ndims)
    abbc_mpo = mp.inject(ac_mpo, pos=1, num=2, inject_ten=None)
    abbc_mpo2 = mp.inject(ac_mpo, pos=[1], num=[2])
    abbc_mpo3 = mp.inject(ac_mpo, pos=[1], inject_ten=[[None, None]])
    assert_array_almost_equal(abbc, abbc_mpo.to_array_global())
    assert_array_almost_equal(abbc, abbc_mpo2.to_array_global())
    assert_array_almost_equal(abbc, abbc_mpo3.to_array_global())

    # Here, only local order.
    ac = factory._zrandn(local_dim * 2)
    b = np.eye(local_dim[0])
    acb = np.tensordot(ac, b, axes=((), ()))
    abc = acb.transpose((0, 1, 4, 5, 2, 3))
    ac_mpo = mp.MPArray.from_array(ac, ndims)
    abc_mpo = mp.inject(ac_mpo, pos=1, num=1, inject_ten=None)
    # Keep local order
    abc_from_mpo = abc_mpo.to_array()
    assert_array_almost_equal(abc, abc_from_mpo)


@pt.mark.parametrize('local_dim, rank', MP_TEST_PARAMETERS_INJECT)
def test_inject_many(local_dim, rank, rgen):
    """Calling mp.inject() repeatedly vs. calling it with sequence arguments"""
    mpa = factory.random_mpa(3, local_dim, rank, rgen, normalized=True,
                             dtype=np.complex_)
    inj_lt = [factory._zrandn(s, rgen) for s in [(2, 3), (1,), (2, 2), (3, 2)]]

    mpa_inj1 = mp.inject(mpa, 1, None, [inj_lt[0]])
    mpa_inj1 = mp.inject(mpa_inj1, 2, 1, inj_lt[0])
    mpa_inj1 = mp.inject(mpa_inj1, 4, None, [inj_lt[2]])
    mpa_inj2 = mp.inject(mpa, [1, 2], [2, None], [inj_lt[0], [inj_lt[2]]])
    mpa_inj3 = mp.inject(mpa, [1, 2], [2, 1], [inj_lt[0], inj_lt[2]])
    assert_mpa_almost_equal(mpa_inj1, mpa_inj2, True)
    assert_mpa_almost_equal(mpa_inj1, mpa_inj3, True)

    inj_lt = [inj_lt[:2], inj_lt[2:]]
    mpa_inj1 = mp.inject(mpa, 1, None, inj_lt[0])
    mpa_inj1 = mp.inject(mpa_inj1, 4, inject_ten=inj_lt[1])
    mpa_inj2 = mp.inject(mpa, [1, 2], None, inj_lt)
    assert_mpa_almost_equal(mpa_inj1, mpa_inj2, True)


def test_inject_shapes(rgen):
    """Check that mp.inject() picks up the correct shape"""
    mpa = factory.random_mpa(3, ([1], [2], [3]), 3, rgen, normalized=True)
    print(mpa.shape)
    mpa_inj = mp.inject(mpa, [0, 2], [1, 1])
    assert mpa_inj.shape == ((1, 1), (1,), (2,), (3, 3), (3,))
    mpa_inj = mp.inject(mpa, [1, 3], [1, 1], None)
    assert mpa_inj.shape == ((1,), (2, 2), (2,), (3,), (3, 3))


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_inject_vs_chain(nr_sites, local_dim, rank, rgen):
    """Compare mp.inject() with mp.chain()"""
    if nr_sites == 1:
        return
    mpa = factory.random_mpa(nr_sites // 2, local_dim, rank, rgen,
                             dtype=np.complex_, normalized=True)
    pten = [factory._zrandn((local_dim,) * 2) for _ in range(nr_sites // 2)]
    pten_mpa = mp.MPArray.from_kron(pten)

    outer1 = mp.chain((pten_mpa, mpa))
    outer2 = mp.inject(mpa, 0, inject_ten=pten)
    assert_mpa_almost_equal(outer1, outer2, True)

    outer1 = mp.chain((mpa, pten_mpa))
    outer2 = mp.inject(mpa, [len(mpa)], [None], inject_ten=[pten])
    assert_mpa_almost_equal(outer1, outer2, True)


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_localouter(nr_sites, local_dim, rank, rgen):
    mpa1 = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen)
    mpa2 = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen)
    arr1 = mpa1.to_array()
    arr1 = arr1.reshape(arr1.shape + (1, ) * nr_sites)
    arr2 = mpa2.to_array()
    arr2 = arr2.reshape((1, ) * nr_sites + arr2.shape)

    tensor_mp = mp.localouter(mpa1, mpa2)
    tensor_np = arr1 * arr2

    assert tensor_mp.ndims == (2,) * nr_sites
    assert tensor_np.shape == (local_dim,) * (2 * nr_sites)

    assert_array_almost_equal(tensor_np, tensor_mp.to_array_global())


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank, local_width',
                     [(5, 2, 3, 1), (6, 2, 4, 3), (4, 3, 5, 2)])
def test_local_sum(nr_sites, local_dim, rank, local_width, dtype, rgen):
    eye_mpa = factory.eye(1, local_dim)

    def embed_mpa(mpa, startpos):
        mpas = [eye_mpa] * startpos + [mpa] + \
               [eye_mpa] * (nr_sites - startpos - local_width)
        res = mp.chain(mpas)
        return res

    nr_startpos = nr_sites - local_width + 1
    mpas = [factory.random_mpa(local_width, (local_dim,) * 2, rank,
                               dtype=dtype, randstate=rgen)
            for i in range(nr_startpos)]

    # Embed with mp.chain() and calculate naive MPA sum:
    mpas_embedded = [embed_mpa(mpa, i) for i, mpa in enumerate(mpas)]
    mpa_sum = mpas_embedded[0]
    for mpa in mpas_embedded[1:]:
        mpa_sum += mpa

    # Compare with local_sum: Same result, smaller rank
    mpa_local_sum = mp.local_sum(mpas)

    # Check that local_sum() is no worse than naive sum
    assert all(d1 <= d2 for d1, d2 in zip(mpa_local_sum.ranks, mpa_sum.ranks))
    # Check that local_sum() is actually better than naive sum because
    # it calls local_sum_simple().
    assert any(d1 < d2 for d1, d2 in zip(mpa_local_sum.ranks, mpa_sum.ranks))
    assert_array_almost_equal(mpa_local_sum.to_array(), mpa_sum.to_array())


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_diag_1pleg(nr_sites, local_dim, rank, rgen):
    mpa = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen)
    mpa_np = mpa.to_array()
    # this should be a single, 1D numpy array
    diag_mp = mp.diag(mpa)
    diag_np = np.array([mpa_np[(i,) * nr_sites] for i in range(local_dim)])
    assert_array_almost_equal(diag_mp, diag_np)


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_diag_2plegs(nr_sites, local_dim, rank, rgen):
    mpa = factory.random_mpa(nr_sites, 2 * (local_dim,), rank, randstate=rgen)
    mpa_np = mpa.to_array()
    # this should be a single, 1D numpy array
    diag_mp = mp.diag(mpa, axis=1)
    diag_np = np.array([mpa_np[(slice(None), i) * nr_sites]
                        for i in range(local_dim)])
    for a, b in zip(diag_mp, diag_np):
        assert a.ndims[0] == 1
        assert_array_almost_equal(a.to_array(), b)


###############################################################################
#                         Shape changes, conversions                          #
###############################################################################
# nr_sites, local_dim, rank, sites_per_group
MP_TEST_PARAMETERS_GROUPS = [(6, 2, 4, 3), (6, 2, 4, 2), (4, 3, 5, 2)]


@pt.mark.parametrize('nr_sites, local_dim, rank, sites_per_group',
                     MP_TEST_PARAMETERS_GROUPS)
def test_group_sites(nr_sites, local_dim, rank, sites_per_group, rgen):
    assert (nr_sites % sites_per_group) == 0, \
        'nr_sites not a multiple of sites_per_group'
    mpa = factory.random_mpa(nr_sites, (local_dim,) * 2, rank, randstate=rgen)
    grouped_mpa = mpa.group_sites(sites_per_group)
    op = mpa.to_array()
    grouped_op = grouped_mpa.to_array()
    assert_array_almost_equal(op, grouped_op)


@pt.mark.parametrize('nr_sites, local_dim, rank, sites_per_group',
                     MP_TEST_PARAMETERS_GROUPS)
def test_split_sites(nr_sites, local_dim, rank, sites_per_group, rgen):
    assert (nr_sites % sites_per_group) == 0, \
        'nr_sites not a multiple of sites_per_group'
    ndims = (local_dim,) * (2 * sites_per_group)
    mpa = factory.random_mpa(nr_sites // sites_per_group, ndims, rank, randstate=rgen)
    split_mpa = mpa.split_sites(sites_per_group)
    op = mpa.to_array()
    split_op = split_mpa.to_array()
    assert_array_almost_equal(op, split_op)


@pt.mark.parametrize('ndims', [1, 2, 3])
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_reverse(nr_sites, local_dim, rank, ndims, rgen):
    mpa = factory.random_mpa(nr_sites, (local_dim,) * ndims, rank, rgen,
                             normalized=True)
    arr = mpa.to_array()
    rev_arr = arr.transpose(np.arange(nr_sites * ndims)
                            .reshape((nr_sites, ndims))[::-1, :].ravel())
    rev_mpa = mpa.reverse()
    rev_arr2 = rev_mpa.to_array()
    assert_almost_equal(rev_arr, rev_arr2)


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_bleg2pleg_pleg2bleg(nr_sites, local_dim, rank, rgen):
    mpa = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen)
    # +2 so we cover all possibilities
    mpa.canonicalize(left=nr_sites // 2, right=min(nr_sites // 2 + 2, nr_sites))

    for pos in range(nr_sites - 1):
        mpa_t = mpa.vleg2leg(pos)
        true_rank = mpa.ranks[pos]
        pshape = [(local_dim,)] * pos + [(local_dim, true_rank)] + \
            [(true_rank, local_dim)] + [(local_dim,)] * (nr_sites - pos - 2)
        ranks = list(mpa.ranks)
        ranks[pos] = 1
        assert_array_equal(mpa_t.shape, pshape)
        assert_array_equal(mpa_t.ranks, ranks)
        assert_correct_normalization(mpa_t)

        mpa_t = mpa_t.leg2vleg(pos)
        # This is an ugly hack, but necessary to use the assert_mpa_identical
        # function. Normalization-awareness gets lost in the process!
        mpa_t._lt._lcanonical, mpa_t._lt._rcanonical = mpa.canonical_form
        assert_mpa_identical(mpa, mpa_t)

    if nr_sites > 1:
        mpa = factory.random_mpa(nr_sites, local_dim, 1, randstate=rgen)
        mpa.canonicalize()
        mpa_t = mpa.leg2vleg(nr_sites // 2 - 1)
        assert_correct_normalization(mpa_t)


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_split(nr_sites, local_dim, rank, rgen):
    if nr_sites < 2:
        return
    mpa = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen)
    for pos in range(nr_sites - 1):
        mpa_l, mpa_r = mpa.split(pos)
        assert len(mpa_l) == pos + 1
        assert len(mpa_l) + len(mpa_r) == nr_sites
        assert_correct_normalization(mpa_l)
        assert_correct_normalization(mpa_r)
        recons = np.tensordot(mpa_l.to_array(), mpa_r.to_array(), axes=(-1, 0))
        assert_array_almost_equal(mpa.to_array(), recons)

    for (lnorm, rnorm) in it.product(range(nr_sites - 1), range(1, nr_sites)):
        mpa_l, mpa_r = mpa.split(nr_sites // 2 - 1)
        assert_correct_normalization(mpa_l)
        assert_correct_normalization(mpa_r)


def test_reshape(rgen):
    mpa = factory.random_mpa(4, [(3, 2), (4,), (2, 5), (24,)], 4)
    mpa.canonicalize()
    mpa_r = mpa.reshape([(2, 3), (2, 2), (10,), (3, 2, 4)])
    assert all(s1 == s2 for s1, s2 in
               zip(mpa_r.shape, [(2, 3), (2, 2), (10,), (3, 2, 4)]))
    assert_correct_normalization(mpa_r, *mpa.canonical_form)


###############################################################################
#                         Normalization & Compression                         #
###############################################################################
@pt.mark.parametrize('nr_sites, local_dim, _', pt.MP_TEST_PARAMETERS)
def test_canonicalization_from_full(nr_sites, local_dim, _, rgen):
    op = factory._random_op(nr_sites, local_dim, randstate=rgen)
    mpo = mp.MPArray.from_array(op, 2)
    assert_correct_normalization(mpo, nr_sites - 1, nr_sites)


# FIXME Add counter to normalization functions
@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_canonicalization_incremental(nr_sites, local_dim, rank, rgen, dtype):
    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    op = mpo.to_array_global()
    assert_correct_normalization(mpo, 0, nr_sites)
    assert_array_almost_equal(op, mpo.to_array_global())

    for site in range(1, nr_sites):
        mpo.canonicalize(left=site)
        assert_correct_normalization(mpo, site, nr_sites)
        assert_array_almost_equal(op, mpo.to_array_global())
        assert mpo.dtype == dtype

    for site in range(nr_sites - 1, 0, -1):
        mpo.canonicalize(right=site)
        assert_correct_normalization(mpo, site - 1, site)
        assert_array_almost_equal(op, mpo.to_array_global())
        assert mpo.dtype == dtype


# FIXME Add counter to normalization functions
@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_canonicalization_jump(nr_sites, local_dim, rank, rgen, dtype):
    # This test assumes at least two sites.
    if nr_sites == 1:
        return

    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    op = mpo.to_array_global()
    assert_correct_normalization(mpo, 0, nr_sites)
    assert_array_almost_equal(op, mpo.to_array_global())

    center = nr_sites // 2
    mpo.canonicalize(left=center - 1, right=center)
    assert_correct_normalization(mpo, center - 1, center)
    assert_array_almost_equal(op, mpo.to_array_global())
    assert mpo.dtype == dtype


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_canonicalization_full(nr_sites, local_dim, rank, rgen, dtype):
    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    op = mpo.to_array_global()
    assert_correct_normalization(mpo, 0, nr_sites)
    assert_array_almost_equal(op, mpo.to_array_global())

    mpo.canonicalize(right=1)
    assert_correct_normalization(mpo, 0, 1)
    assert_array_almost_equal(op, mpo.to_array_global())
    assert mpo.dtype == dtype

    ###########################################################################
    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             randstate=rgen, dtype=dtype)
    op = mpo.to_array_global()
    assert_correct_normalization(mpo, 0, nr_sites)
    assert_array_almost_equal(op, mpo.to_array_global())

    mpo.canonicalize(left=len(mpo) - 1)
    assert_correct_normalization(mpo, len(mpo) - 1, len(mpo))
    assert_array_almost_equal(op, mpo.to_array_global())
    assert mpo.dtype == dtype


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_canonicalization_default_args(nr_sites, local_dim, rank, rgen):
    # The following normalizations assume at least two sites.
    if nr_sites == 1:
        return

    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank, randstate=rgen)
    assert_correct_normalization(mpo, 0, nr_sites)

    mpo.canonicalize(left=1)
    mpo.canonicalize()
    assert_correct_normalization(mpo, nr_sites - 1, nr_sites)

    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank, randstate=rgen)
    assert_correct_normalization(mpo, 0, nr_sites)

    # The following normalization assumes at least three sites.
    if nr_sites == 2:
        return

    mpo.canonicalize(left=1)
    mpo.canonicalize(right=nr_sites - 2)
    mpo.canonicalize()
    assert_correct_normalization(mpo, 0, 1)


def test_canonicalization_compression(rgen):
    """If the rank is too large at the boundary, qr decompostion
    in normalization may yield smaller rank"""
    mpo = factory.random_mpa(sites=2, ldim=2, rank=20, randstate=rgen)
    mpo.canonicalize(right=1)
    assert_correct_normalization(mpo, 0, 1)
    assert mpo.ranks[0] == 2

    mpo = factory.random_mpa(sites=2, ldim=2, rank=20, randstate=rgen)
    mpo.canonicalize(left=1)
    assert_correct_normalization(mpo, 1, 2)
    assert mpo.ranks[0] == 2


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_mult_mpo_scalar_normalization(nr_sites, local_dim, rank, rgen):
    if nr_sites < 2:
        # Re-normalization has no effect for nr_sites == 1. There is
        # nothing more to test than :func:`test_mult_mpo_scalar`.
        return

    mpo = factory.random_mpa(nr_sites, (local_dim, local_dim), rank,
                             dtype=np.complex_, randstate=rgen)
    op = mpo.to_array_global()
    scalar = rgen.randn() + 1.j * rgen.randn()

    center = nr_sites // 2
    mpo.canonicalize(left=center - 1, right=center)
    mpo_times_two = scalar * mpo

    assert_array_almost_equal(scalar * op, mpo_times_two.to_array_global())
    assert_correct_normalization(mpo_times_two, center - 1, center)

    mpo *= scalar
    assert_array_almost_equal(scalar * op, mpo.to_array_global())
    assert_correct_normalization(mpo, center - 1, center)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_singularvals(nr_sites, local_dim, rank, dtype, rgen):
    mps = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen,
                             dtype=dtype, normalized=True, force_rank=True)
    psi = mps.to_array()
    # Start from a non-normalized state
    assert mps.canonical_form == (0, nr_sites)
    svals = list(mps.singularvals())
    if nr_sites == 1:
        assert mps.canonical_form == (0, 1)
    else:
        # The last local tensor update from _compress_svd_r() is not
        # carried out. This behaviour may change.
        assert mps.canonical_form == (nr_sites - 2, nr_sites - 1)
    assert len(svals) == nr_sites - 1
    for n_left in range(1, nr_sites):
        sv = svals[n_left - 1]
        mat = psi.reshape((local_dim**n_left, -1))
        sv2 = np.linalg.svd(mat, full_matrices=False, compute_uv=False)
        n_sv = min(len(sv), len(sv2))
        # Output from `svd()` is always in descending order
        assert_almost_equal(sv[n_sv:], 0.0)
        assert_almost_equal(sv2[n_sv:], 0.0)
        assert_array_almost_equal(sv[:n_sv], sv2[:n_sv])


@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_pad_ranks(nr_sites, local_dim, rank, rgen):
    mps = factory.random_mpa(nr_sites, local_dim, rank, randstate=rgen,
                             normalized=True)
    mps2 = mps.pad_ranks(2 * rank)
    assert mps2.ranks == tuple(min(d, 2 * rank) for d in mp.full_rank(mps.shape))
    assert_almost_equal(mp.normdist(mps, mps2), 0.0)
    mps2 = mps.pad_ranks(2 * rank, force_rank=True)
    assert mps2.ranks == (2 * rank,) * (nr_sites - 1)
    assert_almost_equal(mp.normdist(mps, mps2), 0.0)


#####################################
#  SVD and variational compression  #
#####################################

# nr_sites, local_dims, rank
compr_sizes = pt.mark.parametrize(
    # Start with `2*rank` and compress to `rank`.
    'nr_sites, local_dims, rank',
    (
        (4, 2, 3),
        pt.mark.long((2, (2, 3), 5)),
        pt.mark.long((5, 3, 4)),
        # TODO Create a separate marker for very long tests:
        # (4, (2, 3), 5),
        # (6, 2, 3),
        # (5, (2, 2, 2), 20),  # about  2 minutes (Core i5-3380M)
        # (16, 2, 10),         # about  2 minutes
        # (16, 2, 30),         # about 10 minutes
    )
)

compr_settings = pt.mark.parametrize(
    'comparg',
    (
        dict(method='svd', direction='left'),
        dict(method='svd', direction='right'),
        dict(method='svd', direction='left', relerr=1e-6),
        dict(method='svd', direction='right', relerr=1e-6),
        pt.mark.long(dict(method='var', num_sweeps=1, var_sites=1)),
        dict(method='var', num_sweeps=2, var_sites=1),
        pt.mark.long(dict(method='var', num_sweeps=3, var_sites=1)),
        pt.mark.long(dict(method='var', num_sweeps=1, var_sites=2)),
        dict(method='var', num_sweeps=2, var_sites=2),
        pt.mark.long(dict(method='var', num_sweeps=3, var_sites=2)),
        # See :func:`call_compression` below for the meaning of
        # 'fillbelow'.
        dict(method='var', num_sweeps=2, var_sites=1, startmpa='fillbelow'),
    )
)

# Test compression works for different normalizations of the MPA
# before compression.
compr_normalization = pt.mark.parametrize(
    'canonicalize',
    (dict(left=1, right=-1), dict()) +
    tuple(pt.mark.long(x) for x in (
        None,
        dict(left='afull'),
        dict(right='afull'),
        dict(left=1), dict(left=-1), dict(right=1), dict(right=-1),
        dict(left=1, right=2), dict(left=-2, right=-1),
        dict(left=1, right=-1),
    ))
)


def _chain_decorators(*args):
    def chain_decorator(f):
        for deco in reversed(args):
            f = deco(f)
        return f
    return chain_decorator


compr_test_params = _chain_decorators(compr_sizes, compr_settings,
                                      compr_normalization)


def normalize_if_applicable(mpa, nmz):
    """Check whether the given normalization can be applied.

    :param mp.MPArray mpa: Will call `mpa.canonicalize()`
    :param nmz: Keyword arguments for `mpa.canonicalize()` or `None`

    :returns: True if the normalization has been applied.

    `nmz=None` means not to call `mpa.canonicalize()` at all.

    The test whether the normalization can be applied is not
    comprehensive.

    """
    # Make sure the input is non-normalized. Otherwise, the output can
    # be more normalized than desired for the test.
    assert mpa.canonical_form == (0, len(mpa)), "want non-normalized MPA for test"
    if nmz is not None:
        if nmz.get('left') == 1 and nmz.get('right') == -1 and len(mpa) == 2:
            return False
        mpa.canonicalize(**nmz)
    return True


def call_compression(mpa, comparg, target_rank, rgen, call_compress=False):
    """Call `mpa.compress` or `mpa.compression` with suitable arguments.

    Does not make a copy of `mpa` in any case.

    :param target_rank: Compress to rank `target_rank`.
    :param call_compress: If `True`, call `mpa.compress` instead of
        `mpa.compression` (the default).
    :param comparg: Settings dict for compression.  If `relerr` is not
        present, add `rank = target_rank`.  If `startmpa` is equal to
        `'fillbelow'`, insert a random MPA.

    :returns: Compressed MPA.

    """
    if not ('relerr' in comparg) and (comparg.get('startmpa') == 'fillbelow'):
        startmpa = factory.random_mpa(len(mpa), mpa.shape[0], target_rank,
                                      normalized=True, randstate=rgen,
                                      dtype=mpa.dtype)
        comparg = update_copy_of(comparg, {'startmpa': startmpa})
    else:
        comparg = update_copy_of(comparg, {'rank': target_rank})

    if (comparg.get('method') == 'var') and not ('startmpa' in comparg):
        comparg = update_copy_of(comparg, {'randstate': rgen})

    if call_compress:
        return mpa.compress(**comparg)
    else:
        return mpa.compression(**comparg)


# We want check compression for inputs with norm different from 1.  In the next
# function and below, we do this with a normalized state multiplied with a
# constant with magnitude different from 1.  This is to avoid errors like
# "123456789.1 and 123456789.2 are not equal to six decimals" and is related to
# the fixme at the module start.


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@compr_test_params
def test_compression_and_compress(nr_sites, local_dims, rank, canonicalize,
                                  comparg, dtype, rgen):
    """Test that .compression() and .compress() produce identical results.

    """
    # See comment above on "4.2 *"
    mpa = 4.2 * factory.random_mpa(nr_sites, local_dims, rank * 2,
                                   normalized=True, dtype=dtype, randstate=rgen)
    if not normalize_if_applicable(mpa, canonicalize):
        return

    comparg = comparg.copy()
    if comparg['method'] == 'var':
        # Exact equality between `compr` and `compr2` below requires
        # using the same start vector in both cases.
        comparg['startmpa'] = factory.random_mpa(nr_sites, local_dims, rank,
                                                 dtype=dtype, randstate=rgen)

    # The results from .compression() and .compress() must match
    # exactly. No numerical difference is allowed.
    compr2 = mpa.copy()
    overlap2 = call_compression(compr2, comparg, rank, rgen, call_compress=True)
    compr, overlap = call_compression(mpa, comparg, rank, rgen)
    assert_almost_equal(overlap, overlap2)
    # FIXME Why do they not agree completely? We are doing the same thing...
    assert_mpa_identical(compr, compr2, decimal=12)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@compr_test_params
def test_compression_result_properties(nr_sites, local_dims, rank,
                                       canonicalize, comparg, rgen, dtype):
    """Test general properties of the MPA coming from a compression.

    * Compare SVD compression against simpler implementation

    * Check that all implementations return the correct overlap

    * Check that the rank has decreased and that it is as
      prescribed

    * Check that the normalization advertised in the result is correct

    * Check that compression doesnt change the dtype

    TODO: The worst case for compression is that all singular values
    have the same size.  This gives a fidelity lower bound for the
    compression result.  Check that lower bound.

    FIXME: Make this test a wrapper around MPArray.compression() to
    reduce code duplication.  This wrapper would replace
    call_compression().  This would also apply more tests
    .compress(). At the moment, we mostly test .compression().

    """
    mpa = 4.2 * factory.random_mpa(nr_sites, local_dims, rank * 2,
                                   normalized=True, randstate=rgen, dtype=dtype)
    if not normalize_if_applicable(mpa, canonicalize):
        return
    compr, overlap = call_compression(mpa.copy(), comparg, rank, rgen)

    # 'relerr' is currently 1e-6 and no rank is provided, so no
    # compression will occur.
    if 'relerr' not in comparg:
        # Check that the rank has changed.
        assert max(compr.ranks) < max(mpa.ranks)
        # Check that the target rank is satisfied
        assert max(compr.ranks) <= rank

    # Check that the inner product is correct.
    assert_almost_equal(overlap, mp.inner(mpa, compr))

    # SVD: Check that .canonical_form is as expected.
    if comparg['method'] == 'svd':
        normtarget = {'left': (0, 1), 'right': (len(compr) - 1, len(compr))}
        assert compr.canonical_form == normtarget[comparg['direction']]

    # Check the content of .canonical_form is correct.
    assert_correct_normalization(compr)
    assert compr.dtype == dtype

    # SVD: compare with alternative implementation
    if comparg['method'] == 'svd' and 'relerr' not in comparg:
        alt_compr = compression_svd(mpa.to_array(), rank, comparg['direction'])
        compr = compr.to_array()
        assert_array_almost_equal(alt_compr, compr)


@pt.mark.parametrize('dtype', pt.MP_TEST_DTYPES)
@pt.mark.parametrize('nr_sites, local_dim, rank', pt.MP_TEST_PARAMETERS)
def test_var_no_worse_than_svd(nr_sites, local_dim, rank, rgen, dtype):
    """Variational compresssion should always improve the overlap of the
    compressed mpa with the original one -- we test this by running a single
    variational compression sweep after an SVD compression and check that
    the overlap did not become smaller"""
    mpa = 4.2 * factory.random_mpa(nr_sites, local_dim, 5 * rank,
                                   normalized=True, randstate=rgen, dtype=dtype)
    mpa_svd, overlap_svd = mpa.compression(method='svd', rank=rank)
    overlap_svd /= mp.norm(mpa.copy()) * mp.norm(mpa_svd)

    mpa_var, overlap_var = mpa.compression(method='var', rank=rank,
                                           startmpa=mpa_svd, num_sweeps=1)
    overlap_var /= mp.norm(mpa) * mp.norm(mpa_var)

    assert overlap_var > overlap_svd * (1 - 1e-14)


@compr_test_params
def test_compression_rank_noincrease(nr_sites, local_dims, rank,
                                     canonicalize, comparg, rgen):
    """Check that rank does not increase if the target rank
    is larger than the MPA rank

    """
    if 'relerr' in comparg:
        return  # Test does not apply
    mpa = 4.2 * factory.random_mpa(nr_sites, local_dims, rank, normalized=True,
                                   randstate=rgen)
    norm = mp.norm(mpa.copy())
    if not normalize_if_applicable(mpa, canonicalize):
        return

    for factor in (1, 2):
        compr, overlap = call_compression(mpa, comparg, rank * factor, rgen)
        assert_almost_equal(overlap, norm**2)
        assert_mpa_almost_equal(compr, mpa, full=True)
        assert (np.array(compr.ranks) <= np.array(mpa.ranks)).all()


@pt.mark.parametrize('add', ('zero', 'self', 'self2'))
@compr_test_params
def test_compression_trivialsum(nr_sites, local_dims, rank, canonicalize,
                                comparg, add, rgen):
    """Check that `a + b` compresses exactly to a multiple of `a` if `b`
    is equal to one of `0`, `a` or `-2*a`

    """
    mpa = 4.2 * factory.random_mpa(nr_sites, local_dims, rank, normalized=True,
                                   randstate=rgen)
    norm = mp.norm(mpa.copy())
    if not normalize_if_applicable(mpa, canonicalize):
        return
    zero = factory.zero(nr_sites, local_dims, rank)
    choices = {'zero': (zero, 1), 'self': (mpa, 2), 'self2': (-2*mpa, -1)}
    add, factor = choices[add]

    msum = mpa + add
    assert_mpa_almost_equal(msum, factor * mpa, full=True)

    # Check that rank has increased (they exactly add)
    for dim1, dim2, sum_dim in zip(mpa.ranks, add.ranks, msum.ranks):
        assert dim1 + dim2 == sum_dim

    compr, overlap = call_compression(msum, comparg, rank, rgen)
    assert_almost_equal(overlap, (norm * factor)**2)
    assert_mpa_almost_equal(compr, factor * mpa, full=True)
    assert (np.array(compr.ranks) <= np.array(mpa.ranks)).all()
