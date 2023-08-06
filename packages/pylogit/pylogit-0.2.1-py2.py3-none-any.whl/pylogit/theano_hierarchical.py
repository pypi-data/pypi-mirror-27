"""
@module:    theano_hierarchical_calcs.py
@name:      Hierarchichal Logit Calculations with Theano
@author:    Timothy Brathwaite
@summary:   Contains functions necessary for calculating choice probabilities
            and estimating Hierarchical Logit models with Theano.
@questions: 1) It is unclear how the guards against overflow and underflow will
               work with the autodifferentiation in Theano. Off the top of my
               head, this type of 'hard-coding' of a value is not
               differentiable.
"""
import numpy as np
from scipy.sparse import csr_matrix

# Import the theano.tensor module for use in defining
import theano
import theano.tensor as tt
from theano import sparse


# Define the boundary values which are not to be exceeded during computation
# This is to prevent underflow and overflow.
min_exponent_val = -700
max_exponent_val = 700

max_comp_value = 1e300
min_comp_value = 1e-300


# Define symbols for the quantities that will be used in the various functions
# beta will be a 1D array with a shape (design.shape[0],) column
beta = tt.dvector('beta')
# design will be 2D with arbitrary number of rows and columns
design = tt.dmatrix('design')
# rows_to_obs will be a 2D compressed sparse row matrix. Note that
# this may not be the most efficient format to use, since I have
# more rows than columns, but I have to compute dot products with
# this variable so that seems to point to the use of compressed
# sparse rows
rows_to_obs = sparse.csr_matrix('rows_to_obs', dtype="int64")
# The choice vector will be a 2D array with one row. lrow specifies
# a dtype of int64 which seems like overkill, but I think this is
# the dtype of the default integer array from numpy.
choice_vector = tt.lrow('choice_vector')

# Define a symbol for the error components that will be added to the
# traditional systematic utility for the MNL model. Note that these
# will be normal error components for now
error_components = tt.dvector('err_components')

# Create a function to calculate the systematic utilities for the
# choice model given the beta, design, and non-gumbel error
# components. Note that in the future this function will be expanded
# to include the arguments needed to compute the transformed
# utilities for the asymmetric choice models.
def calc_error_comp_utilities(beta, design, error_components):
    """
    This function will compute X*beta + error_components.

    Parameters
    ----------
    beta : 1D ndarray of shape `(design.shape[1],)`.
        All elements should by ints, floats, or longs. There should be one
        element per index coefficient.
    design : 2D ndarray.
        There should be one row per observation per available alternative.
        There should be one column per utility coefficient being estimated. All
        elements should be ints, floats, or longs.
    error_components : 1D ndarray of shape `(design.shape[0],)`.
        All elements should be floats or longs. These will be the error
        components to be added to the deterministic portion of the systematic
        utility.

    Returns
    -------
    sys_utility : 1D ndarray of shape `(design.shape[0],)`
        X*beta + error_components
    """
    return tt.dot(design, beta) + error_components


