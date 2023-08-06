# -*- coding: utf-8 -*-

"""TOOLS and FUNCTIONS for VEM JDE
Used in different versions of VEM
"""

import logging

from collections import OrderedDict

import numpy as np
import scipy

from numpy.matlib import repmat
from scipy.linalg import toeplitz
from scipy.optimize import fmin_slsqp, brentq, least_squares, leastsq
from scipy.stats import norm
from sympy.parsing.sympy_parser import parse_expr

from pyhrf.paradigm import restarize_events
from pyhrf.boldsynth.hrf import getCanoHRF


np.seterr(under="ignore")
logger = logging.getLogger(__name__)


# Tools
##############################################################

eps = np.spacing(1)


def mult(v1, v2):
    """Multiply two vectors.

    The first vector is made vertical and the second one horizontal. The result
    will be a matrix of size len(v1), len(v2).

    Parameters
    ----------
    v1 : ndarray
        unidimensional
    v2 : ndarray
        unidimensional

    Returns
    -------
    x : ndarray, shape (len(v1), len(v2))
    """

    v1 = v1.reshape(len(v1), 1)
    v2 = v2.reshape(1, len(v2))
    return v1.dot(v2)


def maximum(iterable):
    """Return the maximum and the indice of the maximum of an iterable.

    Parameters
    ----------
    iterable : iterable or numpy array

    Returns
    -------
    iter_max : the maximum
    iter_max_indice : the indice of the maximum
    """

    iter_max = max(iterable)

    try:
        # this is an iterable (tuple or list)
        iter_max_indice = iterable.index(iter_max)
    except AttributeError:
        # this is an numpy array
        iter_max_indice = iterable.argmax()

    return iter_max, iter_max_indice


def normpdf(x, mu, sigma):
    u = (x - mu) / np.abs(sigma)
    y = (1 / (np.sqrt(2 * np.pi) * np.abs(sigma))) * np.exp(-u * u / 2)
    return y


def polyFit(signal, tr, order, p):
    n = len(signal)
    ptp = np.dot(p.transpose(), p)
    invptp = np.linalg.inv(ptp)
    invptppt = np.dot(invptp, p.transpose())
    l = np.dot(invptppt, signal)
    return l


def drifts_coeffs_fit(signal, drift_basis):
    """# TODO

    Parameters
    ----------
    signal : ndarray, shape (nb_scans, nb_voxels)
    drift_basis : ndarray, shape (nb_scans, int)

    Returns
    -------
    drift_coeffs : ndarray, shape
    """

    return np.linalg.inv(drift_basis.T.dot(drift_basis)).dot(drift_basis.T).dot(signal)


def PolyMat(Nscans, paramLFD, tr):
    '''Build polynomial basis'''
    regressors = tr * np.arange(0, Nscans)
    timePower = np.arange(0, paramLFD + 1, dtype=int)
    regMat = np.zeros((len(regressors), paramLFD + 1), dtype=np.float64)

    for v in xrange(paramLFD + 1):
        regMat[:, v] = regressors[:]
    #tPowerMat = np.matlib.repmat(timePower, Nscans, 1)
    tPowerMat = repmat(timePower, Nscans, 1)
    lfdMat = np.power(regMat, tPowerMat)
    lfdMat = np.array(scipy.linalg.orth(lfdMat))
    return lfdMat


def poly_drifts_basis(nb_scans, param_lfd, tr):
    """Build polynomial drifts basis.

    Parameters
    ----------
    nb_scans : int
    param_lfd : int
        TODO
    tr : float

    Returns
    -------
    drifts_basis : ndarray, shape (nb_scans, K)
        K is determined by the scipy.linalg.orth function and corresponds to the
        effective rank of the matrix it is applied to (see function's docstring)
    """

    regressors = tr * np.arange(0, nb_scans)
    time_power = np.arange(0, param_lfd + 1, dtype=int)
    reg_mat = np.zeros((nb_scans, param_lfd + 1), dtype=np.float64)

    for v in xrange(param_lfd + 1):
        reg_mat[:, v] = regressors[:]

    drifts_basis = np.power(reg_mat, time_power)
    drifts_basis = np.array(scipy.linalg.orth(drifts_basis))

    return drifts_basis


def cosine_drifts_basis(nb_scans, param_lfd, tr):
    """Build cosine drifts basis.

    Parameters
    ----------
    nb_scans : int
    param_lfd : int
        TODO
    tr : float

    Returns
    -------
    drifts_basis : ndarray, shape (nb_scans, K)
        K is determined by the scipy.linalg.orth function and corresponds to the
        effective rank of the matrix it is applied to (see function's docstring)
    """

    fct_nb = int(np.fix(2. * (nb_scans * tr) / param_lfd + 1.))  # +1 stands for the mean/cst regressor

    drifts_basis = np.zeros((nb_scans, fct_nb), dtype=float)
    drifts_basis[:, 0] = np.ones(nb_scans, dtype=float) / np.sqrt(nb_scans)

    amplitude = np.sqrt(2. / nb_scans)
    n = np.arange(0, nb_scans)
    omega = np.pi * (2. * n + 1.) / (2. * nb_scans)

    samples = np.arange(1, fct_nb - 1)
    for k in samples:
        drifts_basis[:, k] = amplitude * np.cos(omega*k)

    drifts_basis = np.array(scipy.linalg.orth(drifts_basis))

    return drifts_basis


def covariance_matrix(order, D, dt):
    D2 = buildFiniteDiffMatrix_s(order, D)
    R = np.dot(D2, D2) / pow(dt, 2 * order)
    return R


def roc_curve(dvals, labels, rocN=None, normalize=True):
    """
    Compute ROC curve coordinates and area

    - `dvals`  - a list with the decision values of the classifier
    - `labels` - list with class labels, \in {0, 1}

    returns (FP coordinates, TP coordinates, AUC )
    """
    if rocN is not None and rocN < 1:
        rocN = int(rocN * np.sum(np.not_equal(labels, 1)))

    TP = 0.0  # current number of true positives
    FP = 0.0  # current number of false positives

    fpc = [0.0]  # fp coordinates
    tpc = [0.0]  # tp coordinates
    dv_prev = - np.inf  # previous decision value
    TP_prev = 0.0
    FP_prev = 0.0
    area = 0.0

    #num_pos = labels.count(1)  # num pos labels np.sum(labels)
    #num_neg = labels.count(0)  # num neg labels np.prod(labels.shape)-num_pos

    #if num_pos == 0 or num_pos == len(labels):
    #    raise ValueError, "There must be at least one example from each class"

    # sort decision values from highest to lowest
    indices = np.argsort(dvals)[::-1]

    for idx in indices:
        # increment associated TP/FP count
        if labels[idx] == 1:
            TP += 1.
        else:
            FP += 1.
            if rocN is not None and FP == rocN:
                break
        # Average points with common decision values
        # by not adding a coordinate until all
        # have been processed
        if dvals[idx] != dv_prev:
            if len(fpc) > 0 and FP == fpc[-1]:
                tpc[-1] = TP
            else:
                fpc.append(FP)
                tpc.append(TP)
            dv_prev = dvals[idx]
            area += _trap_area((FP_prev, TP_prev), (FP, TP))
            FP_prev = FP
            TP_prev = TP

    #area += _trap_area( ( FP, TP ), ( FP_prev, TP_prev ) )
    #fpc.append( FP  )
    #tpc.append( TP )
    if normalize:
        fpc = [np.float64(x) / FP for x in fpc]
        if TP > 0:
            tpc = [np.float64(x) / TP for x in tpc]
        if area > 0:
            area /= (TP * FP)

    return fpc, tpc, area


def fit_hrf_two_gammas(hrf_mean, dt, duration):
    """Fits the estimated HRF to the standard two gammas model.

    Parameters
    ----------
    dt: float
    duration: float
    hrf_mean : ndarray, shape (hrf_len,)

    Returns
    -------
    delay_of_response : float
    delay_of_undershoot : float
    dispersion_of_response : float
    dispersion_of_undershoot : float
    ratio_resp_under : float
    delay : float
    """

    def two_gamma_hrf(params):

        delay_of_response = params[0]
        delay_of_undershoot = params[1]
        dispersion_of_response = params[2]
        dispersion_of_undershoot = params[3]
        ratio_resp_under = params[4]
        delay = params[5]

        canonical_hrf = getCanoHRF(duration, dt, True, delay_of_response,
                                   delay_of_undershoot, dispersion_of_response,
                                   dispersion_of_undershoot, ratio_resp_under, delay)[1]

        return canonical_hrf - hrf_mean

    x0 = np.asarray([6., 16., 1., 1., 6., 0.])
    try:
        res = least_squares(two_gamma_hrf, x0,
                            bounds=(np.zeros(6), duration + np.zeros(6))).x
    except ImportError as e:
        res = leastsq(two_gamma_hrf, x0).x

    return res


def compute_mat_X_2(nbscans, tr, lhrf, dt, onsets, durations=None):
    if durations is None:  # assume spiked stimuli
        durations = np.zeros_like(onsets)
    osf = tr / dt  # over-sampling factor
    # construction will only work if dt is a multiple of tr
    if int(osf) != osf:
        raise Exception('OSF (%f) is not an integer' % osf)

    x = np.zeros((nbscans, lhrf), dtype=float)
    tmax = nbscans * tr  # total session duration
    lgt = int((nbscans + 2) * osf)  # nb of scans if tr=dt
    paradigm_bins = restarize_events(onsets, durations, dt, tmax)
    firstcol = np.concatenate(
        (paradigm_bins, np.zeros(lgt - len(paradigm_bins))))
    firstrow = np.concatenate(
        ([paradigm_bins[0]], np.zeros(lhrf - 1, dtype=int)))
    x_tmp = np.array(toeplitz(firstcol, firstrow), dtype=int)
    #x_tmp2 = np.zeros_like(x_tmp)
    #for i in xrange(0, x_tmp.shape[1], osf):
    #    x_tmp2[:, i] = x_tmp[:, i]
    os_indexes = [(np.arange(nbscans) * osf).astype(int)]
    x = x_tmp[os_indexes]
    return x