def calc_mixed_mnl_probabilities(beta,
                                 design,
                                 rows_to_obs,
                                 error_components):
    """
    This function will calculate the MNL choice probabilities for each
    alternative of each choice situation in the design matrix. This function
    will be specific to ONLY the MNL model. Note this function is overly
    restrictive because Theano can only do automatic differentiation of
    functions that return scalars. This means the log-likelihood function
    must only return a single value, so this probability function must only
    return a 1D array (or a column vector in 2D).

    Parameters
    ----------
    beta : 1D ndarray of shape `(design.shape[1],)`.
        All elements should by ints, floats, or longs. There should be one
        element per index coefficient.
    design : 2D ndarray.
        There should be one row per observation per available alternative.
        There should be one column per utility coefficient being estimated. All
        elements should be ints, floats, or longs.
    rows_to_obs : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).
    error_components : 1D ndarray of shape `(design.shape[0],)`.
        All elements should be floats or longs. These will be the error
        components to be added to the deterministic portion of the systematic
        utility.

    Returns
    -------
    long_probs : 1D ndarray of shape `(design.shape[0],)`.
        There will be one element per observation per available alternative for
        that observation. Each element will be the probability of the
        corresponding observation being associated with that rows corresponding
        alternative.
    """
    # Calculate the systematic utility for each alternative for each individual
    sys_utilities = calc_error_comp_utilities(beta, design, error_components)

    # The following commands are to guard against numeric under/over-flow
    # Note that the strange function calls (e.g. switch) are used because
    # Theano needs special commands to emulate the (clearer) numpy behavior.
    sys_utilities = tt.switch(tt.lt(sys_utilities, min_exponent_val),
                              min_exponent_val,
                              sys_utilities)

    sys_utilities = tt.switch(tt.gt(sys_utilities, max_exponent_val),
                              max_exponent_val,
                              sys_utilities)

    # Exponentiate the transformed utilities
    long_exponentials = np.exp(sys_utilities)

    # Calculate \sum _j exp(V_j) for each individual.
    # Result should be a 1D array.
    individual_denominators = sparse.dot(sparse.transpose(rows_to_obs),
                                         long_exponentials)

    # Get a 1D array of the same number of rows as the design matrix, with each
    # element of each row representing the `individual_denominators` for the
    # given choice situation for the given observation.
    long_denominators = sparse.dot(rows_to_obs,
                                   individual_denominators)

    # long_probs will be of shape (num_rows,) Each element will provide the
    # probability of the observation associated with that row having the
    # alternative associated with that row as the observation's outcome
    long_probs = long_exponentials / long_denominators

    # Guard against underflow. Note the `.nonzero()` is so Theano can duplicate
    # the boolean slicing capabilities of numpy.
    long_probs = tt.switch(tt.eq(long_probs, 0), min_comp_value, long_probs)

    # Consider using an assert statement that ensures all probabilities add to
    # 1 for each choice situation.
    return long_probs


# Create the function that will calculate the log-likelihood for the MNL model
# This will be a symbolic function once we evaluate it on the Theano Tensor
# Variables.
def calc_mixed_mnl_log_likelihood(theta_tilde,
                                  num_variances,
                                  num_betas,
                                  design,
                                  rows_to_obs,
                                  choice_vector,
                                  total_error_array,
                                  overwrite):
    """
    This function will calculate the log-likelihood of an MNL model (and only
    an MNL model).

    Parameters
    ----------
    beta : 1D ndarray of shape `(design.shape[1],)`.
        All elements should by ints, floats, or longs. Should have 1 element
        for each utility coefficient being estimated (i.e. num_features).
    design : 2D ndarray.
        There should be one row per observation per available alternative.
        There should be one column per utility coefficient being estimated. All
        elements should be ints, floats, or longs.
    rows_to_obs : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).
    choice_vector : 2D ndarray of shape `(1, design.shape[0])`.
        All elements should be either ones or zeros. There should be one column
        per observation per available alternative for the given observation.
        Elements denote the alternative which is chosen by the given
        observation with a 1 and a zero otherwise.
    error_components : 1D ndarray of shape `(design.shape[0],)`.
        All elements should be floats or longs. These will be the error
        components to be added to the deterministic portion of the systematic
        utility.

    Returns
    -------
    log_likelihood : float. The log likelihood of the multinomial logit model.
    """
    # Get the position in theta_tilde, at which the betas start
    beta_neg_idx = -1 * num_betas
    # Split theta_tilde into its various components
    beta = theta_tilde[beta_neg_idx:]
    error_terms = theta_tilde[num_variances:beta_neg_idx]

    # Create the actual total array of error terms by overwriting
    # the zeros with their actual values from theta_tilde where
    # appropriate.
    total_error_array =\
        tt.set_subtensor(total_error_array[overwrite],
                         error_terms)

    # Calculate the probability of each individual choosing each available
    # alternative for that individual.
    long_probs =\
        calc_mixed_mnl_probabilities(beta,
                                     design,
                                     rows_to_obs,
                                     total_error_array)

    # Calculate the log likelihood
    log_likelihood = tt.dot(choice_vector, tt.log(long_probs))

    # Note that the log-likelihood is a (1, 1) array, so summing over
    # both axes does nothing but return the value at log_likelihood[0][0]
    # This is necessary because we need to return a scalar for the
    # automatic differentiation capabilities of Theano to work.
    return log_likelihood[0]


def log_jacobian_log_transform(theta_tilde, num_variances):
    """
    Calculate the log of the jacobian for variables that result
    from a `log` transform where `theta_new = log(theta_orig)`
    or alternatively `theta_orig = exp(theta_new)`.

    Parameters
    ----------
    orig_params : 1D ndarray.
        Should specify the value of the original parameters that
        were log-transformed.

    Returns
    -------
    log_jacobian : scalar.
        `log_jacobian = log(prod(orig_params))`
    """
    # Split theta_tilde into its various components
    alt_specific_variances = tt.exp(theta_tilde[:num_variances])

    return tt.sum(tt.log(alt_specific_variances))


def log_second_stage_inv_gammas(theta_tilde,
                                num_variances,
                                inv_gamma_alphas,
                                inv_gamma_betas):
    """
    Calculates the log of the joint density of the alternative specific
    variances. Note that alternative specific variances are assumed to
    be independent of each other and follow inverse gamma distributions.
    The returned value is correct up to an additive constant (which is
    comprised of arbitrary constants as well as the log-marginal evidence).

    Parameters
    ----------
    alt_variances : 1D ndarray of positive floats.
        Each element represents the variance of a particular alternative.
    inv_gamma_alphas, inv_gamma_betas : 1D ndarray of floats.
        Each element of inv_gamma_alphas (inv_gamma_betas) is a hyperprior
        for the alpha (beta) of the inverse gamma distribution that is
        being used as the prior for the given alternative's variance.

    Returns
    -------
    log_second_stage : scalar.
        The log of the joint density of the alternative specific variances,
        up to an additive constant that contains the log of the
        normalization constant and the log of the other arbitrary contants
        from the inverse gamma distribution.

    References
    ----------
    Gelman, Andrew, et al. (2014). Bayesian Data Analysis, 3rd Ed. Taylor
        & Francis Group. pp. 576-578.
    """
    # Split theta_tilde into its various components
    alt_variances = tt.exp(theta_tilde[:num_variances])

    # Begin computation of the log-joint-second-stage density
    neg_alphas_plus_1 = -1 * (inv_gamma_alphas + 1)
    term_1 = tt.dot(neg_alphas_plus_1, tt.log(alt_variances))

    neg_betas_over_variances = -1 * inv_gamma_betas / alt_variances

    # Guard against overflow
    neg_betas_over_variances = tt.switch(tt.lt(neg_betas_over_variances,
                                               -1 * max_comp_value),
                                         -1 * max_comp_value,
                                         neg_betas_over_variances)
    term_2 = tt.sum(neg_betas_over_variances)

    log_second_stage = term_1 + term_2

    return log_second_stage


def log_first_stage_indep_normal_priors(theta_tilde,
                                        num_variances,
                                        num_betas,
                                        filtered_rows_to_alts):
    """
    Calculates the log of the first stage joint density of error terms
    conditional on the alternative specific variances. Note that the
    error terms are assumed to be INDEPENDENTLY normally distributed
    with mean zero, conditional on the alternative specific variances.
    The returned value is correct up to an additive constant (which is
    comprised of arbitrary constants as well as the log-marginal evidence).

    Parameters
    ----------
    error_terms : 1D ndarray of floats.
        The error terms we want to calculate the log of the joint density of.
    alt_variances : 1D ndarray of positive floats.
        Each value should represent one alternative speciific variance.
    filtered_rows_to_alts : 2D sparse array of zeros and ones.
        Each element (i, j) should denote whether row i corresponds to
        alternative j or not using one's and zero's reespectively.

    Returns
    -------
    log_first_stage : scalar.
        The log of the joint density of the error terms, up to an additive
        constant that contains the log of the normalization constant and the
        log of the other arbitrary contants from the multivariate normal
        distribution.

    References
    ----------
    Gelman, Andrew, et al. (2014). Bayesian Data Analysis, 3rd Ed. Taylor
        & Francis Group. pp. 576-578.
    """
    # Get the position in theta_tilde, at which the betas start
    beta_neg_idx = -1 * num_betas
    # Split theta_tilde into its various components
    alt_variances = tt.exp(theta_tilde[:num_variances])
    error_terms = theta_tilde[num_variances:beta_neg_idx]

    # If the error terms are conditionally independent given the
    # alternative specific variances, then the covariance matrix
    # for the joint distribution of errors is diagonal and the inverse
    # of a diagonal matrix is a diagonal matrix with the inverses on
    # the diagonal. The inverses are calculated below
    inverse_variances = 1.0 / alt_variances

    # Map the inverse variances to their corresponding rows of error terms
    long_inverse_variances =\
        sparse.dot(filtered_rows_to_alts, inverse_variances)

    squared_errors = error_terms**2

    # Below, we implement -0.5 * (theta - mu)^T Sigma^{-1} (theta - mu) for
    # the specific case of a diagonal Sigma, Mu = 0, and theta = error_terms
    log_first_stage =\
        -0.5 * tt.sum(tt.mul(long_inverse_variances, squared_errors))

    return log_first_stage