def buildFiniteDiffMatrix(order, size, regularization=None):
    """Build the finite difference matrix used for the hrf regularization prior.

    Parameters
    ----------
    order : int
        difference order (see numpy.diff function)
    size : int
        size of the matrix
    regularization : array like, optional
        one dimensional vector of factors used for regularizing the hrf

    Returns
    -------
    diffMat : ndarray, shape (size, size)
        the finite difference matrix"""

    a = np.diff(np.concatenate((np.zeros(order), [1], np.zeros(order))),
                n=order)
    b = a[len(a)//2:]
    diffMat = toeplitz(np.concatenate((b, np.zeros(size - len(b)))))

    if regularization is not None:
        regularization = np.array(regularization)
        if regularization.shape != (size,):
            raise Exception("regularization shape ({}) must be (size,) ({},)".format(regularization.shape, size))
        if not all(regularization > 0):
            raise Exception("All values of regularization must be stricly positive")
        diffMat = (np.triu(diffMat, 1) * regularization +
                   np.tril(diffMat, -1) * regularization[:, np.newaxis] +
                   np.diag(diffMat.diagonal() * regularization))
        # diffMat = (np.triu(diffMat, 1) + np.tril(diffMat, -1) +
                   # np.diag(diffMat.diagonal() * regularization))
        # diffMat = diffMat * regularization

    return diffMat


def create_conditions(onsets, durations, nb_conditions, nb_scans, hrf_len, tr, dt):
    """Generate the occurrences matrix.

    Parameters
    ----------
    onsets : dict
        dictionary of onsets for each condition.
    durations : dict
        dictionary of durations for each condition.
    nb_conditions : int
        number of experimental conditions.
    nb_scans : int
        number of scans.
    hrf_len : int
        number of points of the hrf
    tr : float
        time of repetition
    dt : float
        hrf temporal precision

    Returns
    -------
    X : dict
        dictionary of the occurence matrix
    occurence_matrix : ndarray
    condition_names : list
    """
    condition_names = []
    matrix_x = OrderedDict()
    occurrence_matrix = np.zeros((nb_conditions, nb_scans, hrf_len), dtype=np.int32)

    for nc, (condition, onset) in enumerate(onsets.iteritems()):
        duration = np.asarray(durations[condition]).flatten()
        mat_x_2 = compute_mat_X_2(nb_scans, tr, hrf_len, dt, onset, durations=duration)

        matrix_x[condition] = mat_x_2
        occurrence_matrix[nc, :, :] = mat_x_2

        condition_names.append(condition)

    return matrix_x, occurrence_matrix, condition_names


def create_neighbours(graph):
    """Transforms the graph list in ndarray. This is for performances purposes. Sets the empty neighbours to -1.

    Parameters
    ----------
    graph : list of ndarray
        each graph[i] represents the list of neighbours of the ith voxel

    Returns
    -------
    neighbours_indexes : ndarray
    """

    max_neighbours = len(max(graph, key=len))

    neighbours_indexes = [np.concatenate((arr, np.zeros(max_neighbours-len(arr))-1))
                          for arr in graph]

    return np.asarray(neighbours_indexes, dtype=int)


def _trap_area(p1, p2):
    """
    Calculate the area of the trapezoid defined by points
    p1 and p2

    `p1` - left side of the trapezoid
    `p2` - right side of the trapezoid
    """
    base = abs(p2[0] - p1[0])
    avg_ht = (p1[1] + p2[1]) / 2.0

    return base * avg_ht


def roc_curve(dvals, labels, rocN=None, normalize=True):
    """
    Compute ROC curve coordinates and area

    - `dvals`  - a list with the decision values of the classifier
    - `labels` - list with class labels, \in {0, 1}

    returns (FP coordinates, TP coordinates, AUC )
    """
    if rocN is not None and rocN < 1:
        rocN = int(rocN * np.sum(np.not_equal(labels, 1)))

    TP = 0.0  # current number of true positives
    FP = 0.0  # current number of false positives

    fpc = [0.0]  # fp coordinates
    tpc = [0.0]  # tp coordinates
    dv_prev = - np.inf  # previous decision value
    TP_prev = 0.0
    FP_prev = 0.0
    area = 0.0

    # num_pos = labels.count(1)  # num pos labels np.sum(labels)
    # num_neg = labels.count(0)  # num neg labels np.prod(labels.shape)-num_pos

    # if num_pos == 0 or num_pos == len(labels):
    #    raise ValueError, "There must be at least one example from each class"

    # sort decision values from highest to lowest
    indices = np.argsort(dvals)[::-1]

    for idx in indices:
        # increment associated TP/FP count
        if labels[idx] == 1:
            TP += 1.
        else:
            FP += 1.
            if rocN is not None and FP == rocN:
                break
        # Average points with common decision values
        # by not adding a coordinate until all
        # have been processed
        if dvals[idx] != dv_prev:
            if len(fpc) > 0 and FP == fpc[-1]:
                tpc[-1] = TP
            else:
                fpc.append(FP)
                tpc.append(TP)
            dv_prev = dvals[idx]
            area += _trap_area((FP_prev, TP_prev), (FP, TP))
            FP_prev = FP
            TP_prev = TP

    #area += _trap_area( ( FP, TP ), ( FP_prev, TP_prev ) )
    #fpc.append( FP  )
    #tpc.append( TP )
    if normalize:
        fpc = [np.float64(x) / FP for x in fpc]
        if TP > 0:
            tpc = [np.float64(x) / TP for x in tpc]
        if area > 0:
            area /= (TP * FP)

    return fpc, tpc, area


def sum_over_neighbours(neighbours_indexes, array_to_sum):
    """Sums the `array_to_sum` over the neighbours in the graph."""

    if not neighbours_indexes.size:
        return array_to_sum

    if neighbours_indexes.max() > array_to_sum.shape[-1] - 1:
        raise Exception("Can't sum over neighbours. Please check dimensions")

    array_cat_zero = np.concatenate((array_to_sum,
                                     np.zeros(array_to_sum.shape[:-1]+(1,), dtype=array_to_sum.dtype)),
                                    axis=-1)

    return array_cat_zero[..., neighbours_indexes].sum(axis=-1)


def contrasts_mean_var_classes(contrasts, condition_names, nrls_mean, nrls_covar, nrls_class_mean, nrls_class_var,
                               nb_contrasts, nb_classes, nb_voxels):
    """Computes the contrasts nrls from the conditions nrls and the mean and variance of the gaussian classes of the
    contrasts (in the cases of all inactive conditions and all active conditions).

    Parameters
    ----------
    contrasts : OrderedDict
        TODO.
    condition_names : list
        TODO.
    nrls_mean : ndarray, shape (nb_voxels, nb_conditions)
        TODO.
    nrls_covar : ndarray, shape (nb_conditions, nb_conditions, nb_voxels)
        TODO.
    nrls_class_mean : ndarray, shape (nb_conditions, nb_classes)
        TODO.
    nrls_class_var : ndarray, shape (nb_conditions, nb_classes)
        TODO.
    nb_contrasts : int
    nb_classes : int
    nb_voxels : int

    Returns
    -------
    contrasts_mean : ndarray, shape (nb_voxels, nb_contrasts)
    contrasts_var : ndarray, shape (nb_voxels, nb_contrasts)
    contrasts_class_mean : ndarray, shape (nb_contrasts, nb_classes)
    contrasts_class_var : ndarray, shape (nb_contrasts, nb_classes)
    """

    contrasts_mean = np.zeros((nb_voxels, nb_contrasts))
    contrasts_var = np.zeros((nb_voxels, nb_contrasts))
    contrasts_class_mean = np.zeros((nb_contrasts, nb_classes))
    contrasts_class_var = np.zeros((nb_contrasts, nb_classes))

    for i, contrast_name in enumerate(contrasts):
        parsed_contrast = parse_expr(contrasts[contrast_name])

        for condition_nb, condition_name in enumerate(condition_names):
            coeff = parsed_contrast.coeff(condition_name)

            if coeff:
                contrasts_mean[:, i] += float(coeff) * nrls_mean[:, condition_nb]
                contrasts_var[:, i] += float(coeff)**2 * nrls_covar[condition_nb, condition_nb, :]
                contrasts_class_mean[i, 1] += float(coeff) * nrls_class_mean[condition_nb, 1]
                contrasts_class_var[i, :] += float(coeff)**2 * nrls_class_var[condition_nb, :]

    return contrasts_mean, contrasts_var, contrasts_class_mean, contrasts_class_var


def ppm_contrasts(contrasts_mean, contrasts_var, contrasts_class_mean,
                  contrasts_class_var, threshold_a="std_inact", threshold_g=0.95):
    """Computes the ppm for the given contrast using either the standard deviation
    of the "all inactive conditions" class gaussian (default) or the intersection
    of the [all inactive conditions] and [all active conditions] classes
    gaussians as threshold for the PPM_a and 0.95 (default) for the PPM_g.
    Be carefull, this computation considers the mean of the inactive class as zero.

    Parameters
    ----------
    contrasts_mean : ndarray, shape (nb_voxels, nb_contrasts)
    contrasts_var : ndarray, shape (nb_voxels, nb_contrasts)
    contrasts_class_mean : ndarray, shape (nb_contrasts, nb_classes)
    contrasts_class_var : ndarray, shape (nb_contrasts, nb_classes)
    threshold_a : str, optional
        if "std_inact" (default) uses the standard deviation of the
        [all inactive conditions] gaussian class as PPM_a threshold, if "intersect"
        uses the intersection of the [all inactive/all active conditions]
        gaussian classes
    threshold_g : float, optional
        the threshold of the PPM_g

    Returns
    -------
    ppm_a_contrasts : ndarray, shape (nb_voxels, nb_contrasts)
    ppm_g_contrasts : ndarray, shape (nb_voxels, nb_contrasts)
    """

    import warnings
    warnings.warn(
        "The ppm_contrasts function is deprecated, use ppms_computation instead",
        DeprecationWarning
    )

    return ppms_computation(contrasts_mean, contrasts_var, contrasts_class_mean,
                            contrasts_class_var, threshold_a, threshold_g)


def ppms_computation(elements_mean, elements_var, class_mean, class_var, threshold_a="std_inact", threshold_g=0.9):
    r"""Considering the `elements_mean` and `elements_var` from a gaussian distribution, commutes the posterior
    probability maps considering for the alpha threshold, either the standard deviation of the
    [all inactive conditions] gaussian class or the intersection of the [all (in)active conditions] gaussian classes;
    and for the gamma threshold 0.9 (default).

    The posterior probability maps (PPM) per experimental condition is computed as
    :math:`p(a^{m}_{j} > \delta | y_{j}) > \alpha`. Note that we have to thresholds to set. We set :math:`\delta` to get
    a posterior probability distribution, and :math:`\alpha` is the threshold that we set to see a certain level of
    significance. As default, we chose a threshold :math:`\delta` for each experimental condition *m* as the
    intersection of the two Gaussian densities of the Gaussian Mixture Model (GMM) that represent active and non-active
    voxel.

    .. math::

        \frac{(\delta - \mu^{m}_{1})^{2}}{v^{m}_{1}} - \frac{(\delta - \mu^{m}_{0})^{2}}{v^{m}_{0}} =
        \log\left( \frac{v^{m}_{1}}{v^{m}_{0}} \right)

    :math:`\mu^{m}_{i}` and :math:`v^{m}_{i}` being the parameters of the GMM in :math:`a^{m}_{j}` corresponding to
    active (*i=0*) and non-active (*i=1*) voxels for experimental condition *m*.

    .. math::

        \delta = \frac{\mu_{1}\sigma_{0}^{2} \pm \sigma_{0}\sigma_{1}\sqrt{\mu^{2}_{1} + 2 \left(\sigma^{2}_{0} -
        \sigma^{2}_{1} \right) \log \left( \frac{\sigma_{0}}{\sigma_{1}} \right)}}{\sigma^{2}_{0} - \sigma^{2}_{1}}

    **Be careful, this computation considers the mean of the inactive class as zero.**

    Notes
    -----
    nb_elements refers either to the number of contrasts (for the PPMs contrasts computation) or for the number of
    conditions (for the PPMs nrls computation).

    Parameters
    ----------
    elements_mean : ndarray, shape (nb_voxels, nb_elements)
    elements_var : ndarray, shape (nb_voxels, nb_elements)
    class_mean : ndarray, shape (nb_elements, nb_classes)
    class_var : ndarray, shape (nb_elements, nb_classes)
    threshold_a : str, optional
        if "std_inact" (default) uses the standard deviation of the [all inactive conditions] gaussian class as PPM_a
        threshold. If "intersect" uses the intersection of the [all inactive/all active conditions] gaussian classes.
    threshold_g : float, optional
        the threshold of the PPM_g

    Returns
    -------
    ppm_a: ndarray, shape (nb_voxels, nb_elements)
    ppm_g: ndarray, shape (nb_voxels, nb_elements)
    """

    if threshold_a == "std_inact":
        thresh = np.sqrt(class_var[:, 0])  # standard deviation of the [all inactive conditions]

    elif threshold_a == "intersect":  # intersection of the [all inactive/all active conditions]
        intersect1 = class_mean[:, 1] * class_var[:, 0]

        class_sd = np.sqrt(class_var)  # standard deviation
        class_var_diff = class_var[:, 0] - class_var[:, 1]  # sigma^2_0 - sigma^2_1

        intersect2 = class_sd.prod(axis=1) * np.sqrt(
            class_mean[:, 1]**2 +
            2 * class_var_diff * np.log(class_sd[:, 0] / class_sd[:, 1])
        )

        threshs = np.concatenate(((intersect1 - intersect2)[:, np.newaxis],
                                  (intersect1 + intersect2)[:, np.newaxis]),
                                 axis=1) / class_var_diff[:, np.newaxis]

        mask_mean = (threshs > 0) & (threshs < class_mean[:, 1][:, np.newaxis])
        mask = (mask_mean |
                (~mask_mean.any(axis=1)[:, np.newaxis] & (threshs == threshs.max(axis=1)[:, np.newaxis])))

        thresh = threshs[mask]

        if len(thresh) < len(threshs):
            logger.warning("The gaussians do not have one intersection between means. Choosing the highest")
            thresh = threshs.max(axis=1)
            thresh = np.concatenate((thresh[:, np.newaxis], class_var[:, 0][:, np.newaxis]), axis=1).max(axis=1)

    else:
        raise NotImplemented

    ppm_a = norm.sf(thresh, elements_mean, elements_var**.5)
    ppm_g = norm.isf(threshold_g, elements_mean, elements_var**.5)

    return ppm_a, ppm_g


def norm1_constraint(function, variance):
    """Returns the function constrained with optimization strategy.

    Parameters
    ----------
    function : array_like
        function to optimize under norm1 constraint
    variance : array_like
        variance of the `function`, must be the same size

    Returns
    -------
    optimized_function : numpy array

    Raises
    ------
    ValueError
        If `len(variance) != len(function)`

    """

    variance_inv = np.linalg.inv(variance)

    current_level = logger.getEffectiveLevel()
    if current_level >= logging.WARNING:
        disp = 0
    elif current_level >= logging.INFO:
        disp = 1
    else:
        disp = 2

    def objective_function(fct):
        """Function to minimize"""
        diff = fct - function
        return np.dot(np.dot(diff.T, variance_inv), diff)

    def norm1_constraint_equation(fct):
        """Norm2(fct) == 1"""
        return np.linalg.norm(fct, 2) - 1

    minimized_function = fmin_slsqp(objective_function, function,
                                    eqcons=[norm1_constraint_equation],
                                    bounds=[(None, None)] * len(function),
                                    disp=disp)

    return minimized_function


# Expectation functions
##############################################################


def nrls_expectation(hrf_mean, nrls_mean, occurence_matrix, noise_struct,
                     labels_proba, nrls_class_mean, nrls_class_var,
                     nb_conditions, y_tilde, nrls_covar,
                     hrf_covar, noise_var):
    r"""Computes the VE-A step of the JDE-VEM algorithm.

    .. math::

       \Sigma^{(r)}_{A_{j}} &= \left( \sum\limits^{I}_{i=1} \Delta_{ij} + \widetilde{H}_{j} \right)^{-1} \\
       m^{(r)}_{A_{j}} &= \Sigma^{(r)}_{A{j}} \left( \sum\limits^{I}_{i=1} \Delta_{ij} \mu_{i}^{(r-1)} + \widetilde{G}^{t}\Gamma_{j}^{(r-1)}\left(y_{j} - P\ell^{(r-1)} \right)\right)

    where:

    The mth column of :math:`\widetilde{G}` is denote by :math:`\widetilde{g}_{m}  = X_{m}m^{(r)}_{H} \in \mathbb{R}^{N}`

    .. math::

        \Delta_{ij} &= \mathrm{diag}_{M}\left[\frac{q^{(r-1)}_{Z_{mj}}(i)}{\sigma^{2(r)}_{mi}}\right] \\

        \widetilde{H}_{j} &= \widetilde{g}^{t}_{m} \Gamma^{(r-1)}_{j} \widetilde{g}_{m'} + \mathrm{tr}\left( \Gamma^{(r-1)}_{j}X_{m} \Sigma^{(r)}_{H}X^{t}_{m'} \right)


    Parameters
    ----------
    hrf_mean : ndarray, shape (hrf_len,)
    nrls_mean : ndarray, shape (nb_voxels, nb_conditions)
    occurence_matrix : ndarray, shape (nb_conditions, nb_scans, hrf_len)
    noise_struct : ndarray, shape (nb_scans, nb_scans)
    labels_proba : ndarray, shape (nb_conditions, nb_classes, nb_voxels)
    nrls_class_mean : ndarray, shape (nb_conditions, nb_classes)
    nrls_class_var : ndarray, shape (nb_conditions, nb_classes)
    nb_conditions : int
    y_tilde : ndarray, shape (nb_scans, nb_voxels)
        BOLD data minus drifts
    nrls_covar : ndarray, shape (nb_conditions, nb_conditions, nb_voxels)
    hrf_covar : ndarray, shape (hrf_len, hrf_len)
    noise_var : ndarray, shape (nb_voxels,)

    Returns
    -------
    nrls_mean : ndarray, shape (nb_voxels, nb_conditions)
    nrls_covar : ndarray, shape (nb_conditions, nb_conditions, nb_voxels)
    """

    # Pre-compute some matrix products
    om_hm_prod = occurence_matrix.dot(hrf_mean).T  # matrix G made of columns g_m = X_m * m_H
    om_hc_prod = occurence_matrix.dot(hrf_covar.T)
    ns_om_prod = np.tensordot(noise_struct, occurence_matrix, axes=(1, 1))

    # first term of nrls_covar: p_q / sigma_h
    delta_k = labels_proba / nrls_class_var[:, :, np.newaxis]
    delta = delta_k.sum(axis=1)  # sum across classes K

    # second term of nrls_covar: G.T*Gamma*G + tr(Gamma*X*Sigma_H*X.T)
    h_tilde = om_hm_prod.T.dot(noise_struct).dot(om_hm_prod)[..., np.newaxis]
    h_tilde += np.einsum('ijk, jlk', om_hc_prod, ns_om_prod)[..., np.newaxis]
    h_tilde = h_tilde / noise_var

    # nrls_covar computation
    nrls_covar = h_tilde.transpose(2, 0, 1) + delta.T[:, np.newaxis, :] * np.eye(nb_conditions)
    nrls_covar = np.linalg.inv(nrls_covar).transpose(1, 2, 0)

    # first term of nrls_mean: G.T*Gamma*y_tilde
    ns_yt_prod = noise_struct.dot(y_tilde).T
    x_tilde = ns_yt_prod.dot(om_hm_prod) / noise_var[:, np.newaxis]

    # second term of nrls_mean
    x_tilde += (delta_k * nrls_class_mean[:, :, np.newaxis]).sum(axis=1).T

    # dot product across voxels of nrls_covar and x_tilde
    nrls_mean = np.einsum('ijk,kj->ki', nrls_covar, x_tilde)

    return nrls_mean, nrls_covar


def hrf_expectation(nrls_covar, nrls_mean, occurence_matrix, noise_struct, hrf_regu_prior_inv, sigmaH, nb_voxels,
                    y_tilde, noise_var, prior_mean_term=0., prior_cov_term=0.):

    r"""Computes the VE-H step of the JDE-VEM algorithm.

    .. math::

        m^{(r)}_{H}  &= \Sigma^{(r)}_{H} \left( \sum\limits_{i \in \mathcal{P}} \widetilde{S}_{i}^{t}
        \widetilde{y}^{(r)}_{i} \right) \\

        \left(\Sigma^{(r)}_{H}\right)^{-1} &= \frac{\mathbf{R}^{-1}}{\sigma^{2(r)}_{h}} + \sum\limits_{i\in
        \mathcal{P}} \left( \sum\limits_{m,m'} \sigma^{(r-1)}_{A_{mi}A_{m'i}} \mathbf{X}^{t}_{m} \Gamma^{(r)}_{i}
        \mathbf{X}_{m'} + \widetilde{S}_{i}^{t} \Gamma^{(r)}_{i} \widetilde{S}_{i}\right)

    where

    .. math::

        \widetilde{S}_{i} &= \sum\limits^{M}_{m=1} m^{(r-1)}_{A_{mi}}\mathbf{X}_{m} \\

        \widetilde{y}^{(r)}_{i} &= \Gamma^{(r)}_{i} \left( y_{i} - \mathbf{P}\ell^{(r)}_{i} \right)


    Here, :math:`m^{(r-1)}_{A_{mi}}` and :math:`\sigma^{(r-1)}_{A_{mi}A_{m'i}}` denote the
    :math:`m^{th}` and :math:`(m,m')^{th}` entries of the mean vector and covariance matrix of the current
    :math:`q^{(r-1)}_{A_{i}}`, respectively.

    Parameters
    ----------
    nrls_covar : ndarray, shape (nb_conditions, nb_conditions, nb_voxels)
    nrls_mean : ndarray, shape (nb_voxels, nb_conditions)
    occurence_matrix : ndarray, shape (nb_conditions, nb_scans, hrf_len)
    noise_struct : ndarray, shape (nb_scans, nb_scans)
    hrf_regu_prior_inv : ndarray, shape (hrf_len, hrf_len)
        inverse of the hrf regularization prior matrix `R`
    sigmaH : float
    nb_voxels : int
    y_tilde : ndarray, shape (nb_scans, nb_voxels)
    noise_var : ndarray, shape (nb_voxels,)
    prior_mean_term : float, optional
    prior_cov_term : float, optional

    Returns
    -------
    hrf_mean : ndarray, shape (hrf_len,)
    hrf_covar : ndarray, shape (hrf_len, hrf_len)
    """

    # Pre-compute some matrix products
    nm_om_prod = np.tensordot(nrls_mean, occurence_matrix, axes=(1, 0))
    ns_om_prod = np.tensordot(noise_struct, occurence_matrix, axes=(1, 1))
    om_ns_om_prod = np.tensordot(occurence_matrix.T, ns_om_prod, axes=(1, 0))
    cov_noise = np.maximum(noise_var, eps)[:, np.newaxis, np.newaxis]
    nm_om_ns_prod = np.tensordot(nm_om_prod, noise_struct, axes=(1, 0)) / cov_noise

    # Sigma_H computation
    # first term: part of the prior -> R^-1 / sigmaH
    hrf_covar_inv = hrf_regu_prior_inv / sigmaH

    # second term: sum_{m, m'} (Sigma_a(m,m') * X_m.T * noise_struct_i * X_m')
    hrf_covar_inv += (np.einsum('ijk,lijm->klm', nrls_covar, om_ns_om_prod) / cov_noise).sum(0)

    # third term: let S=sum_m (m_a * X_m), then S.T * noise_struct_i * S
    for i in xrange(nb_voxels):
        hrf_covar_inv += nm_om_ns_prod[i, :, :].dot(nm_om_prod[i, :, :])

    # forth term (depends on prior type): we sum the term that corresponds to the prior
    hrf_covar_inv += prior_cov_term

    # Sigma_H
    hrf_covar = np.linalg.inv(hrf_covar_inv)

    # m_H computation: S.T * noise_struct_i * y_tilde
    y_bar_tilde = np.einsum('ijk,ki->j', nm_om_ns_prod, y_tilde)

    # we sum the term that corresponds to the prior
    y_bar_tilde += prior_mean_term

    # m_H = Sigma_H * y_bar_tilde
    hrf_mean = hrf_covar.dot(y_bar_tilde)

    return hrf_mean, hrf_covar


def labels_expectation(nrls_covar, nrls_mean, nrls_class_var, nrls_class_mean, beta, labels_proba, neighbours_indexes,
                       nb_conditions, nb_classes, nb_voxels=None, parallel=True, nans_init=False):
    r"""Computes the E-Z (or E-Q) step of the JDE-VEM algorithm.

    Using the *mean-field* approximation,
    :math:`\widetilde{p}^{(r)}_{Q^{m}}(q^{m})` is approximated by a factorized density
    :math:`\widetilde{p}^{(r)}_{Q^{m}}(q^{m})=
    \prod\limits_{j \in \mathcal{P}_{\gamma}}\widetilde{p}^{(r)}_{Q^{m}_{j}}(q^{m}_{j})` such that if
    :math:`q^{m}_{j} = i`, then :math:`\widetilde{p}^{(r)}_{Q^{m}_{j}}(i) \propto \mathcal{N} \left(m^{(r)}_{A^{m}_{j}};
    \mu^{(r-1)}_{im}, v^{(r-1)}_{im} \right) f\left(q^{m}_{j} = i \,|\, \widetilde{q}^{m}_{\sim j};
    \beta^{(r-1)}_{m}, v^{(r-1)}_{m} \right)` where :math:`\widetilde{q}^{m}` is a particular configuration of
    :math:`q^{m}` updated at each iteration according to a specific scheme and

    .. math::

        f\left( q^{m}_{j} \,|\, \widetilde{q}^{m}_{\sim j}; \beta^{(r-1)}_{m}, v^{(r-1)}_{m} \right) \propto
        \exp\left(\alpha^{m(r)}_{j}(q^{m}_{j}) + \beta^{(r-1)}_{m}\sum\limits_{k \sim j}
        I\left(\widetilde{q}^{m}_{k} = q^{m}_{j}\right) \right)

    where

    .. math::

        \left\{ \alpha^{m(r)}_{j} = \left( -v^{(r)}_{A_{j}^{m}A^{m''}_{j}} \left[ \frac{1}{v^{(r-1)}_{0m}},
        \frac{1}{v^{(r-1)}_{1m}} \right] \right)^{t}, j \in \mathcal{P}_{\gamma}\right\}


    and :math:`v^{(r)}_{A_{j}^{m}A^{m''}_{j}}` denotes the :math:`(m,m')` entries of the covariance matrix
    :math:`\Sigma^{(r)}_{A_{j}}`


    Notes
    -----
        The *mean-field fixed point* equation is defined in:

            Celeux, G., Forbes, F., & Peyrard, N. (2003). EM procedures using mean field-like approximations for
            Markov model-based image segmentation. Pattern Recognition, 36(1), 131–144.
            https://doi.org/10.1016/S0031-3203(02)00027-4

    Parameters
    ----------
    nrls_covar : ndarray, shape (nb_conditions, nb_conditions, nb_voxels)
    nrls_mean : ndarray, shape (nb_voxels, nb_conditions)
    nrls_class_var : ndarray, shape (nb_conditions, nb_classes)
    nrls_class_mean : ndarray, shape (nb_conditions, nb_classes)
    beta : ndarray, shape
    labels_proba : ndarray, shape (nb_conditions, nb_classes, nb_voxels)
    neighbours_indexes : ndarray, shape (nb_voxels, max(len(a) for a in graph))
        This is the version of graph array where arrays from graph smaller than
        the maximum ones are filled with -1
    nb_conditions : int
    nb_classes : int
    nb_voxels : int
    parallel : bool
    nans_init : bool

    Returns
    -------
    labels_proba : ndarray, shape (nb_conditions, nb_classes, nb_voxels)
    """

    alpha = (-0.5 * np.diagonal(nrls_covar)[:, :, np.newaxis] / nrls_class_var[np.newaxis, :, :]).transpose(1, 2, 0)
    alpha -= alpha.mean(axis=2)[:, :, np.newaxis]

    gauss = normpdf(nrls_mean[..., np.newaxis], nrls_class_mean, np.sqrt(nrls_class_var)).transpose(1, 2, 0)

    # update z_tilde (q_tilde), i.e., the quantity which is involved in the a priori Potts field
    # (by solving for the mean-field fixed point Equation)
    if not parallel and nb_voxels:
        energy = np.zeros_like(labels_proba)
        local_energy = np.zeros_like(labels_proba)

        for vox in xrange(nb_voxels):
            local_energy[:, :, vox] = sum_over_neighbours(neighbours_indexes[vox, :],
                                                          beta[..., np.newaxis, np.newaxis] * labels_proba)

            energy[:, :, vox] = alpha[:, :, vox] + local_energy[:, :, vox]

            labels_proba[:, :, vox] = np.exp(energy[:, :, vox]) * gauss[:, :, vox]
            labels_proba[:, :, vox] = labels_proba[:, :, vox] / labels_proba[:, :, vox].sum(axis=1)[:, np.newaxis]

    else:
        if not parallel:
            logger.warning("Could not use asynchronous expectation. Please provide the nb_voxels parameter")

        local_energy = sum_over_neighbours(neighbours_indexes,
                                           beta[..., np.newaxis, np.newaxis] * labels_proba)
        energy = alpha + local_energy

        if nans_init:
            labels_proba_nans = np.ones_like(labels_proba) / nb_classes
        else:
            labels_proba_nans = labels_proba.copy()

        labels_proba = np.exp(energy) * gauss

        # Remove NaNs and Infs (TODO: check for sequential mode)
        if (labels_proba.sum(axis=1) == 0).any():
            mask = labels_proba.sum(axis=1)[:, np.newaxis, :].repeat(2, axis=1) == 0
            labels_proba[mask] = labels_proba_nans[mask]

        if np.isinf(labels_proba.sum(axis=1)).any():
            mask = np.isinf(labels_proba.sum(axis=1))[:, np.newaxis, :].repeat(1, axis=1)
            labels_proba[mask] = labels_proba_nans[mask]

        labels_proba = labels_proba / labels_proba.sum(axis=1)[:, np.newaxis, :]

    return labels_proba


# Maximization functions
##############################################################

def maximization_class_proba(labels_proba, nrls_mean, nrls_covar):
    r"""Computes the M-(mu, sigma) step of the JDE-VEM algorithm.

    .. math::

        \bar{q}^{(r)}_{mk}   & = \sum \limits_{i \in \mathcal{P}} q^{(r)}_{Z_{mi}} (k) \\
        \mu^{(r+1)}_{mk}     & = \frac{\sum \limits_{i \in \mathcal{P}} q^{(r)}_{Z_{mi}} (k) m^{(r)}_{A_{mi}}}{\bar{q}^{(r)}_{mk}} \\
        \sigma^{2(r+1)}_{mk} &= \frac{\sum \limits_{i \in \mathcal{P}} q^{(r)}_{Z_{mi}} (k) \left(\left(m^{(r)}_{A_{mi}} - \mu^{(r+1)}_{mk}\right)^{2} + \sigma^{(r)}_{A_{im}A_{im}} \right)}{\bar{q}^{(r)}_{mk}}

    """

    labels_proba_sum = labels_proba.sum(axis=2)

    nrls_class_mean = np.zeros_like(labels_proba_sum)
    nrls_class_mean[:, 1] = (labels_proba[:, 1, :] * nrls_mean.T).sum(axis=1) / labels_proba_sum[:, 1]

    nm_minus_ncm = (nrls_mean[..., np.newaxis] - nrls_class_mean[np.newaxis, ...]).transpose(1, 2, 0)**2

    nrls_covar_diag = np.diagonal(nrls_covar).T

    nrls_class_var = (labels_proba * (nm_minus_ncm + nrls_covar_diag[:, np.newaxis, :])).sum(axis=2) / labels_proba_sum

    return nrls_class_mean, nrls_class_var


def maximization_drift_coeffs(data, nrls_mean, occurence_matrix, hrf_mean, noise_struct, drift_basis):
    r"""Computes the M-(l, Gamma) step of the JDE-VEM algorithm. In the AR(1) case:

    .. math::

        \ell^{(r)}_{j} = \left( \bm{P}^{\intercal} \bm{\Lambda}^{(r)}_{j} \bm{P} \right)^{-1} \bm{P}^{\intercal} \bm{\Lambda}^{(r)}_{j} \left( y_{j} - \bm{\widetilde{S}}_{j} m^{(r)}_{H} \right)

    """

    # Precomputations
    db_ns_db = drift_basis.T.dot(noise_struct).dot(drift_basis)

    data_s = data - nrls_mean.dot(occurence_matrix.dot(hrf_mean)).T

    return np.linalg.inv(db_ns_db).dot(drift_basis.T).dot(noise_struct).dot(data_s)


def maximization_sigmaH(D, Sigma_H, R, m_H):
    r"""Computes the M-sigma_h step of the JDE-VEM algorithm.

    .. math::

        \sigma^{2(r+1)}_{h} = \frac{\mathrm{tr} ((\Sigma^{(r)}_{H} + m^{(r)}_{H} (m^{(r)}_{H})^{\intercal})\mathbf{R}^{-1})}{D-1}

    """
    sigmaH = (np.dot(mult(m_H, m_H) + Sigma_H, R)).trace()
    sigmaH /= D
    return sigmaH


def maximization_sigmaH_prior(D, Sigma_H, R, m_H, gamma_h):
    r"""Computes the M-sigma_h step of the JDE-VEM algorithm with a prior.

    .. math::

        \sigma_{h}^{(r)} = \frac{(D-1) + \sqrt{8 \lambda_{\sigma_{h}} C + (D-1)^{2}}}{4\lambda_{\sigma_{h}}}

    where

    .. math::

        C = \mathrm{tr}\left( \left( \Sigma^{(r)}_{H} + m^{(r)}_{H} (m^{(r)}_{H})^{\intercal} \right) \mathbf{R}^{-1} \right)
    """

    alpha = (np.dot(mult(m_H, m_H) + Sigma_H, R)).trace()

    # sigmaH = (D + sqrt(D*D + 8*gamma_h*alpha)) / (4*gamma_h)
    sigmaH = (-D + np.sqrt(D * D + 8 * gamma_h * alpha)) / (4 * gamma_h)

    return sigmaH


def maximization_noise_var(occurence_matrix, hrf_mean, hrf_covar, nrls_mean, nrls_covar, noise_struct, data_drift,
                           nb_scans):
    r"""Computes the M-sigma_epsilon step of the JDE-VEM algorithm.

    .. math::

        \sigma^{2(r)}_{j} = \frac{1}{N} \left(\mathrm{E}_{\widetilde{p}^{(r)}_{A_{j}}} \left[a^{t}_{j}
        \widetilde{\Lambda}^{(r)}_{j} a_{j} \right] - 2 \left(m^{(r)}_{A_{j}}\right)^{t} \widetilde{G}^{(r)}_{j}
        y^{(r)}_{j} + \left(y^{(r)}_{j}\right)^{t} \Lambda^{(r)}_{j}y^{(r)}_{j} \right)


    where matrix :math:`\widetilde{\Lambda}^{(r)}_{j} = \mathrm{E}_{\widetilde{p}^{(r)}_{H}}
    \left[ G^{t}\Lambda^{(r)}_{j}G \right]` is a :math:`M \times M` whose element :math:`(m, m')` is given by

    .. math::

        \widetilde{g}^{t}_{m}\Lambda^{(r)}_{j}\widetilde{g}_{m'} + \mathrm{tr}\left(\Lambda^{(r)}_{j} X_{m}
        \Sigma^{(r)}_{H} X^{t}_{m'} \right)
    """

    # Precomputations
    om_hm = occurence_matrix.dot(hrf_mean)
    ns_om = np.tensordot(noise_struct, occurence_matrix, axes=(1, 1))
    nm_om_hm = nrls_mean.dot(om_hm)

    hm_om_ns_om_hm = ns_om.transpose(1, 0, 2).dot(hrf_mean).dot(om_hm.T)
    hc_om_ns_om = np.einsum('ijk,ljk->il', occurence_matrix.dot(hrf_covar.T), ns_om.transpose(1, 0, 2))

    hm_om_nm_ns_nm_om_hm = np.einsum('ij,ij->i', nrls_mean.dot(hm_om_ns_om_hm + hc_om_ns_om), nrls_mean)

    tr_nc_om_ns_om = np.einsum('ijk,ji->k', nrls_covar, hm_om_ns_om_hm + hc_om_ns_om)

    ns_df = noise_struct.dot(data_drift)
    df_ns_df = np.einsum('ij,ij->j', data_drift, ns_df)

    nm_om_hm_ns_df = np.einsum('ij,ji->i', nm_om_hm, ns_df)

    sigma = (hm_om_nm_ns_nm_om_hm + tr_nc_om_ns_om + df_ns_df - 2 * nm_om_hm_ns_df) / nb_scans

    return sigma


def beta_gradient(beta, labels_proba, labels_neigh, neighbours_indexes, gamma, gradient_method="m1"):
    r"""Computes the gradient of the beta function.

    The maximization of :math:`f(\beta^{m})` needs the computation of its derivative with respect to :math:`\beta^{m}`.

    **Method 1**

    .. math::

        \frac{\partial f(\beta^{m})}{\partial \beta^{m}} = -\frac{1}{2} \sum\limits_{j}
        \sum\limits_{k \in N(j)} \sum\limits_{i \in \{0,1\}} \left\{ p_{mf_{j}}(i)p_{mf_{k}}(i) -
        \widetilde{p}_{q^{m}_{j}}(i)\widetilde{p}_{q^{m}_{k}}(i) \right\} - \lambda_{\beta}

    **Method 2**

    .. math::

        \frac{\partial f(\beta^{m})}{\partial \beta^{m}} = - \sum\limits_{j}
        \sum\limits_{k \in N(j)} \sum\limits_{i \in \{0,1\}} \widetilde{p}_{q^{m}_{k}} (i) \left\{ p_{mf_{j}} (i) -
        \frac{1}{2}\widetilde{p}_{q^{m}_{j}} (i) \right\} - \lambda_{\beta}

    where

    .. math::

          p_{mf_{j}} (i) = \frac{\exp \left( \beta \sum\limits_{k \in N(j)} \widetilde{p}_{q^{m}_{k}} (i) \right)}
          {\sum\limits_{i \in \{0,1\}} \exp \left( \beta \sum\limits_{k \in N(j)} \widetilde{p}_{q^{m}_{k}} (i) \right)}


    Parameters
    ----------
    beta : float
    labels_proba : ndarray
    labels_neigh : ndarray
    neighbours_indexes : ndarray
    gamma : float
    gradient_method : str
        for testing purposes

    Returns
    -------
    gradient : float
        the gradient estimated in beta
    """

    beta_labels_neigh = beta * labels_neigh

    energy = np.exp(beta_labels_neigh - beta_labels_neigh.max(axis=0))
    energy /= energy.sum(axis=0)

    energy_neigh = sum_over_neighbours(neighbours_indexes, energy)

    if gradient_method == "m1":
        return (gamma*np.ones_like(beta)
                + (energy*energy_neigh - labels_proba*labels_neigh).sum()/2.)
    elif gradient_method == "m2":
        return (gamma*np.ones_like(beta)
                + ((energy - labels_proba)*labels_neigh).sum()/2.)
    else:
        raise NotImplemented


def beta_maximization(beta, labels_proba, neighbours_indexes, gamma):
    r"""Computes the Beta Maximization step of the JDE VEM algorithm.

    The maximization over each :math:`\beta^{m}` corresponds to the M-step obtained for a standard Hiddden MRF model:

    .. math::

        \hat{\beta}^{m} = \underset{\beta^{m}}{\mathrm{arg\, max}} f(\beta^{m})


    Parameters
    ----------
    beta : ndarray
        initial value of beta
    labels_proba : ndarray
    neighbours_indexes : ndarray
    gamma : float

    Returns
    -------
    beta : float
        the new value of beta
    success : bool
        True if the maximization has succeeded

    Notes
    -----
    See :meth:`beta_gradient` function.
    """

    labels_neigh = sum_over_neighbours(neighbours_indexes, labels_proba)

    try:
        beta_new, res = brentq(beta_gradient, 0., 10,
                               args=(labels_proba, labels_neigh, neighbours_indexes, gamma),
                               full_output=True)
        converged = res.converged
    except ValueError:
        beta_new = beta
        converged = False

    return beta_new, converged


def constraint_norm1_b(Ftilde, Sigma_F, positivity=False, perfusion=None):
    """ Constrain with optimization strategy """
    from scipy.optimize import fmin_l_bfgs_b, fmin_slsqp
    Sigma_F_inv = np.linalg.inv(Sigma_F)
    zeros_F = np.zeros_like(Ftilde)

    def fun(F):
        'function to minimize'
        return np.dot(np.dot((F - Ftilde).T, Sigma_F_inv), (F - Ftilde))

    def grad_fun(F):
        'gradient of the function to minimize'
        return np.dot(Sigma_F_inv, (F - Ftilde))

    def fung(F):
        'function to minimize'
        mean = np.dot(np.dot((F - Ftilde).T, Sigma_F_inv), (F - Ftilde)) #* 0.5
        Sigma = np.dot(Sigma_F_inv, (F - Ftilde))
        return mean #, Sigma

    def ec1(F):
        'Norm2(F)==1'
        return - 1 + np.linalg.norm(F, 2)

    def ec2(F):
        'F(0)==0'
        return F[0]

    def ec3(F):
        'F(end)==0'
        return F[-1]

    if positivity:
        def ec0(F):
            'F>=0 ?? or F>=-baseline??'
            return F
        y = fmin_slsqp(fun, Ftilde, eqcons=[ec1, ec2, ec3], ieqcons=[ec0],
                       bounds=[(None, None)] * (len(zeros_F)))
        #y = fmin_slsqp(fun, zeros_F, eqcons=[ec1], ieqcons=[ec2],
        #               bounds=[(None, None)] * (len(zeros_F)))
        #y = fmin_l_bfgs_b(fung, zeros_F, bounds=[(-1, 1)] * (len(zeros_F)))
    else:
        #y = fmin_slsqp(fun, Ftilde, eqcons=[ec1],
        #               bounds=[(None, None)] * (len(zeros_F)))
        y = fmin_slsqp(fun, Ftilde, eqcons=[ec1],#, ec2], #, ec3],
                       bounds=[(None, None)] * (len(zeros_F)))
        #print fmin_l_bfgs_b(fung, Ftilde, bounds=[(-1, 1)] * (len(zeros_F)), approx_grad=True)
        #y = fmin_l_bfgs_b(fun, Ftilde, fprime=grad_fun,
        #                  bounds=[(-1, 1)] * (len(zeros_F)))[0] #, approx_grad=True)[0]
    return y



def expectation_H_asl(Sigma_A, m_A, m_C, G, XX, W, Gamma, Gamma_X, X_Gamma_X, J, y_tilde,
                      cov_noise, R_inv, sigmaH, prior_mean_term, prior_cov_term):
    """
    Expectation-H step:

    .. math::

        p_H = argmax_h(E_pa,pc,pg[log p(h|y, a, c, g; theta)]) \propto exp(E_pa,pc,pg[log p(y|h, a, c, g; theta) + log p(h; sigmaH)])

    Returns
    -------
        m_H, Sigma_H of probability distribution p_H of the current iteration
    """

    ## Precomputations
    WXG = W.dot(XX.dot(G).T)
    mAX = np.tensordot(m_A, XX, axes=(1, 0))                # shape (J, N, D)
    #Gamma_X = np.tensordot(Gamma, XX, axes=(1, 1))
    #X_Gamma_X = np.tensordot(XX.T, Gamma_X, axes=(1, 0))    # shape (D, M, M, D)
    #cov_noise = np.maximum(sigma_eps, eps)[:, np.newaxis, np.newaxis]
    mAX_Gamma = (np.tensordot(mAX, Gamma, axes=(1, 0)) / cov_noise) # shape (J, D, N)

    ## Sigma_H computation
    # first summand: part of the prior -> R^-1 / sigmaH + prior_cov_term
    S_a = R_inv / sigmaH + prior_cov_term
    # second summand: E_pa[Saj.T*Gamma*Saj]
    # sum_{m, m'} Sigma_a(m,m') X_m.T Gamma_i X_m'
    S_a += (np.einsum('ijk,lijm->klm', Sigma_A, X_Gamma_X) / cov_noise).sum(0)
    # third summand: E_pa[Saj.T*Gamma*Saj]
    # (sum_m m_a X_m).T Gamma_i (sum_m m_a X_m)
    for i in xrange(0, J):
        S_a += mAX_Gamma[i, :, :].dot(mAX[i, :, :])  #option 1 faster 13.4
    #S_a += np.einsum('ijk,ikl->ijl', mAX_Gamma, mAX).sum(0) # option 2 second 8.8
    #S_a += np.einsum('ijk,ikl->jl', mAX_Gamma, mAX) # option 3 slower 7.5

    # Sigma_H = S_a^-1
    Sigma_H = np.linalg.inv(S_a)

    ## m_H
    # Y_bar_tilde computation: (sum_m m_a X_m).T Gamma_i y_tildeH
    # y_tildeH = yj - sum_m m_C WXG - w alphaj - P lj
    y_tildeH = y_tilde - WXG.dot(m_C.T)
    #Y_bar_tilde = np.tensordot(mAX_Gamma, y_tildeH, axes=([0, 2], [1, 0])) # slower
    Y_bar_tilde = np.einsum('ijk,ki->j', mAX_Gamma, y_tildeH)

    # we sum the term that corresponds to the prior
    Y_bar_tilde += prior_mean_term

    # m_H = S_a^-1 y_bar_tilde
    m_H = np.dot(np.linalg.inv(S_a), Y_bar_tilde)

    return m_H, Sigma_H


def expectation_H_ms_concat(Sigma_A, m_A, m_C, G, XX, W, Gamma, Gamma_X, X_Gamma_X, J, y_tilde,
                  cov_noise, R_inv, sigmaH, prior_mean_term, prior_cov_term, S):
    """
    Expectation-H step:

    .. math::
        p_H = argmax_h(E_pa,pc,pg[log p(h|y, a, c, g; theta)]) \propto exp(E_pa,pc,pg[log p(y|h, a, c, g; theta) + log p(h; sigmaH)])

    Returns
    -------
        m_H, Sigma_H of probability distribution p_H of the current iteration
    """

    ## Precomputations
    WXG = W.dot(XX.dot(G).T)
    mAX = np.tensordot(m_A, XX, axes=(1, 0))                # shape (J, N, D)
    #Gamma_X = np.tensordot(Gamma, XX, axes=(1, 1))
    #X_Gamma_X = np.tensordot(XX.T, Gamma_X, axes=(1, 0))   # shape (D, M, M, D)
    #cov_noise = np.maximum(sigma_eps, eps)[:, np.newaxis, np.newaxis]
    mAX_Gamma = (np.tensordot(mAX, Gamma, axes=(1, 0)) / cov_noise) # shape (J, D, N)

    ## Sigma_H computation
    # first summand: part of the prior -> R^-1 / sigmaH + prior_cov_term
    S_a = R_inv / sigmaH + prior_cov_term
    # second summand: E_pa[Saj.T*Gamma*Saj]
    # sum_{m, m'} Sigma_a(m,m') X_m.T Gamma_i X_m'
    print Sigma_A.shape
    for s in xrange(0, S):
        S_a += (np.einsum('ijk,lijm->klm', Sigma_A, X_Gamma_X) / cov_noise).sum(0)
    # third summand: E_pa[Saj.T*Gamma*Saj]
    # (sum_m m_a X_m).T Gamma_i (sum_m m_a X_m)
    for i in xrange(0, J):
        for s in xrange(0, S):
            i2 = (s-1)*J + i
            S_a += mAX_Gamma[i2, :, :].dot(mAX[i2, :, :])  #option 1 faster 13.4
    #S_a += np.einsum('ijk,ikl->ijl', mAX_Gamma, mAX).sum(0) # option 2 second 8.8
    #S_a += np.einsum('ijk,ikl->jl', mAX_Gamma, mAX) # option 3 slower 7.5

    # Sigma_H = S_a^-1
    Sigma_H = np.linalg.inv(S_a)

    ## m_H
    # Y_bar_tilde computation: (sum_m m_a X_m).T Gamma_i y_tildeH
    # y_tildeH = yj - sum_m m_C WXG - w alphaj - P lj
    y_tildeH = y_tilde - WXG.dot(m_C.T)
    #Y_bar_tilde = np.tensordot(mAX_Gamma, y_tildeH, axes=([0, 2], [1, 0])) # slower
    Y_bar_tilde = np.einsum('ijk,ki->j', mAX_Gamma, y_tildeH)

    # we sum the term that corresponds to the prior
    Y_bar_tilde += prior_mean_term

    # m_H = S_a^-1 y_bar_tilde
    m_H = np.dot(np.linalg.inv(S_a), Y_bar_tilde)

    return m_H, Sigma_H


def expectation_H_ms(Sigma_A, m_A, m_C, G, XX, W, Gamma, Gamma_X, X_Gamma_X, J, y_tilde,
                  cov_noise, R_inv, sigmaH, prior_mean_term, prior_cov_term, N, M, D, S):
    """
    Expectation-H step:

    .. math::
        p_H = argmax_h(E_pa,pc,pg[log p(h|y, a, c, g; theta)]) \propto exp(E_pa,pc,pg[log p(y|h, a, c, g; theta) + log p(h; sigmaH)])

    Returns
    -------
        m_H, Sigma_H of probability distribution p_H of the current iteration
    """

    ## Precomputations
    mAX = np.zeros((S, J, N, D), dtype=np.float64)
    WXG = np.zeros((S, N, M), dtype=np.float64)
    mAX_Gamma = np.zeros((S, J, D, N), dtype=np.float64)
    for s in xrange(0, S):
        WXG[s, :, :] = W.dot(XX[s, :, :, :].dot(G).T)                                   # shape (N, M)
        mAX[s, :, :, :] = np.tensordot(m_A[s, :, :], XX[s, :, :, :], axes=(1, 0))       # shape (J, N, D)
        mAX_Gamma[s, :, :, :] = (np.tensordot(mAX[s, :, :, :], Gamma, axes=(1, 0)) / cov_noise[s, :, :, :]) # shape (J, D, N)

    ## Sigma_H computation
    # first summand: part of the prior -> R^-1 / sigmaH + prior_cov_term
    S_a = R_inv / sigmaH + prior_cov_term
    # second summand: sum_{m, m'} Sigma_a(m,m') X_m.T Gamma_i X_m'
    for s in xrange(0, S):
        S_a += (np.einsum('ijk,lijm->klm', Sigma_A[:, :, :, s], X_Gamma_X[:, :, s, :, :]) / cov_noise[s, :, :, :]).sum(0)
    # third summand: (sum_m m_a X_m).T Gamma_i (sum_m m_a X_m)
    for s in xrange(0, S):
        for i in xrange(0, J):
            S_a += mAX_Gamma[s, i, :, :].dot(mAX[s, i, :, :])  #option 1 faster 13.4

    # Sigma_H = S_a^-1
    Sigma_H = np.linalg.inv(S_a)

    ## m_H
    # Y_bar_tilde computation: (sum_m m_a X_m).T Gamma_i y_tildeH
    # y_tildeH = yj - sum_m m_C WXG - w alphaj - P lj
    y_tildeH = np.zeros_like(y_tilde)
    Y_bar_tilde = np.zeros_like(prior_mean_term)
    for s in xrange(0, S):
        y_tildeH[s, :, :] = y_tilde[s, :, :] - WXG[s, :, :].dot(m_C[s, :, :].T)
        Y_bar_tilde += np.einsum('ijk,ki->j', mAX_Gamma[s, :, :, :], y_tildeH[s, :, :])

    # we sum the term that corresponds to the prior
    Y_bar_tilde += prior_mean_term

    # m_H = S_a^-1 y_bar_tilde
    m_H = np.dot(np.linalg.inv(S_a), Y_bar_tilde)

    return m_H, Sigma_H


def expectation_G_asl(Sigma_C, m_C, m_A, H, XX, W, WX, Gamma, Gamma_WX,
                      XW_Gamma_WX, J, y_tilde, cov_noise, R_inv, sigmaG,
                      prior_mean_term, prior_cov_term):
    """
    Expectation-G step:

    .. math::
        p_G = argmax_g(E_pa,pc,ph[log p(g|y, a, c, h; theta)]) \propto exp(E_pa,pc,ph[log p(y|h, a, c, g; theta) + log p(g; sigmaG)])

    Returns
    -------
        m_G, Sigma_G of probability distribution p_G of the current iteration
    """

    ## Precomputations
    XH = XX.dot(H).T
    mCWX = np.tensordot(m_C, WX, axes=(1, 0))                    # shape (J, N, D)
    mCWX_Gamma = np.tensordot(mCWX, Gamma, axes=(1, 0)) / cov_noise # shape (J, D, N)

    ## Sigma_H computation
    # first summand: part of the prior -> R^-1 / sigmaH + prior_cov_term
    S_c = R_inv / sigmaG + prior_cov_term
    # second summand: E_pc[Scj.T*Gamma*Scj] op1
    # sum_{m, m'} Sigma_c(m,m') X_m.T W.T Gamma_i W X_m'
    S_c += (np.einsum('ijk,lijm->klm', Sigma_C, XW_Gamma_WX) / cov_noise).sum(0)
    # third summand: E_pc[Scj.T*Gamma*Scj] op2
    # (sum_m m_c X_m).T Gamma_i (sum_m m_c W X_m)
    for i in xrange(0, J):
        S_c += mCWX_Gamma[i, :, :].dot(mCWX[i, :, :])  # option 1 faster 13.4
    #S_c += np.einsum('ijk,ikl->ijl', mCWX_Gamma, mCWX).sum(0) # option 2 second 8.8
    #S_c += np.einsum('ijk,ikl->jl', mCWX_Gamma, mCWX) # option 3 slower 7.5

    # Sigma_G = S_c^-1
    Sigma_G = np.linalg.inv(S_c)

    ## m_G
    # Y_bar_tilde computation: (sum_m m_c W X_m).T Gamma_i y_tildeG
    # y_tildeG = yj - sum_m m_A XH - w alphaj - P lj
    y_tildeG = y_tilde - XH.dot(m_A.T)
    #Y_bar_tilde = np.tensordot(mCWX_Gamma, y_tildeG, axes=([0, 2], [1, 0]))  # slower
    Y_bar_tilde = np.einsum('ijk,ki->j', mCWX_Gamma, y_tildeG)
    # we sum the term that corresponds to the prior
    Y_bar_tilde += prior_mean_term

    # m_H = S_c^-1 y_bar_tilde
    m_G = np.dot(Sigma_G, Y_bar_tilde)

    return m_G, Sigma_G


def expectation_G_ms(Sigma_C, m_C, m_A, H, XX, W, WX, Gamma, Gamma_WX,
                  XW_Gamma_WX, J, y_tilde, cov_noise, R_inv, sigmaG,
                  prior_mean_term, prior_cov_term, N, M, D, S):
    """
    Expectation-G step:

    .. math::
        p_G = argmax_g(E_pa,pc,ph[log p(g|y, a, c, h; theta)]) \propto exp(E_pa,pc,ph[log p(y|h, a, c, g; theta) + log p(g; sigmaG)])

    Returns
    -------
        m_G, Sigma_G of probability distribution p_G of the current iteration
    """

    ## Precomputations
    XH = XX.dot(H).T
    mCWX = np.zeros((S, J, N, D), dtype=np.float64)
    mCWX_Gamma = np.zeros((S, J, D, N), dtype=np.float64)
    for s in xrange(0, S):
        mCWX[s, :, :, :] = np.tensordot(m_C[s, :, :], WX[s, :, :, :], axes=(1, 0))       # shape (J, N, D)
        mCWX_Gamma[s, :, :, :] = (np.tensordot(mCWX[s, :, :, :], Gamma, axes=(1, 0)) / cov_noise[s, :, :, :]) # shape (J, D, N)

    ## Sigma_H computation
    # first summand: part of the prior -> R^-1 / sigmaH + prior_cov_term
    S_c = R_inv / sigmaG + prior_cov_term
    # second summand: sum_{m, m'} Sigma_c(m,m') X_m.T W.T Gamma_i W X_m'
    for s in xrange(0, S):
        S_c += (np.einsum('ijk,lijm->klm', Sigma_C[:, :, :, s], XW_Gamma_WX[:, :, s, :, :]) / cov_noise[s, :, :, :]).sum(0)
    # third summand: (sum_m m_c X_m).T Gamma_i (sum_m m_c W X_m)
    for s in xrange(0, S):
        for i in xrange(0, J):
            S_c += mCWX_Gamma[s, i, :, :].dot(mCWX[s, i, :, :])  #option 1 faster 13.4

    # Sigma_G = S_c^-1
    Sigma_G = np.linalg.inv(S_c)

    ## m_G
    # Y_bar_tilde computation: (sum_m m_c W X_m).T Gamma_i y_tildeG
    # y_tildeG = yj - sum_m m_A XH - w alphaj - P lj
    y_tildeG = np.zeros_like(y_tilde)
    Y_bar_tilde = np.zeros_like(prior_mean_term)
    for s in xrange(0, S):
        y_tildeG[s, :, :] = y_tilde[s, :, :] - XH[:, :, s].dot(m_A[s, :, :].T)
        Y_bar_tilde += np.einsum('ijk,ki->j', mCWX_Gamma[s, :, :, :], y_tildeG[s, :, :])
    # we sum the term that corresponds to the prior
    Y_bar_tilde += prior_mean_term

    # m_H = S_c^-1 y_bar_tilde
    m_G = np.dot(Sigma_G, Y_bar_tilde)

    return m_G, Sigma_G



def expectation_A_asl(H, G, m_C, W, XX, Gamma, Gamma_X, q_Z, mu_Ma, sigma_Ma,
                      J, y_tilde, Sigma_H, sigma_eps_m):
    """
    Expectation-A step:

    .. math::
        p_A = argmax_h(E_pc,pq,ph,pg[log p(a|y, h, c, g, q; theta)]) \propto exp(E_pc,ph,pg[log p(y|h, a, c, g; theta)] + E_pq[log p(a|q; mu_Ma, sigma_Ma)])

    Returns
    -------
        m_A, Sigma_A of probability distribution p_A of the current iteration
    """

    ## Pre-compute XH, X*Sigma_H, XG, WXG, Gamma*X
    XH = XX.dot(H).T
    Sigma_H_X = XX.dot(Sigma_H.T).T
    XG = XX.dot(G).T
    WXG = W.dot(XG)

    ## Sigma_A computation
    # first summand of Sigma_A: XH.T*Gamma*XH / sigma_eps
    Sigma_A = XH.T.dot(Gamma).dot(XH)[..., np.newaxis] / sigma_eps_m
    # second summand of Sigma_A: tr(X.T*Gamma*X*Sigma_H / sigma_eps)
    second_summand = np.einsum('ijk, jli', Sigma_H_X, Gamma_X)
    Sigma_A += second_summand[..., np.newaxis] / sigma_eps_m
    # third summand of Sigma_A: part of p(a|q; theta_A)
    Delta_k = (q_Z / np.maximum(sigma_Ma[:, :, np.newaxis], eps))
    Delta = Delta_k.sum(axis=1)         # sum across classes K
    for i in xrange(0, J):
        Sigma_A[:, :, i] = np.linalg.inv(Sigma_A[:, :, i] + \
                                         np.diag(Delta[:, i]))

    ## m_A computation
    # adding m_C*WXG to y_tilde
    y_tildeH = y_tilde - WXG.dot(m_C.T)
    Gamma_y_tildeH = Gamma.dot(y_tildeH).T
    X_tildeH = Gamma_y_tildeH.dot(XH) / sigma_eps_m[:, np.newaxis] \
               + (Delta_k * mu_Ma[:, :, np.newaxis]).sum(axis=1).T
    # dot product across voxels of Sigma_A and X_tildeH
    m_A = np.einsum('ijk,kj->ki', Sigma_A, X_tildeH)

    return m_A, Sigma_A


def expectation_A_ms(m_A, Sigma_A, H, G, m_C, W, XX, Gamma, Gamma_X, q_Z, mu_Ma, sigma_Ma,
                  J, y_tilde, Sigma_H, sigma_eps_m, N, M, D, S):
    """
    Expectation-A step:

    .. math::
        p_A = argmax_h(E_pc,pq,ph,pg[log p(a|y, h, c, g, q; theta)]) \propto exp(E_pc,ph,pg[log p(y|h, a, c, g; theta)] + E_pq[log p(a|q; mu_Ma, sigma_Ma)])

    Returns
    -------
        m_A, Sigma_A of probability distribution p_A of the current iteration
    """

    ## Pre-compute XH, X*Sigma_H, XG, WXG, Gamma*X
    XH = np.zeros((S, N, M), dtype=np.float64)
    XG = np.zeros((S, N, M), dtype=np.float64)
    Sigma_H_X = np.zeros((D, N, M, S), dtype=np.float64)
    WXG = np.zeros((S, N, M), dtype=np.float64)

    for s in xrange(0, S):
        XH[s, :, :] = XX[s, :, :, :].dot(H).T                       # (S, N, M)
        Sigma_H_X[:, :, :, s] = XX[s, :, :, :].dot(Sigma_H.T).T     # (D, N, M, S)
        XG[s, :, :] = XX[s, :, :, :].dot(G).T                       # (S, N, M)
        WXG[s, :, :] = W.dot(XG[s, :, :])                           # (S, N, M)

        ## Sigma_A computation
        # first summand of Sigma_A: XH.T*Gamma*XH / sigma_eps
        Sigma_A[:, :, :, s] = XH[s, :, :].T.dot(Gamma).dot(XH[s, :, :])[..., np.newaxis] / sigma_eps_m[s, :]
        # second summand of Sigma_A: tr(X.T*Gamma*X*Sigma_H / sigma_eps)
        second_summand = np.einsum('ijk, jli', Sigma_H_X[:, :, :, s], Gamma_X[:, s, :, :])
        Sigma_A[:, :, :, s] += second_summand[..., np.newaxis] / sigma_eps_m[s, :]
    # third summand of Sigma_A: part of p(a|q; theta_A)
    Delta_k = (q_Z / np.maximum(sigma_Ma[:, :, np.newaxis], eps))
    Delta = Delta_k.sum(axis=1)         # sum across classes K
    for s in xrange(0, S):
        for i in xrange(0, J):
            Sigma_A[:, :, i, s] = np.linalg.inv(Sigma_A[:, :, i, s] + \
                                             np.diag(Delta[:, i]))

    ## m_A computation
    # adding m_C*WXG to y_tilde
    for s in xrange(0, S):
        y_tildeH = y_tilde[s, :, :] - WXG[s, :, :].dot(m_C[s, :, :].T)
        Gamma_y_tildeH = Gamma.dot(y_tildeH).T
        X_tildeH = Gamma_y_tildeH.dot(XH[s, :, :]) / sigma_eps_m[s, :, np.newaxis] \
                   + (Delta_k * mu_Ma[:, :, np.newaxis]).sum(axis=1).T
        # dot product across voxels of Sigma_A and X_tildeH
        m_A[s, :, :] = np.einsum('ijk,kj->ki', Sigma_A[:, :, :, s], X_tildeH)

    return m_A, Sigma_A


def expectation_C_asl(G, H, m_A, W, XX, Gamma, Gamma_X, q_Z, mu_Mc, sigma_Mc,
                      J, y_tilde, Sigma_G, sigma_eps_m):
    """
    Expectation-C step:

    .. math::
        p_C = argmax_h(E_pa,pq,ph,pg[log p(a|y, h, a, g, q; theta)]) \propto exp(E_pa,ph,pg[log p(y|h, a, c, g; theta)] + E_pq[log p(c|q; mu_Mc, sigma_Mc)])

    Returns
    -------
        m_C, Sigma_C of probability distribution p_C of the current iteration
    """

    ## Pre-compute XH, X*Sigma_H, XG, WXG, Gamma*X
    XH = XX.dot(H).T
    Sigma_G_X = XX.dot(Sigma_G.T).T
    XG = XX.dot(G).T
    WXG = W.dot(XG)

    ## Sigma_C computation
    # first summand of Sigma_C: WXG.T*Gamma*WXG / sigma_eps
    Sigma_C = WXG.T.dot(Gamma).dot(WXG)[..., np.newaxis] / sigma_eps_m
    # second summand of Sigma_C: tr(X.T*Gamma*X*Sigma_G / sigma_eps)
    second_summand = np.einsum('ijk, jli', Sigma_G_X, Gamma_X)
    Sigma_C += second_summand[..., np.newaxis] / sigma_eps_m
    # third summand of Sigma_C: part of p(c|q; theta_C)
    Delta_k = (q_Z / np.maximum(sigma_Mc[:, :, np.newaxis], eps))
    Delta = Delta_k.sum(axis=1)          # sum across classes K
    for i in xrange(0, J):
        Sigma_C[:, :, i] = np.linalg.inv(Sigma_C[:, :, i] + \
                                         np.diag(Delta[:, i]))

    ## m_C computation
    # adding m_A*XH to y_tilde
    y_tildeG = y_tilde - XH.dot(m_A.T)
    Gamma_y_tildeG_WXG = Gamma.dot(y_tildeG).T.dot(WXG)
    X_tildeG = Gamma_y_tildeG_WXG / sigma_eps_m[:, np.newaxis] + \
                    (Delta_k * mu_Mc[:, :, np.newaxis]).sum(axis=1).T
    # dot product across voxels of Sigma_C and X_tildeG
    m_C = np.einsum('ijk,kj->ki', Sigma_C, X_tildeG)

    return m_C, Sigma_C


def expectation_C_ms(m_C, Sigma_C, G, H, m_A, W, XX, Gamma, Gamma_X, q_Z, mu_Mc, sigma_Mc,
                  J, y_tilde, Sigma_G, sigma_eps_m, N, M, D, S):
    """
    Expectation-C step:

    .. math::
        p_C = argmax_h(E_pa,pq,ph,pg[log p(a|y, h, a, g, q; theta)]) \propto exp(E_pa,ph,pg[log p(y|h, a, c, g; theta)] + E_pq[log p(c|q; mu_Mc, sigma_Mc)])

    Returns
    -------
        m_C, Sigma_C of probability distribution p_C of the current iteration
    """

    ## Pre-compute XH, X*Sigma_G, XG, WXG, Gamma*X
    XH = np.zeros((S, N, M), dtype=np.float64)
    XG = np.zeros((S, N, M), dtype=np.float64)
    Sigma_G_X = np.zeros((D, N, M, S), dtype=np.float64)
    WXG = np.zeros((S, N, M), dtype=np.float64)

    for s in xrange(0, S):
        XH[s, :, :] = XX[s, :, :, :].dot(H).T                       # (S, N, M)
        Sigma_G_X[:, :, :, s] = XX[s, :, :, :].dot(Sigma_G.T).T     # (D, N, M, S)
        XG[s, :, :] = XX[s, :, :, :].dot(G).T                       # (S, N, M)
        WXG[s, :, :] = W.dot(XG[s, :, :])                           # (S, N, M)

        ## Sigma_C computation
        # first summand of Sigma_C: WXG.T*Gamma*WXG / sigma_eps
        Sigma_C[:, :, :, s] = WXG[s, :, :].T.dot(Gamma).dot(WXG[s, :, :])[..., np.newaxis] / sigma_eps_m[s, :]
        # second summand of Sigma_C: tr(X.T*Gamma*X*Sigma_G / sigma_eps)
        second_summand = np.einsum('ijk, jli', Sigma_G_X[:, :, :, s], Gamma_X[:, s, :, :])
        Sigma_C[:, :, :, s] += second_summand[..., np.newaxis] / sigma_eps_m[s, :]
    # third summand of Sigma_C: part of p(c|q; theta_C)
    Delta_k = (q_Z / np.maximum(sigma_Mc[:, :, np.newaxis], eps))
    Delta = Delta_k.sum(axis=1)          # sum across classes K
    for s in xrange(0, S):
        for i in xrange(0, J):
            Sigma_C[:, :, i, s] = np.linalg.inv(Sigma_C[:, :, i, s] + \
                                             np.diag(Delta[:, i]))

    ## m_C computation
    # adding m_A*XH to y_tilde
    for s in xrange(0, S):
        y_tildeG = y_tilde[s, :, :] - XH[s, :, :].dot(m_A[s, :, :].T)
        Gamma_y_tildeG_WXG = Gamma.dot(y_tildeG).T.dot(WXG[s, :, :])
        X_tildeG = Gamma_y_tildeG_WXG / sigma_eps_m[s, :, np.newaxis] + \
                        (Delta_k * mu_Mc[:, :, np.newaxis]).sum(axis=1).T
        # dot product across voxels of Sigma_C and X_tildeG
        m_C[s, :, :] = np.einsum('ijk,kj->ki', Sigma_C[:, :, :, s], X_tildeG)

    return m_C, Sigma_C


def expectation_Q_asl(Sigma_A, m_A, Sigma_C, m_C, sigma_Ma, mu_Ma, sigma_Mc, \
                  mu_Mc, Beta, p_q_t, p_Q, neighbours_indexes, graph, M, J, K):
    # between ASL and BOLD just alpha and Gauss_mat change!!!
    alpha = - 0.5 * np.diagonal(Sigma_A)[:, :, np.newaxis] / (sigma_Ma[np.newaxis, :, :]) \
            - 0.5 * np.diagonal(Sigma_C)[:, :, np.newaxis] / (sigma_Mc[np.newaxis, :, :])  # (J, M, K)
    Gauss_mat = normpdf(m_A[...,np.newaxis], mu_Ma, np.sqrt(sigma_Ma)) * \
                normpdf(m_C[...,np.newaxis], mu_Mc, np.sqrt(sigma_Mc))

    # Update Ztilde ie the quantity which is involved in the a priori
    # Potts field [by solving for the mean-field fixed point Equation]
    # TODO: decide if we take out the computation of p_q_t or Ztilde
    B_pqt = Beta[:, np.newaxis, np.newaxis] * p_q_t.copy()
    B_pqt = np.concatenate((B_pqt, np.zeros((M, K, 1), dtype=B_pqt.dtype)), axis=2)
    local_energy = B_pqt[:, :, neighbours_indexes].sum(axis=3).transpose(2, 0, 1)
    energy = (alpha + local_energy)
    energy -= energy.max()
    Probas = (np.exp(energy) * Gauss_mat).transpose(1, 2, 0)
    aux = Probas.sum(axis=1)[:, np.newaxis, :]
    aux[np.where(aux==0)] = eps
    p_q_t = Probas / aux

    return p_q_t, p_q_t


def expectation_Q_ms(Sigma_A, m_A, Sigma_C, m_C, sigma_Ma, mu_Ma, sigma_Mc, \
                  mu_Mc, Beta, p_q_t, p_Q, neighbours_indexes, graph, M, J, K, S):
    # between ASL and BOLD just alpha and Gauss_mat change!!!
    alpha = np.zeros((J, M, K), dtype=np.float64)
    Gauss_mat = np.zeros_like(alpha)
    for s in xrange(S):
        alpha -= 0.5 * np.diagonal(Sigma_A[:, :, :, s])[:, :, np.newaxis] / (sigma_Ma[np.newaxis, :, :])
        #Gauss_mat += np.log(vt.normpdf(m_A[s, :, :, np.newaxis], mu_Ma, np.sqrt(sigma_Ma)))
        Gauss_mat += sp.stats.norm.logpdf(m_A[s, :, :, np.newaxis], mu_Ma, np.sqrt(sigma_Ma))

    # Update Ztilde ie the quantity which is involved in the a priori
    # Potts field [by solving for the mean-field fixed point Equation]
    # TODO: decide if we take out the computation of p_q_t or Ztilde
    B_pqt = Beta[:, np.newaxis, np.newaxis] * p_q_t.copy()
    B_pqt = np.concatenate((B_pqt, np.zeros((M, K, 1), dtype=B_pqt.dtype)), axis=2)
    local_energy = B_pqt[:, :, neighbours_indexes].sum(axis=3).transpose(2, 0, 1)
    energy = (local_energy + alpha + Gauss_mat )
    #energy -= energy.max()
    Probas = (np.exp(energy)).transpose(1, 2, 0)
    aux = Probas.sum(axis=1)[:, np.newaxis, :]
    aux[np.where(aux==0)] = eps
    p_q_t = Probas / aux

    return p_q_t, p_q_t


def expectation_Q_async_asl(Sigma_A, m_A, Sigma_C, m_C, sigma_Ma, mu_Ma, sigma_Mc, \
                  mu_Mc, Beta, p_q_t, p_Q, neighbours_indexes, graph, M, J, K):
    # between ASL and BOLD just alpha and Gauss_mat change!!!
    alpha = (- 0.5 * np.diagonal(Sigma_A)[:, :, np.newaxis] / (sigma_Ma[np.newaxis, :, :]) \
             - 0.5 * np.diagonal(Sigma_C)[:, :, np.newaxis] / (sigma_Mc[np.newaxis, :, :])).transpose(1, 2, 0)  # (J, M, K)
    Gauss_mat = (normpdf(m_A[...,np.newaxis], mu_Ma, np.sqrt(sigma_Ma)) * \
                 normpdf(m_C[...,np.newaxis], mu_Mc, np.sqrt(sigma_Mc))).transpose(1, 2, 0)

    energy = np.zeros_like(p_q_t)
    local_energy = np.zeros_like(p_q_t)
    Probas = np.zeros_like(p_q_t)
    for vox in xrange(J):
        B_pqt = Beta[:, np.newaxis, np.newaxis] * p_q_t.copy()
        B_pqt = np.concatenate((B_pqt, np.zeros((M, K, 1), dtype=B_pqt.dtype)), axis=2)
        local_energy[:, :, vox] = B_pqt[:, :, neighbours_indexes[vox, :]].sum(axis=2)
        energy[:, :, vox] = (alpha[:, :, vox] + local_energy[:, :, vox])
        Probas[:, :, vox] = (np.exp(energy[:, :, vox]) * Gauss_mat[:, :, vox])
        aux = Probas[:, :, vox].sum(axis=1)[:, np.newaxis]
        aux[np.where(aux==0)] = eps
        p_q_t[:, :, vox] = Probas[:, :, vox] / aux

        #local_energy[:, :, vox] = sum_over_neighbours(neighbours_indexes[vox, :], beta[..., np.newaxis, np.newaxis] * labels_proba)
        #energy[:, :, vox] = alpha[:, :, vox] + local_energy[:, :, vox]
        #labels_proba[:, :, vox] = (np.exp(energy[:, :, vox])*gauss[:, :, vox])
        #labels_proba[:, :, vox] = labels_proba[:, :, vox]/labels_proba[:, :, vox].sum(axis=1)[:, np.newaxis]

    return p_q_t, p_q_t


def maximization_mu_sigma_asl(q_Z, m_X, Sigma_X):

    qZ_sumvox = q_Z.sum(axis=2)                              # (M, K)
    Mu = np.zeros_like(qZ_sumvox)
    Mu[:, 1] = (q_Z[:, 1, :] * m_X.T).sum(axis=1) / qZ_sumvox[:, 1]

    mX_minus_Mu_2 = (m_X[..., np.newaxis] - Mu[np.newaxis, ...]).transpose(1, 2, 0)**2
    SigmaX_diag = np.diagonal(Sigma_X).T
    Sigma = (q_Z * (mX_minus_Mu_2 + SigmaX_diag[:, np.newaxis, :])).sum(axis=2) / qZ_sumvox

    return Mu, Sigma


def maximization_mu_sigma_ms(q_Z, m_X, Sigma_X, M, J, S, K):
    qZ_sumvox = q_Z.sum(axis=2) * S                          # (M, K)
    Mu = np.zeros_like(qZ_sumvox)
    Mu[:, 1] = (q_Z[:, 1, :] * m_X.sum(0).T).sum(axis=1) / qZ_sumvox[:, 1]

    sess_term = np.zeros((M, K, J), dtype=np.float64)
    for s in xrange(S):
        mX_minus_Mu_2 = (m_X[s, :, :, np.newaxis] - Mu[np.newaxis, :, :]).transpose(1, 2, 0)**2
        SigmaX_diag = np.diagonal(Sigma_X[:, :, :, s]).T
        sess_term += mX_minus_Mu_2 + np.concatenate((SigmaX_diag[:, np.newaxis, :],
                                                     SigmaX_diag[:, np.newaxis, :]), axis=1)
    Sigma = (q_Z * sess_term).sum(axis=2) / qZ_sumvox

    return Mu, Sigma


def maximization_sigma_asl(D, Sigma_H, R_inv, m_H, use_hyp, gamma_h):
    alpha = (np.dot(m_H[:, np.newaxis] * m_H[np.newaxis, :] + Sigma_H, R_inv)).trace()
    if use_hyp:
        sigma = (-(D) + np.sqrt((D) * (D) + 8 * gamma_h * alpha)) / (4*gamma_h)
    else:
        sigma = alpha / (D)
    return sigma


def maximization_Mu_asl(H, G, matrix_covH, matrix_covG,
                        sigmaH, sigmaG, sigmaMu, Omega, R_inv):
    Aux = matrix_covH / sigmaH + np.dot(Omega.T, Omega) / sigmaG + R_inv / sigmaMu
    Mu = np.dot(sp.linalg.inv(Aux), (H / sigmaH + np.dot(Omega.T, G) / sigmaG))
    return Mu


def maximization_beta_m4_asl(beta, p_Q, Qtilde_sumneighbour, Qtilde, neighboursIndexes,
                             maxNeighbours, gamma, MaxItGrad, gradientStep):
    # Method 4 in Christine's thesis:
    # - sum_j sum_k (sum_neighbors p_Q) (p_Q_MF - p_Q) - gamma
    Gr = 100
    ni = 1
    while ((abs(Gr) > 0.0001) and (ni < MaxItGrad)):

        # p_Q_MF according to new beta
        beta_Qtilde_sumneighbour = beta * Qtilde_sumneighbour
        E = np.exp(beta_Qtilde_sumneighbour - beta_Qtilde_sumneighbour.max(axis=0))  # (K, J)
        p_Q_MF = E / E.sum(axis=0)

        # Gradient computation
        Gr = gamma + (Qtilde_sumneighbour * (p_Q_MF - p_Q)).sum()

        # Update of beta: beta - gradientStep * Gradient
        beta -= gradientStep * Gr

        ni += 1
    return beta


def maximization_beta_m2_asl(beta, p_Q, Qtilde_sumneighbour, Qtilde, neighboursIndexes,
                             maxNeighbours, gamma, MaxItGrad, gradientStep):
    # Method 2 in Christine's thesis:
    # - 1/2 sum_j sum_k sum_neighbors (p_Q_MF p_Q_MF_sumneighbour - p_Q pQ_sumneighbour) - gamma
    Gr = 100
    ni = 1

    while ((abs(Gr) > 0.0001) and (ni < MaxItGrad)):

        # p_Q_MF according to new beta
        beta_Qtilde_sumneighbour = beta * Qtilde_sumneighbour
        E = np.exp(beta_Qtilde_sumneighbour - beta_Qtilde_sumneighbour.max(axis=0))  # (K, J)
        p_Q_MF = E / E.sum(axis=0)

        # sum_neighbours p_Q_MF(neighbour) according to new beta
        p_Q_MF_sumneighbour = p_Q_MF[:, neighboursIndexes].sum(axis=2)

        # Gradient computation
        Gr = gamma + ( p_Q_MF * p_Q_MF_sumneighbour - p_Q * Qtilde_sumneighbour ).sum() / 2.

        # Update of beta: beta - gradientStep * Gradient
        beta -= gradientStep * Gr

        ni += 1
    return beta


def fun(Beta, p_Q, Qtilde_sumneighbour, neighboursIndexes, gamma):
    'function to minimize'
    # p_Q_MF according to new beta
    if (p_Q).ndim == 3:
        beta_Qtilde_sumneighbour = (Beta[:, np.newaxis, np.newaxis] * \
                                Qtilde_sumneighbour).squeeze()
    else:
        beta_Qtilde_sumneighbour = (Beta * Qtilde_sumneighbour).squeeze()
    # Mean field approximation
    E = np.exp(beta_Qtilde_sumneighbour - beta_Qtilde_sumneighbour.max(axis=0))  # (K, J)
    aux = E.sum(axis=0)
    aux[np.where(aux==0)] = eps
    p_Q_MF = E / aux
    if (p_Q).ndim == 3:
        p_Q_MF_sumneighbour = p_Q_MF[:, :, neighboursIndexes].sum(axis=3)  # (M, K, J)
        function = - np.log(np.exp(beta_Qtilde_sumneighbour).sum(axis=1)).sum() \
                    + (Beta * (p_Q * Qtilde_sumneighbour / 2. + \
                        p_Q_MF * (Qtilde_sumneighbour - p_Q_MF_sumneighbour / 2.) \
                        ).sum(axis=(1, 2))) - gamma * Beta
        gradient = - gamma * np.ones_like(Beta) - (p_Q_MF * p_Q_MF_sumneighbour - \
                                   p_Q * Qtilde_sumneighbour).sum(axis=(1, 2)) / 2.
    else:
        p_Q_MF_sumneighbour = p_Q_MF[:, neighboursIndexes].sum(axis=2)  # (M, K, J)
        function = - np.log(np.exp(beta_Qtilde_sumneighbour).sum(axis=0)).sum() \
                    + (Beta * (p_Q * Qtilde_sumneighbour / 2. + \
                          p_Q_MF * (Qtilde_sumneighbour - p_Q_MF_sumneighbour / 2.) \
                          ).sum()) - gamma * Beta
        gradient = - gamma * np.ones_like(Beta) - (p_Q_MF * p_Q_MF_sumneighbour - \
                                                   p_Q * Qtilde_sumneighbour).sum() / 2.
    return np.asfortranarray([-function])#, np.asfortranarray([ - gradient])


def grad_fun(Beta, p_Q, Qtilde_sumneighbour, neighboursIndexes, gamma):
    'function to minimize'
    # p_Q_MF according to new beta
    beta_Qtilde_sumneighbour = (Beta * \
                                Qtilde_sumneighbour).squeeze()
    # Mean field approximation
    E = np.exp(beta_Qtilde_sumneighbour - beta_Qtilde_sumneighbour.max(axis=0))  # (K, J)
    aux = E.sum(axis=0)
    aux[np.where(aux==0)] = eps
    p_Q_MF = E / aux
    if (p_Q_MF).ndim == 3:
        p_Q_MF_sumneighbour = p_Q_MF[:, :, neighboursIndexes].sum(axis=3)  # (M, K, J)
        gradient = - gamma * np.ones_like(Beta) - (p_Q_MF * p_Q_MF_sumneighbour - \
                                                   p_Q * Qtilde_sumneighbour).sum(axis=(1, 2)) / 2.
    else:
        p_Q_MF_sumneighbour = p_Q_MF[:, neighboursIndexes].sum(axis=2)  # (M, K, J)
        gradient = - gamma * np.ones_like(Beta) - (p_Q_MF * p_Q_MF_sumneighbour - \
                                                  p_Q * Qtilde_sumneighbour).sum() / 2.
    return np.asfortranarray([-gradient])


def maximization_beta_m2_scipy_asl(Beta, p_Q, Qtilde_sumneighbour, Qtilde, neighboursIndexes,
                                   maxNeighbours, gamma, MaxItGrad, gradientStep):
    """ Maximize beta """
    from scipy.optimize import fmin_l_bfgs_b, minimize, fmin_bfgs, fmin_cg, brentq

    try:
        beta_new, res = brentq(
            grad_fun, 0., 10, args=(p_Q, Qtilde_sumneighbour, neighboursIndexes, gamma),
            full_output=True
        )
    except ValueError:
        beta_new = Beta
        class res(): pass
        res.converged = False
    if not res.converged:
        logger.warning("max beta did not converge: %s (beta=%s)", res, beta_new)

    return beta_new #, res.converged

    """
    #beta_new = fmin_l_bfgs_b(fun, Beta, \
    #                args=(p_Q, Qtilde_sumneighbour, neighboursIndexes, gamma),
    #                bounds=[(0, 10)] * (len(np.array([Beta]))))
    try:
        n = len(Beta)
    except:
        n = 1
    print n
    beta_new = fmin_l_bfgs_b(fun, np.array([Beta]), \
                    args=(p_Q, Qtilde_sumneighbour, neighboursIndexes, gamma),
                    fprime=grad_fun,
                    bounds=[(0, None)]*n)
    print beta_new
    # You can add at the end fprime=grad_fun to give the gradient separately
    return beta_new[0]"""


def maximization_LA_asl(Y, m_A, m_C, XX, WP, W, WP_Gamma_WP, H, G, Gamma):
    # Precomputations
    #WP = np.append(w[:, np.newaxis], P, axis=1)
    #Gamma_WP = Gamma.dot(WP)
    #WP_Gamma_WP = WP.T.dot(Gamma_WP)

    # TODO: for BOLD, just take out mCWXG term
    mAXH = m_A.dot(XX.dot(H)).T                             # shape (N, J)
    mCWXG = XX.dot(G).dot(W).T.dot(m_C.T)                   # shape (N, J)
    S = Y - (mAXH + mCWXG)

    AL = np.linalg.inv(WP_Gamma_WP).dot(WP.T).dot(Gamma).dot(S)
    return AL   ##AL[1:, :], AL[0, :], AL


def maximization_sigma_noise_asl(XX, m_A, Sigma_A, H, m_C, Sigma_C, G,
                                 Sigma_H, Sigma_G, W, y_tilde, Gamma,
                                 Gamma_X, Gamma_WX, N):
    """
    Maximization sigma_noise
    """
    # Precomputations
    XH = XX.dot(H)                                          # shape (N, M)
    XG = XX.dot(G)                                          # shape (N, M)
    WX = W.dot(XX).transpose(1, 0, 2)                       # shape (M, N, D)
    WXG = W.dot(XG.T)
    mAXH = m_A.dot(XH)                                      # shape (J, N)
    mAXH_Gamma = mAXH.dot(Gamma)                            # shape (J, N)
    mCWXG = m_C.dot(WXG.T)                                  # shape (J, N)
    mCWXG_Gamma = mCWXG.dot(Gamma)                          # shape (J, N)
    #Gamma_X = np.tensordot(Gamma, XX, axes=(1, 1))
    #Gamma_WX = np.tensordot(Gamma, WX, axes=(1, 1))

    HXXH = XH.dot(Gamma_X.dot(H))       # (,D)*(D,N,M)*(M,N,D)*(D,) -> (M, M)
    Sigma_H_X_X = np.einsum('ijk,jli->kl', XX.dot(Sigma_H.T).T, Gamma_X)
    GXWWXG = WXG.T.dot(Gamma_WX.dot(G)) # (,D)*(D,N,M)*(M,N,D)*(D,) -> (M, M)
    Sigma_G_XW_WX = np.einsum('ijk,jlk->il', WX.dot(Sigma_G.T), Gamma_WX)

    # mA.T (X.T H.T H X + SH X.T X) mA
    HXAAXH = np.einsum('ij,ij->i', m_A.dot(HXXH + Sigma_H_X_X), m_A)

    # mC.T (W.T X.T G.T G X W + SH W.T X.T X W) mC
    GXWCCWXG = np.einsum('ij,ij->i', m_C.dot(GXWWXG + Sigma_G_XW_WX), m_C)

    # trace(Sigma_A (X.T H.T H X + SH X.T X) ) in each voxel
    tr_SA_HXXH = np.einsum('ijk,ji->k', Sigma_A, (HXXH + Sigma_H_X_X))

    # trace(Sigma_A (W.T X.T G.T G X W + SH W.T X.T X W) ) in each voxel
    tr_SC_HXXH = np.einsum('ijk,ji->k', Sigma_C, (GXWWXG + Sigma_G_XW_WX))

    # mC.T W.T X.T G.T H X mA
    CWXGHXA = np.einsum('ij,ij->i', mCWXG_Gamma, mAXH)

    # y_tilde.T y_tilde
    Gamma_ytilde = Gamma.dot(y_tilde)
    ytilde_ytilde = np.einsum('ij,ij->j', y_tilde, Gamma_ytilde)

    # (mA X H + mC W X G) y_tilde
    AXH_CWXG_ytilde = np.einsum('ij,ji->i', (mAXH + mCWXG), Gamma_ytilde)

    return (HXAAXH + GXWCCWXG + tr_SA_HXXH + tr_SC_HXXH \
            + 2 * CWXGHXA + ytilde_ytilde - 2 * AXH_CWXG_ytilde) / N



def computeFit_asl(H, m_A, G, m_C, W, XX):
    """ Compute Fit """
    # Precomputations
    XH = XX.dot(H)                                          # shape (N, M)
    XG = XX.dot(G)                                          # shape (N, M)
    WX = W.dot(XX).transpose(1, 0, 2)                       # shape (M, N, D)
    WXG = W.dot(XG.T)
    mAXH = m_A.dot(XH).T                                    # shape (N, J)
    mCWXG = m_C.dot(WXG.T).T                                # shape (N, J)

    return mAXH + mCWXG



# Entropy functions
##############################################################

eps_FreeEnergy = 0.00000001
eps_freeenergy = 0.00000001


# def A_Entropy(Sigma_A, M, J):

    # logger.info('Computing NRLs Entropy ...')
    # Det_Sigma_A_j = np.zeros(J, dtype=np.float64)
    # Entropy = 0.0
    # for j in xrange(0, J):
        # Det_Sigma_A_j = np.linalg.det(Sigma_A[:, :, j])
        # Const = (2 * np.pi * np.exp(1)) ** M
        # Entropy_j = np.sqrt(Const * Det_Sigma_A_j)
        # Entropy += np.log(Entropy_j + eps_FreeEnergy)
    # Entropy = - Entropy

    # return Entropy


def nrls_entropy(nrls_covar, nb_conditions):
    r"""Compute the entropy of neural response levels. The entropy of a multivariate normal distribution is

    .. math::

        \ln\left( \sqrt{(2\pi e)^{n} \left|\Sigma \right|} \right)

    where *n* is the dimensionality of the vector space and :math:`\left|\Sigma \right|` is the determinant of the
    covariance matrix.

    Parameters
    ----------
    nrls_covar : ndarray, shape (nb_conditions, nb_conditions, nb_voxels)
        Covariance of the NRLs
    nb_conditions : int

    Returns
    -------
    entropy : float
    """

    const = (2*np.pi)**nb_conditions * np.exp(nb_conditions)
    det_nrls_covar = np.linalg.det(nrls_covar.transpose((2, 0, 1)))

    return np.sum(np.log(np.sqrt(const*det_nrls_covar)))

def A_Entropy(Sigma_A, M, J):
    import warnings
    warnings.warn("The A_Entropy function is deprecated, use nrls_entropy instead",
                  DeprecationWarning)
    return -nrls_entropy(Sigma_A, M)


# def H_Entropy(Sigma_H, D):

    # logger.info('Computing HRF Entropy ...')
    # Det_Sigma_H = np.linalg.det(Sigma_H)
    # Const = (2 * np.pi * np.exp(1)) ** D
    # Entropy = np.sqrt(Const * Det_Sigma_H)
    # Entropy = - np.log(Entropy + eps_FreeEnergy)

    # return Entropy


def hrf_entropy(hrf_covar, hrf_len):
    r"""Compute the entropy of the hemodynamic response function. The entropy of a multivariate normal distribution is

    .. math::

        \ln\left( \sqrt{(2\pi e)^{n} \left|\Sigma \right|} \right)

    where *n* is the dimensionality of the vector space and :math:`\left|\Sigma \right|` is the determinant of the
    covariance matrix.

    Parameters
    ----------
    hrf_covar : ndarray, shape (hrf_len, hrf_len)
        Covariance matrix of the HRF
    hrf_len : int
        size of the HRF

    Returns
    -------
    entropy : float
    """

    det_hrf_covar = np.linalg.det(hrf_covar)

    if det_hrf_covar == 0:
        return 0

    const = (2 * np.pi) ** hrf_len * np.exp(hrf_len)
    return np.log(np.sqrt(const*det_hrf_covar))


def H_Entropy(Sigma_H, D):
    import warnings
    warnings.warn("The H_Entropy function is deprecated, use hrf_entropy instead",
                  DeprecationWarning)
    return -hrf_entropy(Sigma_H, D)


# def Z_Entropy(q_Z, M, J):

    # logger.info('Computing Z Entropy ...')
    # Entropy = 0.0
    # for j in xrange(0, J):
        # for m in xrange(0, M):
            # Entropy += q_Z[m, 1, j] * np.log(q_Z[m, 1, j] + eps_FreeEnergy) + q_Z[
                # m, 0, j] * np.log(q_Z[m, 0, j] + eps_FreeEnergy)

    # return Entropy


def labels_entropy(labels_proba):
    r"""Compute the labels entropy.

    .. math::

        -\sum\limits^{1}_{x=0} p_{Q}(x) \log p_{Q}(x)

    Parameters
    ----------
    labels_proba : ndarray, shape (nb_conditions, nb_classes, nb_voxels)
        Probability of each voxel to be in one class

    Returns
    -------
    entropy : float
    """

    # To prevent log of zero we put in another variable the zeros to epsilon
    # This doesn't change the results since the log is multiplied by zero
    labels_proba_log = labels_proba.copy()
    labels_proba_log[labels_proba_log == 0] = eps

    return -(labels_proba * np.log(labels_proba_log)).sum()


def Z_Entropy(q_Z, M, J):
    import warnings
    warnings.warn("The Z_Entropy function is deprecated, use labels_entropy instead",
                  DeprecationWarning)
    return -labels_entropy(q_Z)


# Entropy functions ASL
##############################################################

eps_FreeEnergy = 0.0000000001


def RL_Entropy(Sigma_RL, M, J):
    #logger.info('Computing RLs Entropy ...')
    Det_Sigma_RL_j = np.zeros(J, dtype=np.float64)
    Const = (2 * np.pi * np.exp(1)) ** M
    Entropy = 0.0
    for j in xrange(0, J):
        Det_Sigma_RL_j = np.linalg.det(Sigma_RL[:, :, j])
        Entropy_j = np.sqrt(Const * Det_Sigma_RL_j)
        Entropy += np.log(Entropy_j)
    return Entropy


def RF_Entropy(Sigma_RF, D):
    #logger.info('Computing RF Entropy ...')
    if Sigma_RF.sum()==0:
        Entropy = 0
    else:
        _, log_Det_Sigma_RF = np.linalg.slogdet(Sigma_RF)
        Const = (2 * np.pi * np.exp(1)) ** D
        Entropy = (np.log(Const) + log_Det_Sigma_RF) /2
    return Entropy


def Q_Entropy(q_Z, M, J):
    #logger.info('Computing Z Entropy ...')
    q_Z_control_0 = q_Z.copy()
    q_Z_control_0[np.where(q_Z==0)] = eps_FreeEnergy
    return - (q_Z * np.log(q_Z_control_0)).sum()


def RL_expectation_Ptilde(m_X, Sigma_X, mu_Mx, sigma_Mx, q_Z):
    #logger.info('Computing RLs expectation Ptilde ...')
    diag_Sigma_X = np.diagonal(Sigma_X)[:, :, np.newaxis]
    S = - q_Z.transpose(2, 0, 1) * (np.log(2 * np.pi * sigma_Mx) + \
                 ((m_X[:, :, np.newaxis] - mu_Mx[np.newaxis, :, :]) ** 2 \
                    + diag_Sigma_X) / sigma_Mx[np.newaxis, :, :]) / 2.
    return S.sum()


def RF_expectation_Ptilde(m_X, Sigma_X, sigmaX, R, R_inv, D):
    #logger.info('Computing RF expectation Ptilde ...')
    _, logdetR = np.linalg.slogdet(R)
    const = D * np.log(2 * np.pi) + logdetR
    S = (np.dot(np.dot(m_X.T, R_inv), m_X) + np.dot(Sigma_X, R_inv).trace()) / sigmaX \
        + D * np.log(sigmaX)
    return - (const + S) / 2.


def Q_expectation_Ptilde(q_Z, neighboursIndexes, Beta, gamma, K, M):
    #Qtilde = np.concatenate((q_Z, np.zeros((M, K, 1), dtype=q_Z.dtype)), axis=2)
    Qtilde_sumneighbour = q_Z[:, :, neighboursIndexes].sum(axis=3) # (M, K, J)
    beta_Qtilde_sumneighbour = Beta[:, np.newaxis, np.newaxis] * Qtilde_sumneighbour

    # Mean field approximation
    E = np.exp(beta_Qtilde_sumneighbour - beta_Qtilde_sumneighbour.max(axis=0)) # (K, J)
    aux = E.sum(axis=0)
    aux[np.where(aux==0)] = eps
    p_Q_MF = E / aux

    # sum_neighbours p_Q_MF(neighbour) according to new beta
    p_Q_MF_sumneighbour = p_Q_MF[:, :, neighboursIndexes].sum(axis=3)  # (M, K, J)

    return - np.log(np.exp(beta_Qtilde_sumneighbour).sum(axis=1)).sum() \
           + (Beta * (q_Z * Qtilde_sumneighbour / 2. + \
                      p_Q_MF * (Qtilde_sumneighbour - p_Q_MF_sumneighbour / 2.)\
                      ).sum(axis=(1,2))).sum() #- (Beta * gamma).sum()


def expectation_Ptilde_Likelihood(y_tilde, m_A, Sigma_A, H, Sigma_H, m_C,
                                  Sigma_C, G, Sigma_G, XX, W, sigma_eps,
                                  Gamma, J, D, M, N, Gamma_X, Gamma_WX):
    #print sigma_eps[np.where(np.isnan(np.log(sigma_eps)))]
    sigma_eps_1 = maximization_sigma_noise_asl(XX, m_A, Sigma_A, H, m_C, Sigma_C, \
                                           G, Sigma_H, Sigma_G, W, y_tilde, Gamma, \
                                           Gamma_X, Gamma_WX, N)
    return  - (N * J * np.log(2 * np.pi) - J * np.log(np.linalg.det(Gamma)) \
            + N * np.log(sigma_eps).sum() + N * (sigma_eps_1 / sigma_eps).sum()) / 2.


def Compute_FreeEnergy(y_tilde, m_A, Sigma_A, mu_Ma, sigma_Ma, m_H, Sigma_H, AuxH,
                       R, R_inv, sigmaH, sigmaG, m_C, Sigma_C, mu_Mc, sigma_Mc,
                       m_G, Sigma_G, AuxG, q_Z, neighboursIndexes, Beta, Gamma,
                       gamma, gamma_h, gamma_g, sigma_eps, XX, W,
                       J, D, M, N, K, hyp, Gamma_X, Gamma_WX, plot=False,
                       bold=False, S=1):
    # Entropy
    EntropyA = RL_Entropy(Sigma_A, M, J)
    EntropyC = RL_Entropy(Sigma_C, M, J)
    EntropyH = RF_Entropy(Sigma_H, D)
    EntropyG = RF_Entropy(Sigma_G, D)
    EntropyQ = Q_Entropy(q_Z, M, J)

    # Likelihood
    EPtildeLikelihood = expectation_Ptilde_Likelihood(y_tilde, m_A, Sigma_A, m_H, Sigma_H, m_C,
                                                      Sigma_C, m_G, Sigma_G, XX, W, sigma_eps,
                                                      Gamma, J, D, M, N, Gamma_X, Gamma_WX)
    EPtildeA = RL_expectation_Ptilde(m_A, Sigma_A, mu_Ma, sigma_Ma, q_Z)
    EPtildeC = RL_expectation_Ptilde(m_C, Sigma_C, mu_Mc, sigma_Mc, q_Z)
    EPtildeH = RF_expectation_Ptilde(AuxH, Sigma_H, sigmaH, R, R_inv, D)
    EPtildeG = RF_expectation_Ptilde(AuxG, Sigma_G, sigmaG, R, R_inv, D)
    EPtildeQ = Q_expectation_Ptilde(q_Z, neighboursIndexes, Beta, gamma, K, M)
    EPtildeBeta = M * np.log(gamma) - gamma * Beta.sum()
    if hyp:
        EPtildeVh = np.log(gamma_h) - gamma_h * sigmaH
        EPtildeVg = np.log(gamma_g) - gamma_g * sigmaG
    else:
        EPtildeVh = 0.
        EPtildeVg = 0.

    if bold:
        Total_Entropy = EntropyA + EntropyH / S + EntropyQ / S
        EPtilde = EPtildeLikelihood + EPtildeA + EPtildeH / S + EPtildeQ / S \
                + EPtildeBeta / S + EPtildeVh / S
    else:
        Total_Entropy = EntropyA + EntropyH + EntropyC + EntropyG + EntropyQ
        EPtilde = EPtildeLikelihood + EPtildeA + EPtildeH + EPtildeC + EPtildeG + EPtildeQ \
                + EPtildeBeta + EPtildeVh + EPtildeVg

    if plot:
        print 'Total_Entropy = ', Total_Entropy
        print 'EA = ', EntropyA, 'EH = ', EntropyH, 'EQ = ', EntropyQ
        if not bold:
            print 'EC = ', EntropyC, 'EG = ', EntropyG,
        print 'Total_EPtilde = ', EPtilde
        print 'ELklh = ', EPtildeLikelihood, 'EPtA = ', EPtildeA,  \
                'EPtH = ', EPtildeH, 'EPtQ = ', EPtildeQ, \
                'EPtBeta = ', EPtildeBeta, 'EPtVh = ', EPtildeVh
        if not bold:
            print 'EPtC = ', EPtildeC, 'EPtG = ', EPtildeG, 'EPtVg = ', EPtildeVg

    return EPtilde + Total_Entropy


# Other functions
##############################################################

def computeFit(hrf_mean, nrls_mean, X, nb_voxels, nb_scans):
    """Compute the estimated induced signal by each stimulus.

    Parameters
    ----------
    hrf_mean: ndarray
    nrls_mean: ndarray
    X: OrderedDict
    nb_voxels: int
    nb_scans: int

    Returns
    -------
    ndarray
    """

    stim_ind_signal = np.zeros((nb_scans, nb_voxels), dtype=np.float64)

    for voxel in xrange(0, nb_voxels):
        for m, condition in enumerate(X):
            stim_ind_signal[:, voxel] += nrls_mean[voxel, m] * np.dot(X[condition], hrf_mean)

    return stim_ind_signal


def expectation_ptilde_likelihood(data_drift, nrls_mean, nrls_covar, hrf_mean, hrf_covar, occurence_matrix, noise_var,
                                  noise_struct, nb_voxels, nb_scans):
    r"""Expectation with respect to likelihood.

    .. math::

        \mathrm{E}_{\widetilde{p}_{a}\widetilde{p}_{h}\widetilde{p}_{q}}\left[\log p(y | a,h,q; \theta) \right] =
        -\frac{NJ}{2} \log 2\pi + \frac{J}{2}\log\left| \Lambda_{j} \right| - N\sum\limits_{j \in J}\log
        v_{b_{j}} + \frac{1}{2v_{b_{j}}}\sum\limits_{j \in J}V_{j}

    where

    .. math::

        V_{j} = \widetilde{m}^{t}_{a_{j}}\mathbf{X}^{t}_{h}\Lambda_{j}\mathbf{X}_{h}\widetilde{m}_{a_{j}}
        + \mathrm{tr}\left( \Sigma_{a_{j}}\mathbf{X}^{t}_{h}\Lambda_{j}\mathbf{X}_h \right) -
        2\widetilde{m}^{t}_{a_{j}} \mathbf{X}^{t}_{h}\Lambda_{j}\left( y_{j} - \mathbf{P}\ell_{j} \right)

    Parameters
    ----------
    data_drift : ndarray, shape (nb_scans, nb_voxels)
        This is the BOLD data minus the drifts (y_tilde in the paper)
    nrls_mean : ndarray, shape (nb_voxels, nb_conditions)
    nrls_covar : ndarray, shape (nb_conditions, nb_conditions, nb_voxels)
    hrf_mean : ndarray, shape (hrf_len,)
    hrf_covar : ndarray, shape (hrf_len, hrf_len)
    occurence_matrix : ndarray, shape (nb_conditions, nb_scans, hrf_len)
    noise_var : ndarray, shape (nb_voxels,)
    noise_struct : ndarray, shape (nb_scans, nb_scans)
    nb_voxels : int
    nb_scans : int

    Returns
    -------
    ptilde_likelihood : float
    """

    noise_var_tmp = maximization_noise_var(occurence_matrix, hrf_mean, hrf_covar, nrls_mean,
                                           nrls_covar, noise_struct, data_drift, nb_scans)

    return - (nb_scans * nb_voxels*np.log(2*np.pi)
              - nb_voxels * np.log(np.linalg.det(noise_struct))
              + nb_scans * np.log(np.absolute(noise_var)).sum()
              + nb_scans * (noise_var_tmp / noise_var).sum()) / 2.


def expectation_ptilde_hrf(hrf_mean, hrf_covar, sigma_h, hrf_regu_prior, hrf_regu_prior_inv, hrf_len):
    r"""Expectation  with respect to p_tilde hrf.

    .. math::
          \mathrm{E}_{\widetilde{p}_{h}}\left[ \log p(h | \sigma_{h}) \right] = -\frac{D+1}{2}\log 2\pi -
          \frac{D-1}{2}\log \sigma_{h} - \frac{\log \left| \mathbf{R} \right|}{2} - \frac{m^{t}_{h}\mathbf{R}^{-1}m_{h}
          + \mathrm{tr} \left( \Sigma_{h} \mathbf{R}^{-1} \right)}{2 \sigma_{h}}

    """

    const = -(hrf_len*np.log(2*np.pi) + hrf_len*np.log(sigma_h)
              + np.linalg.slogdet(hrf_regu_prior)[1])

    s = -(np.dot(np.dot(hrf_mean.T, hrf_regu_prior_inv), hrf_mean)
          + np.dot(hrf_covar, hrf_regu_prior_inv).trace()) / sigma_h

    return (const + s) / 2.


def expectation_ptilde_labels(labels_proba, neighbours_indexes, beta, nb_conditions, nb_classes):
    r"""Expectation with respect to p_tilde q (or z).

    .. math::

        \mathrm{E}_{\widetilde{p}_{q}} \left[ \log p (q | \beta ) \right] = \sum\limits_{m} & \left\{
          - \sum\limits_{j} \left\{ \log \left( \sum\limits^{1}_{i=0} \exp \left(
          \beta^{m} \sum\limits_{k \in N(j)} \widetilde{p}_{q^{m}_{k}} (i) \right)
          \right) \right\} \right. \\
          & \left. - \beta^{m} \sum\limits_{j}\sum\limits_{k \in N(j)}\sum\limits^{1}_{i=0}
          \left[ p^{MF}_{j}(i) \left( \frac{p^{MF}_{k}(i)}{2} -
          \widetilde{p}_{q^{m}_{k}} (i) \right) -
          \frac{1}{2}\widetilde{p}_{q^{m}_{j}}(i)\widetilde{p}_{q^{m}_{k}}(i) \right]
          \right\}

    """

    # term p_{q^{m}_{k}}
    labels_neigh = np.concatenate((labels_proba,
                                   np.zeros((nb_conditions, nb_classes, 1), dtype=labels_proba.dtype)),
                                  axis=2)
    labels_neigh = labels_neigh[:, :, neighbours_indexes].sum(axis=3)

    beta_labels_neigh = beta[:, np.newaxis, np.newaxis] * labels_neigh

    # term p^{MF}_{j}
    energy = np.exp(beta_labels_neigh - beta_labels_neigh.max(axis=0))
    energy /= energy.sum(axis=0)

    # term p^{MF}_{k}
    energy_neigh = energy[:, :, neighbours_indexes].sum(axis=3)

    first_sum = -np.log(np.exp(beta_labels_neigh).sum(axis=1)).sum()
    second_sum = (beta * (labels_proba * labels_neigh/2.
                          + energy * (labels_neigh-energy_neigh/2.)
                          ).sum(axis=(1, 2))
                  ).sum()

    return first_sum + second_sum


def expectation_ptilde_nrls(labels_proba, nrls_class_mean, nrls_class_var, nrls_mean, nrls_covar):
    r"""Expectation with respect to p_tilde a.

    .. math::

        \mathrm{E}_{\widetilde{p}_{a}\widetilde{p}_{q}}[\log p (a | q, \theta_{a})] = \sum\limits_{m}\sum\limits_{j}
        & \left\{ \left[1 - \widetilde{p}_{q^{m}_{j}}(1) \right] \left[\log\frac{1}{\sqrt{2\pi\sigma^{2m}_{0}}} -
        \frac{\left(m_{a^{m}_{j}} - \mu^{m}_{0} \right)^{2} + \Sigma_{a^{m,m}_{j}}}{2\sigma^{2m}_{0}} \right] +
        \right. \\ &  \left. \widetilde{p}_{q^{m}_{j}}(1)  \left[\log\frac{1}{\sqrt{2\pi\sigma^{2m}_{1}}} -
        \frac{\left(m_{a^{m}_{j}} - \mu^{m}_{1} \right)^{2} + \Sigma_{a^{m,m}_{j}}}{2\sigma^{2m}_{1}} \right] \right\}

    """

    diag_nrls_covar = np.diagonal(nrls_covar)[:, :, np.newaxis]

    s = -labels_proba.transpose(2, 0, 1) * (np.log(2*np.pi*nrls_class_var)
                                            + ((nrls_mean[:, :, np.newaxis] - nrls_class_mean[np.newaxis, :, :])**2
                                               + diag_nrls_covar) / nrls_class_var[np.newaxis, :, :]
                                            ) / 2

    return s.sum()


def free_energy_computation(nrls_mean, nrls_covar, hrf_mean, hrf_covar, hrf_len,
                            labels_proba, data_drift, occurence_matrix, noise_var,
                            noise_struct, nb_conditions, nb_voxels, nb_scans, nb_classes,
                            nrls_class_mean, nrls_class_var, neighbours_indexes,
                            beta, sigma_h, hrf_regu_prior, hrf_regu_prior_inv,
                            gamma, hrf_hyperprior):
    r"""Compute the free energy functional.

    .. math::

        \mathcal{F}(q, \theta) = \mathrm{E}_{q}\left[ \log p(y, A, H, Z ; \theta) \right] +  \mathcal{G}(q)

    where :math:`E_{q}[\cdot]` denotes the expectation with respect to *q* and
    :math:`\mathcal{G}(q)` is the entropy of *q*.

    Parameters
    ----------

    Returns
    -------
    free_energy : float
    """

    expectation_likelihood = expectation_ptilde_likelihood(data_drift, nrls_mean, nrls_covar,
                                                           hrf_mean, hrf_covar, occurence_matrix,
                                                           noise_var, noise_struct, nb_voxels, nb_scans)

    entropy_nrls = nrls_entropy(nrls_covar, nb_conditions)
    expectation_nrls = expectation_ptilde_nrls(labels_proba, nrls_class_mean, nrls_class_var, nrls_mean, nrls_covar)

    entropy_labels = labels_entropy(labels_proba)
    expectation_labels = expectation_ptilde_labels(labels_proba, neighbours_indexes, beta, nb_conditions, nb_classes)

    # hrf_covar is set to 0 when the hrf is not estimated
    if np.linalg.det(hrf_covar) == 0:
        expectation_hrf = 0
        entropy_hrf = 0
        hrf_hyperprior = 0
    else:
        expectation_hrf = expectation_ptilde_hrf(hrf_mean, hrf_covar, sigma_h, hrf_regu_prior, hrf_regu_prior_inv,
                                                 hrf_len)
        entropy_hrf = hrf_entropy(hrf_covar, hrf_len)

    total_expectation = expectation_likelihood + expectation_nrls + expectation_labels + expectation_hrf
    total_entropy = entropy_nrls + entropy_hrf + entropy_labels

    total_prior = 0
    if gamma:
        total_prior += nb_conditions*np.log(gamma) - gamma*beta.sum()

    if hrf_hyperprior:
        total_prior += np.log(hrf_hyperprior) - hrf_hyperprior*sigma_h

    return total_expectation + total_entropy + total_prior


# Contrasts
##########################
from pyhrf.tools.aexpression import ArithmeticExpression as AExpr

def compute_contrasts(condition_names, contrasts, m_A, m_C,
                      Sigma_A, Sigma_C, M, J):
    brls_conds = dict([(str(cn), m_A[:, ic])
                      for ic, cn in enumerate(condition_names)])
    prls_conds = dict([(str(cn), m_C[:, ic])
                      for ic, cn in enumerate(condition_names)])
    n = 0
    CONTRAST_A = np.zeros_like(m_A)
    CONTRASTVAR_A = np.zeros_like(m_A)
    CONTRAST_C = np.zeros_like(m_C)
    CONTRASTVAR_C = np.zeros_like(m_C)
    for cname in contrasts:
        print cname
        #------------ contrasts ------------#
        contrast_expr = AExpr(contrasts[cname], **brls_conds)
        contrast_expr.check()
        contrast = contrast_expr.evaluate()
        CONTRAST_A[:, n] = contrast
        contrast_expr = AExpr(contrasts[cname], **prls_conds)
        contrast_expr.check()
        contrast = contrast_expr.evaluate()
        CONTRAST_C[:, n] = contrast

        #------------ variance -------------#
        ContrastCoef = np.zeros(M, dtype=float)
        ind_conds0 = {}
        for m in xrange(0, M):
            ind_conds0[condition_names[m]] = 0.0
        for m in xrange(0, M):
            ind_conds = ind_conds0.copy()
            ind_conds[condition_names[m]] = 1.0
            ContrastCoef[m] = eval(contrasts[cname], ind_conds)
        print 'active contrasts'
        ActiveContrasts = (ContrastCoef != 0) * np.ones(M, dtype=float)
        AC = ActiveContrasts * ContrastCoef
        for j in xrange(0, J):
            Sa_tmp = Sigma_A[:, :, j]
            CONTRASTVAR_A[j, n] = np.dot(np.dot(AC, Sa_tmp), AC)
            Sc_tmp = Sigma_C[:, :, j]
            CONTRASTVAR_C[j, n] = np.dot(np.dot(AC, Sc_tmp), AC)

        n += 1
    return CONTRAST_A, CONTRASTVAR_A, CONTRAST_C, CONTRASTVAR_C


# Plots
####################################

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import os.path as op
import os

def plot_response_functions_it(ni, NitMin, M, H, G, Mu=None, prior=None):
    if not op.exists('./plots'):
        os.makedirs('./plots')
    jet = plt.get_cmap('jet')
    cNorm = colors.Normalize(vmin=0, vmax=NitMin + 1)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    font = {'size': 15}
    matplotlib.rc('font', **font)
    if ni == 0:
        plt.close('all')
    colorVal = scalarMap.to_rgba(ni)
    plt.figure(M + 1)
    plt.plot(H, color=colorVal)
    plt.hold(True)
    plt.savefig('./plots/BRF_Iter_ASL.png')
    plt.figure(M + 2)
    plt.plot(G, color=colorVal)
    plt.hold(True)
    plt.savefig('./plots/PRF_Iter_ASL.png')
    if prior=='hierarchical':
        plt.figure(M + 3)
        plt.plot(Mu, color=colorVal)
        plt.hold(True)
        plt.savefig('./plots/Mu_Iter_ASL.png')
    return


def plot_convergence(ni, M, cA, cC, cH, cG, cAH, cCG,
                     SUM_q_Z, mua1, muc1, FE):
    SUM_p_Q_array = np.zeros((M, ni), dtype=np.float64)
    mua1_array = np.zeros((M, ni), dtype=np.float64)
    muc1_array = np.zeros((M, ni), dtype=np.float64)
    for m in xrange(M):
        for i in xrange(ni):
            SUM_p_Q_array[m, i] = SUM_q_Z[m][i]
            mua1_array[m, i] = mua1[m][i]
            muc1_array[m, i] = muc1[m][i]

    import matplotlib
    import matplotlib.pyplot as plt
    font = {'size': 15}
    matplotlib.rc('font', **font)
    if not op.exists('./plots'):
        os.makedirs('./plots')
    plt.figure(M + 4)
    plt.plot(cAH[1:-1], 'lightblue')
    plt.hold(True)
    plt.plot(cCG[1:-1], 'm')
    plt.hold(False)
    plt.legend(('CAH', 'CCG'))
    plt.grid(True)
    plt.savefig('./plots/Crit_ASL.png')
    plt.figure(M + 5)
    plt.plot(cA[1:-1], 'lightblue')
    plt.hold(True)
    plt.plot(cC[1:-1], 'm')
    plt.plot(cH[1:-1], 'green')
    plt.plot(cG[1:-1], 'red')
    plt.hold(False)
    plt.legend(('CA', 'CC', 'CH', 'CG'))
    plt.grid(True)
    plt.savefig('./plots/Crit_all.png')
    plt.figure(M + 6)
    for m in xrange(M):
        plt.plot(SUM_p_Q_array[m])
        plt.hold(True)
    plt.hold(False)
    plt.savefig('./plots/Sum_p_Q_Iter_ASL.png')
    plt.figure(M + 7)
    plt.plot(FE, label='Free energy')
    plt.legend(loc=4)
    import time
    plt.savefig('./plots/free_energy.png')
    #plt.savefig('./plots/free_energy' + str(time.time()) + '.png')
    return