def log_index_coefs_normal_priors(theta_tilde,
                                  num_betas,
                                  prior_index_variances):
    """
    Calculates the log of the prior density of index coefficients
    conditional on the specified variances of each index coefficient's
    prior density. Note that the index coefficients are assumed to have
    INDEPENDENT prior densities that follow a normally distribution with mean
    zero, conditional on the hyperpriors aka the variance of the prior
    distribution. The returned value is correct up to an additive constant
    (which is comprised of arbitrary constants as well as the log-marginal
    evidence).

    Parameters
    ----------
    error_terms : 1D ndarray of floats.
        The error terms we want to calculate the log of the joint density of.
    alt_variances : 1D ndarray of positive floats.
        Each value should represent one alternative speciific variance.
    filtered_rows_to_alts : 2D sparse array of zeros and ones.
        Each element (i, j) should denote whether row i corresponds to
        alternative j or not using one's and zero's reespectively.

    Returns
    -------
    log_first_stage : scalar.
        The log of the joint density of the error terms, up to an additive
        constant that contains the log of the normalization constant and the
        log of the other arbitrary contants from the multivariate normal
        distribution.

    References
    ----------
    Gelman, Andrew, et al. (2014). Bayesian Data Analysis, 3rd Ed. Taylor
        & Francis Group. pp. 576-578.
    """
    # Get the position in theta_tilde, at which the betas start
    beta_neg_idx = -1 * num_betas
    # Split theta_tilde into its various components
    beta = theta_tilde[beta_neg_idx:]

    # If the betas are conditionally independent given the
    # prior variances, then the covariance matrix
    # for the joint distribution of betas is diagonal and the inverse
    # of a diagonal matrix is a diagonal matrix with the inverses on
    # the diagonal. The inverses are calculated below.
    inverse_variances = 1.0 / prior_index_variances

    # Below, we implement -0.5 * (beta - mu)^T Sigma^{-1} (beta - mu) for
    # the specific case of a diagonal Sigma, Mu = 0
    log_index_coef_prior =\
        -0.5 * tt.sum(tt.mul(inverse_variances, beta**2))

    return log_index_coef_prior


def theano_log_posterior_expr(theta_tilde,
                              design_2d,
                              choice_vector,
                              num_variances,
                              num_betas,
                              rows_to_obs,
                              est_rows_to_alts,
                              hyperprior_alphas,
                              hyperprior_betas,
                              prior_index_variances,
                              total_error_array,
                              overwrite,
                              likelihood_temp,
                              overall_temp):
    """
    Creates the symbolic theano expression for the log of the posterior density
    at a given value of theta_tilde--the vector of parameters being estimated.
    Note that this function assumes we are using independent normal distribution
    priors for each alternative's distribution of normal component error terms
    in the population. It also assumes that we're using independent gamma
    distributions as the prior for the variances of distribution of error terms
    for each alternative. Lastly, it also assumes we are using normal
    distribution priors on the index coefficients.

    Parameters
    ----------
    theta_tilde
    design_2d
    choice_vector
    num_variances
    num_betas
    rows_to_obs
    est_rows_to_alts
    hyperprior_alphas
    hyperprior_betas
    prior_index_variances
    total_error_array
    overwrite
    likelihood_temp : float.
        Determines the temperature used to temper the likelihood of the
        posterior density. To calculate the regular log-posterior, pass
        `likelihood_temp == 1.0`.
    overall_temp : float.
        Determines the temperature used to temper the overall posterior density.
        The returned value will then be `(1.0 / overall_temp) * log_posterior`.
        To calculate the `log_posterior`, pass `overall_temp = 1.0`.

    Returns
    -------
    Theano Variable. Will be an expression for the log-posterior density at
    a given value of theta_tilde.
    """
    # Calculate the log-likelihood
    log_likelihood =\
        calc_mixed_mnl_log_likelihood(theta_tilde,
                                      num_variances,
                                      num_betas,
                                      design_2d,
                                      rows_to_obs,
                                      choice_vector,
                                      total_error_array,
                                      overwrite)

    # Calculate the log of the first stage prior densities
    log_first_stage =\
        log_first_stage_indep_normal_priors(theta_tilde,
                                            num_variances,
                                            num_betas,
                                            est_rows_to_alts)

    # Calculate the log of the second stage prior densities
    log_second_stage =\
        log_second_stage_inv_gammas(theta_tilde,
                                    num_variances,
                                    hyperprior_alphas,
                                    hyperprior_betas)

    # Calculate the log of the prior on the index coefficients
    log_index_prior =\
        log_index_coefs_normal_priors(theta_tilde,
                                      num_betas,
                                      prior_index_variances)

    # Calculate the log-jacobian
    log_jacobian =\
        log_jacobian_log_transform(theta_tilde, num_variances)

    # Sum all of the terms
    log_posterior = ((1.0 / likelihood_temp) * log_likelihood +
                     log_first_stage +
                     log_second_stage +
                     log_index_prior +
                     log_jacobian)

    # Account for any tempering being done overall
    tempered_log_posterior = (1.0 / overall_temp) * log_posterior
    return tempered_log_posterior


def make_log_posterior_functions(design_2d,
                                 choice_vector,
                                 num_variances,
                                 num_betas,
                                 rows_to_obs,
                                 est_rows_to_alts,
                                 hyperprior_alpha,
                                 hyperprior_beta,
                                 prior_index_variances,
                                 alt_ids,
                                 ref_alt_id,
                                 theano_log_posterior,
                                 theano_log_post_grad,
                                 theano_log_post_hessian):
    """
    Creates python functions that accepts a single input,
    `theta_tilde`, and returns the log-posterior, the gradient
    of the log-posterior, and the hessian of the log-posterior.

    Parameters
    ----------
    design_2d : 2D ndarray.
        Should contain the explanatory variables for each
        alternative for each choice situation in the dataset.
    choice_vector : 2D ndarray of shape `(1, design.shape[0])`.
        All elements should be either ones or zeros. There should be one column
        per observation per available alternative for the given observation.
        Elements denote the alternative which is chosen by the given
        observation with a 1 and a zero otherwise.
    num_variances : int.
        Denotes the number of alternative specific variances being estimated.
    num_betas : int.
        Denotes the number of index coefficients that are being estimated.
    rows_to_obs : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).
    est_rows_to_alts : 2D sparse matrix.
        Should be the rows_to_alts sparse mapping matrix, filtered to the rows
        (i.e. observations) and columns (i.e. alternatives) whose alternative
        specific variances are being estimated.
    hyperprior_alpha : 1D ndarray of floats.
        Each element should denote the alpha parameter of the inverse gamma
        distribution being used as the prior of the alternative specific
        variance. There should be one element per alternative specific
        variance being estimated.
    hyperprior_beta : 1D ndarray of floats.
        Each element should denote the beta parameter of the inverse gamma
        distribution being used as the prior of the alternative specific
        variance. There should be one element per alternative specific
        variance being estimated.
    prior_index_variances : 1D ndarray of floats.
        Each element should reepresent a hyperprior, i.e. the variances to
        be used in the prior density for each index coefficient.
    alt_ids : 1D ndarray of ints.
        Should denote the allternative ID corresponding to each row of the
        design matrix.
    ref_alt_id : int.
        Should denote the alternative that is not having an alternative specific
        variance estimated for identifiability reasons.
    theano_log_posterior : callable.
        A compiled theano function. Should accept a 1D ndarray of parameter
        values at which the log-posterior will be calculated. Should also accept
        all of the other arguments that are passed to this constructor function.
        Should return the log-posterior density up to an additive constant.
    theano_log_post_grad : callable.
        A compiled theano function. Should accept a 1D ndarray of parameter
        values at which the hessian of the log-posterior will be calculated.
        Should also accept all of the other arguments that are passed to this
        constructor function. Should return the gradient of the log-posterior
        density.
    theano_log_post_hessian : callable.
        A compiled theano function. Should accept a 1D ndarray of parameter
        values at which the hessian of the log-posterior will be calculated.
        Should also accept all of the other arguments that are passed to this
        constructor function. Should return the hessian of the log-posterior
        density.

    Returns
    -------
    calc_log_posterior : callable.
        Accepts as inputs, an array, theta_tilde. Returns the log-posterior
        corresponding to that value of `theta_tilde`.
    """
    # Define a total_error_array that has a compatible shape with
    # the design matrix.
    total_error_array = np.zeros(design_2d.shape[0], dtype=float)

    # Define which rows are to be overwritten with the error
    # terms from theta_tilde
    overwrite = np.where(alt_ids != ref_alt_id)[0]

    # Store the default arguments for the various functions
    # Note the final two floats (1.0, 1.0) are used as default
    # tempering values. The denote a state of no tempering.
    default_args = [design_2d,
                    choice_vector,
                    num_variances,
                    num_betas,
                    rows_to_obs,
                    est_rows_to_alts,
                    hyperprior_alpha,
                    hyperprior_beta,
                    prior_index_variances,
                    total_error_array,
                    overwrite,
                    1.0,
                    1.0]

    # Define the various closures
    def calc_log_posterior(theta_tilde,
                           likelihood_temp=1.0,
                           overall_temp=1.0):
        """
        Calculates the log-posterior that corresponds to the passed value of
        `theta_tilde`.

        Parameters
        ----------
        theta_tilde : 1D ndarray.
            Contains the parameter values, at which we want to evaluate the log-
            posterior density (up to an additive constant).
        likelihood_temp : float, optional.
            Determines the temperature to be used in tempering the likelihood
            portion of the posterior density. Default == 1.0.
        overall_temp : float, optional.
            Determines the temperature to be used in tempering the the posterior
            density. Default == 1.0.

        Returns
        -------
        log_posterior : float.
            The log-posterior density, up to an additive constant (i.e. the
            normalization factor).
        """
        missing_args = (default_args[:-2] +
                        [likelihood_temp, overall_temp])
        return float(theano_log_posterior(theta_tilde,
                                          *missing_args))

    def calc_log_posterior_grad(theta_tilde):
        """
        Calculates the gradient of the log-posterior that corresponds to the
        passed value of `theta_tilde`.

        Parameters
        ----------
        theta_tilde : 1D ndarray.
            Contains the parameter values, at which we want to evaluate the log-
            posterior density (up to an additive constant).

        Returns
        -------
        log_posterior_grad : 1D ndarray of floats.
            The gradient of the log-posterior density.
        """
        return theano_log_post_grad(theta_tilde,
                                    *default_args)

    def calc_log_posterior_hessian(theta_tilde):
        """
        Calculates the hessian of the log-posterior that corresponds to the
        passed value of `theta_tilde`.

        Parameters
        ----------
        theta_tilde : 1D ndarray.
            Contains the parameter values, at which we want to evaluate the log-
            posterior density (up to an additive constant).

        Returns
        -------
        hessian : 2D ndarray.
            The hessian of the log-posterior density at `theta_tilde`.
        """
        return theano_log_post_hessian(theta_tilde,
                                       *default_args)

    return (calc_log_posterior,
            calc_log_posterior_grad,
            calc_log_posterior_hessian)
