"""
@module:    theano_mnl_calcs.py
@name:      Bayesian MNL Calculations with Theano
@author:    Timothy Brathwaite
@summary:   Contains functions necessary for calculating choice probabilities
            and estimating Bayesian Multinomial Logit models with Theano using
            independent normal distribution priors for each index coefficient
            with mean zero.
"""
import numpy as np
from scipy.sparse import csr_matrix

# Import the theano.tensor module for use in defining
import theano
import theano.tensor as tt
from theano import sparse

from pylogit.choice_tools import create_design_matrix
from pylogit.choice_tools import create_long_form_mappings


# Define the boundary values which are not to be exceeded during computation
min_exponent_val = -700
max_exponent_val = 700

max_comp_value = 1e300
min_comp_value = 1e-300


def theano_mnl_probabilities(beta,
                             design,
                             rows_to_obs):
    """
    This function will calculate the MNL choice probabilities for each
    alternative of each choice situation in the design matrix. This function
    will be specific to ONLY the MNL model. Note this function is overly
    restrictive because Theano can only do automatic differentiation of
    functions that return scalars (so we can only return a 1D array of
    probabilities).

    Parameters
    ----------
    beta : 2D ndarray.
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

    Returns
    -------
    long_probs : 2D numpy array.
        There will be one element per observation per available alternative for
        that observation. Each element will be the probability of the
        corresponding observation being associated with that rows corresponding
        alternative.
    """
    # Calculate the systematic utility for each alternative for each individual
    sys_utilities = design.dot(beta)

    # The following commands are to guard against numeric under/over-flow
    # Note that the strange function calls are used because Theano needs
    # special commands to emulate the numpy behavior.
    sys_utilities = tt.switch(tt.lt(sys_utilities, min_exponent_val),
                              min_exponent_val,
                              sys_utilities)

    sys_utilities = tt.switch(tt.gt(sys_utilities, max_exponent_val),
                              max_exponent_val,
                              sys_utilities)

    # Exponentiate the transformed utilities
    long_exponentials = np.exp(sys_utilities)

    # Calculate \sum _j exp(V_j) for each individual.
    # Result should be a 2D array.
    individual_denominators = sparse.dot(sparse.transpose(rows_to_obs),
                                         long_exponentials)

    # Get a 2D array of the same number of rows as the design matrix, with each
    # element of each row representing the `individual_denominators` for the
    # given choice situation for the given observation.
    long_denominators = sparse.dot(rows_to_obs,
                                   individual_denominators)

    # long_probs will be of shape (num_rows, 1) Each element will provide the
    # probability of the observation associated with that row having the
    # alternative associated with that row as the observation's outcome
    long_probs = long_exponentials / long_denominators

    # Prevent negative infinity values when calculating the log-likelihood.
    long_probs = tt.switch(tt.eq(long_probs, 0), min_comp_value, long_probs)

    # Consider using an assert statement that ensures all probabilities add to
    # 1 for each choice situation.
    return long_probs


# Create the function that will calculate the log-likelihood for the MNL model
# This will be a symbolic function once we evaluate it on the Theano Tensor
# Variables.
def theano_log_likelihood_mnl_1d(beta,
                                 design,
                                 rows_to_obs,
                                 choice_vector):
    """
    This function will calculate the log-likelihood of an MNL model (and only
    an MNL model).

    Parameters
    ----------
    beta : 1D ndarray or 2D ndarray of shape `(design.shape[1], 1)`.
        All elements should by ints, floats, or longs. Should have 1 row
        for each index coefficient being estimated (i.e. num_features).
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

    Returns
    -------
    log_likelihood : float. The log likelihood of the multinomial choice model.
    """
    # Calculate the probability of each individual choosing each available
    # alternative for that individual.
    long_probs = theano_mnl_probabilities(beta,
                                          design,
                                          rows_to_obs)

    # Calculate the log likelihood
    log_likelihood = tt.dot(choice_vector, tt.log(long_probs))

    # Note that the log-likelihood is a (1, 1) array, so summing over
    # both axes does nothing but return the value at log_likelihood[0][0]
    # This is necessary because we need to return a scalar for the
    # automatic differentiation capabilities of Theano to work.
    return log_likelihood[0][0]


def log_index_coefs_normal_priors_1d(beta,
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
    beta : 1D ndarray or 2D ndarray of shape `(design.shape[1], 1)`.
        All elements should by ints, floats, or longs. There should be one
        element per index coefficient.
    prior_index_variances : 1D ndarray of positive floats.
        Each value should represent the variance of the NORMAL distribution
        prior of the corresponding index coefficient.

    Returns
    -------
    log_index_coef_prior : scalar.
        The log of the joint prior of the index coefficients, up to an additive
        constant that contains the log of the normalization constant and the
        log of the other arbitrary contants from the multivariate normal
        distribution.

    References
    ----------
    Gelman, Andrew, et al. (2014). Bayesian Data Analysis, 3rd Ed. Taylor
        & Francis Group. pp. 576-578.
    """
    # If the betas are conditionally independent given the
    # prior variances, then the covariance matrix
    # for the joint distribution of betas is diagonal and the inverse
    # of a diagonal matrix is a diagonal matrix with the inverses on
    # the diagonal. The inverses are calculated below.
    inverse_variances = 1.0 / prior_index_variances

    # Below, we implement -0.5 * (beta - mu)^T Sigma^{-1} (beta - mu) for
    # the specific case of a diagonal Sigma and Mu = 0
    log_index_coef_prior = -0.5 * tt.dot(inverse_variances, beta**2)

    return log_index_coef_prior


def theano_log_posterior_expr_1d(beta,
                                 design_2d,
                                 rows_to_obs,
                                 choice_vector,
                                 prior_index_variances):
    """
    Creates a symbolic theano expression for the (un-normalized) log-posterior,
    given the functions many inputs.

    Parameters
    ----------
    beta : 1D ndarray or 2D ndarray of shape `(design.shape[1], 1)`.
        All elements should by ints, floats, or longs. There should be one
        element per index coefficient.
    design_2d : 2D ndarray.
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
    prior_index_variances : 1D ndarray of positive floats.
        Each value should represent the variance of the NORMAL distribution
        prior of the corresponding index coefficient.

    Returns
    -------
    log_posterior_expr : theano expression.
        A symbolic theano expression for the (un-normalzed) log-posterior,
        given the function's inputs.
    """
    # Calculate the log-likelihood
    log_likelihood = theano_log_likelihood_mnl_1d(beta,
                                                  design_2d,
                                                  rows_to_obs,
                                                  choice_vector)

    # Calculate the log of the prior on the index coefficients
    log_index_prior =\
        log_index_coefs_normal_priors_1d(beta, prior_index_variances)

    # Calculate the log-jacobian in the case of using variable transformations.
    # Note we simply use zero because we're not using any variable
    # transformations.
    log_jacobian = 0

    # Sum all of the terms
    log_posterior = log_likelihood + log_index_prior + log_jacobian

    return log_posterior


def theano_log_likelihood_mnl_2d(beta,
                                 design,
                                 rows_to_obs,
                                 choice_vector):
    """
    This function will calculate the log-likelihood of an MNL model (and only
    an MNL model).

    Parameters
    ----------
    beta : 2D ndarray.
        All elements should by ints, floats, or longs. Should have 1 row
        for each index coefficient being estimated (i.e. num_features).
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
        observation with a 1 and a zero otherwise. The dtype should be 'int'.

    Returns
    -------
    log_likelihood : float. The log likelihood of the multinomial choice model.
    """
    # Calculate the probability of each individual choosing each available
    # alternative for that individual.
    long_probs = theano_mnl_probabilities(beta,
                                          design,
                                          rows_to_obs)

    # Calculate the log likelihood
    log_likelihood = tt.dot(choice_vector, tt.log(long_probs))

    # Note that the log-likelihood should be a 2D array of shape
    # (1, beta.shape[1]).
    return log_likelihood.ravel()


def log_index_coefs_normal_priors_2d(beta,
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
    beta : 2D ndarray.
        All elements should by ints, floats, or longs. There should be one
        element per index coefficient.
    prior_index_variances : 1D ndarray of positive floats.
        Each value should represent the variance of the NORMAL distribution
        prior of the corresponding index coefficient.

    Returns
    -------
    log_index_coef_prior : scalar.
        The log of the joint prior of the index coefficients, up to an additive
        constant that contains the log of the normalization constant and the
        log of the other arbitrary contants from the multivariate normal
        distribution.

    References
    ----------
    Gelman, Andrew, et al. (2014). Bayesian Data Analysis, 3rd Ed. Taylor
        & Francis Group. pp. 576-578.
    """
    # If the betas are conditionally independent given the
    # prior variances, then the covariance matrix
    # for the joint distribution of betas is diagonal and the inverse
    # of a diagonal matrix is a diagonal matrix with the inverses on
    # the diagonal. The inverses are calculated below.
    inverse_variances = tt.shape_padleft(1.0 / prior_index_variances)

    # Below, we implement -0.5 * (beta - mu)^T Sigma^{-1} (beta - mu) for
    # the specific case of a diagonal Sigma and Mu = 0
    log_index_coef_prior = -0.5 * tt.dot(inverse_variances, beta**2)

    return log_index_coef_prior.ravel()


def theano_log_posterior_expr_2d(beta,
                                 design_2d,
                                 rows_to_obs,
                                 choice_vector,
                                 prior_index_variances):
    """
    Creates a symbolic theano expression for the (un-normalized) log-posterior,
    given the functions many inputs.

    Parameters
    ----------
    beta : 2D ndarray.
        All elements should by ints, floats, or longs. There should be one
        element per index coefficient.
    design_2d : 2D ndarray.
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
        observation with a 1 and a zero otherwise. The dtype should be 'int'.
    prior_index_variances : 1D ndarray of positive floats.
        Each value should represent the variance of the NORMAL distribution
        prior of the corresponding index coefficient.

    Returns
    -------
    log_posterior_expr : theano expression.
        A symbolic theano expression for the 1D ndarray of (un-normalzed)
        log-posteriors, given the function's inputs.
    """
    # Calculate the log-likelihood
    log_likelihood = theano_log_likelihood_mnl_2d(beta,
                                                  design_2d,
                                                  rows_to_obs,
                                                  choice_vector)

    # Calculate the log of the prior on the index coefficients
    log_index_prior =\
        log_index_coefs_normal_priors_2d(beta, prior_index_variances)

    # Calculate the log-jacobian in the case of using variable transformations.
    # Note we simply use zero because we're not using any variable
    # transformations.
    log_jacobian = 0

    # Sum all of the terms
    log_posterior = log_likelihood + log_index_prior + log_jacobian

    return log_posterior


def create_compiled_theano_funcs():
    """
    Creates and stores ssymbolic theano expressions for calculating the log
    of the posterior density, the gradient of the log-posterior, and the
    hessian of the log-posterior. Note that 2D posterior functions are also
    needed.
    """
    # Create symbolic inputs for the log-posterior function
    beta = tt.dvector("beta")
    beta_2d = tt.dmatrix("beta_2d")
    design_2d = tt.dmatrix('design')
    choice_vector = tt.lrow('choice_vector')
    rows_to_obs = sparse.csr_matrix('rows_to_obs', dtype="int64")
    prior_index_variances = tt.dvector('hyperprior_index_variances')

    # Gather all of the arguments to the log-posterior functions into lists.
    generic_args =\
        [design_2d, rows_to_obs, choice_vector, prior_index_variances]
    log_posterior_args_1d = [beta] + generic_args
    log_posterior_args_2d = [beta_2d] + generic_args

    # Create the symoblic expressions for the log-posterior,
    # log-likelihood, and probability functions.
    log_post_expr_1d = theano_log_posterior_expr_1d(*log_posterior_args_1d)
    log_like_expr_1d =\
        theano_log_likelihood_mnl_1d(*log_posterior_args_1d[:-1])

    log_post_expr_2d = theano_log_posterior_expr_2d(*log_posterior_args_2d)
    log_like_expr_2d =\
        theano_log_likelihood_mnl_2d(*log_posterior_args_2d[:-1])
    mnl_prob_expr_2d = theano_mnl_probabilities(*log_posterior_args_2d[:-2])

    # Create the symbolic function for the gradient of the log-posterior
    symbolic_log_post_grad =\
        theano.gradient.grad(log_post_expr_1d,
                             beta,
                             disconnected_inputs='ignore')
    # Create the symbolic function for the hessian of the log-posterior
    symbolic_log_post_hessian =\
        theano.gradient.hessian(log_post_expr_1d,
                                beta,
                                disconnected_inputs='ignore')

    # Compile the desired functions
    calc_log_posterior_1d =\
        theano.function(inputs=log_posterior_args_1d, outputs=log_post_expr_1d)

    calc_log_post_grad =\
        theano.function(inputs=log_posterior_args_1d,
                        outputs=symbolic_log_post_grad)

    calc_log_post_hess =\
        theano.function(inputs=log_posterior_args_1d,
                        outputs=symbolic_log_post_hessian)

    calc_log_like_1d =\
        theano.function(inputs=log_posterior_args_1d[:-1],
                        outputs=log_like_expr_1d)

    calc_mnl_prob_2d =\
        theano.function(inputs=log_posterior_args_2d[:-2],
                        outputs=mnl_prob_expr_2d)

    calc_log_posterior_2d =\
        theano.function(inputs=log_posterior_args_2d, outputs=log_post_expr_2d)

    calc_log_like_2d =\
        theano.function(inputs=log_posterior_args_2d[:-1],
                        outputs=log_like_expr_2d)

    # Gather and return the compiled functions
    compiled_funcs = {"log_posterior_1d": calc_log_posterior_1d,
                      "log_posterior_2d": calc_log_posterior_2d,
                      "log_post_grad": calc_log_post_grad,
                      "log_post_hess": calc_log_post_hess,
                      "log_like_1d": calc_log_like_1d,
                      "log_like_2d": calc_log_like_2d,
                      "mnl_probability_2d": calc_mnl_prob_2d}
    return compiled_funcs

# Compile the desired functions
COMPILED_FUNCTIONS = create_compiled_theano_funcs()


def create_convenience_mnl_prob_func(mnl_prob_func_2d, design, rows_to_obs):
    def calc_mnl_probs(coefs):
        # Ensure the index coefficients are conformable with the design matrix
        assert coefs.shape[0] == design.shape[1]

        coef_array_2d = coefs[:, None] if coefs.ndim == 1 else coefs

        probs =
            mnl_prob_func_2d(coef_array_2d, design, rows_to_obs)

        results = probs.ravel() if probs.shape[1] == 1 else probs

        return results

    return calc_mnl_probs


def create_convenience_log_posterior_func(log_post_func_1d,
                                          log_post_func_2d,
                                          design,
                                          rows_to_obs,
                                          choices_row_vec,
                                          prior_variances):
    def calc_log_posterior(coefs):
        constant_args =\
            [coefs, design, rows_to_obs, choices_row_vec, prior_variances]

        correct_func =\
            log_post_func_1d if coefs.ndim == 1 else log_post_func_2d

        return correct_func(*constant_args)

    return calc_log_posterior


def create_convenience_log_like_func(log_like_func_1d,
                                     log_like_func_2d,
                                     design,
                                     rows_to_obs,
                                     choices_row_vec):
    def calc_log_likelihood(coefs):
        constant_args = [coefs, design, rows_to_obs, choices_row_vec]

        correct_func =\
            log_like_func_1d if coefs.ndim == 1 else log_like_func_2d

        return correct_func(*constant_args)

    return calc_log_likelihood


class BayesMNL(object):
    def __init__(self,
                 dataframe,
                 alt_id_col,
                 obs_id_col,
                 choice_col,
                 specification,
                 name_dict,
                 normal_prior_variances):
        # Get the design matrix for this dataset
        design_res = create_design_matrix(dataframe,
                                          specification,
                                          alt_id_col,
                                          names=name_dict)

        # Initialize all object attributes.
        self.design = design_res[0]
        self.ind_var_names = design_res[1]
        self.alt_id_col = alt_id_col
        self.obs_id_col = obs_id_col
        self.choice_col = choice_col
        self.specification = specification
        self.alt_IDs = dataframe[alt_id_col].values
        self.choices = dataframe[choice_col].values
        self.choices_row_vec = self.choices[None, :]
        self.normal_prior_variances = normal_prior_variances
        self.rows_to_obs = None
        self.posterior_mode = None
        self.log_posterior_at_mode = None
        self.neg_log_posterior_hessian_at_mode = None

        # Get the rows_to_obs mapping matrix for this dataset.
        all_mappings =\
            create_long_form_mappings(self.data,
                                      self.obs_id_col,
                                      self.alt_id_col,
                                      choice_col=self.choice_col,
                                      nest_spec=None,
                                      mix_id_col=None,
                                      dense=False)
        self.rows_to_obs = all_mappings["rows_to_obs"]

        # Store the various functions
        compiled_prob_func = COMPILED_FUNCTIONS["mnl_probability_2d"]
        self.calc_probs =\
            create_convenience_mnl_prob_func(compiled_prob_func,
                                             self.design, self.rows_to_obs)

        return None

    def calc_log_posterior(self, coefs):
        # Ensure the index coefficients are conformable with the design matrix
        assert coefs.shape[0] == self.design.shape[1]

        log_post_func_1d = COMPILED_FUNCTIONS["log_posterior_1d"]
        log_post_func_2d = COMPILED_FUNCTIONS["log_posterior_2d"]

        args = [coefs,
                self.design,
                self.rows_to_obs,
                self.choices_row_vec,
                self.normal_prior_variances]

        correct_func =\
            log_post_func_1d if coefs.ndim == 1 else log_post_func_2d

        return correct_func(*args)

    def calc_log_likelihood(self, coefs):
        # Ensure the index coefficients are conformable with the design matrix
        assert coefs.shape[0] == self.design.shape[1]

        log_like_func_1d = COMPILED_FUNCTIONS["log_like_1d"]
        log_like_func_2d = COMPILED_FUNCTIONS["log_like_2d"]

        args = [coefs,
                self.design,
                self.rows_to_obs,
                self.choices_row_vec]

        correct_func =\
            log_like_func_1d if coefs.ndim == 1 else log_like_func_2d

        return correct_func(*args)

    def calc_mnl_probs(self, coefs):
        # Ensure the index coefficients are conformable with the design matrix
        assert coefs.shape[0] == self.design.shape[1]

        coef_array_2d = coefs[:, None] if coefs.ndim == 1 else coefs

        probs =
            mnl_prob_func_2d(coef_array_2d, design, rows_to_obs)

        results = probs.ravel() if probs.shape[1] == 1 else probs

        return results

    def calc_log_posterior_grad(self, coefs):
        assert coefs.shape[0] == self.design.shape[1]
        assert coefs.ndim == 1

        args = [coefs,
                self.design,
                self.rows_to_obs,
                self.choices_row_vec,
                self.normal_prior_variances]

        return COMPILED_FUNCTIONS["log_post_grad"](*args)

    def calc_log_posterior_hessian(self, coefs):
        assert coefs.shape[0] == self.design.shape[1]
        assert coefs.ndim == 1

        args = [coefs,
                self.design,
                self.rows_to_obs,
                self.choices_row_vec,
                self.normal_prior_variances]

        return COMPILED_FUNCTIONS["log_post_hess"](*args)

    def maximize_log_posterior(self):
        # Create an initial vector of parameters. I think using any starting
        # point is okay because I think the posterior is unimodal.
        initial_params = np.zeros(self.design.shape[1])
        # Perform an initial optimization using L-BFGS-B because it is more
        # robust to poor starting points.
        convenience_objective = lambda x: -1 * self.log_posterior(x)
        convenience_gradient = lambda x: -1 * self.log_posterior_grad(x)

        initial_results = minimize(convenience_objective,
                                   initial_params,
                                   method='L-BFGS-B',
                                   jac=convenience_gradient)

        # Perform a second optimization to fully minimize abs(norm(gradient))
        final_results = minimize(convenience_objective,
                                 initial_results["x"],
                                 method='BFGS',
                                 jac=convenience_gradient)

        # Store the posterior mode
        self.posterior_mode = final_results["x"]
        self.log_posterior_at_mode = -1 * final_results["fun"]
        self.neg_log_posterior_hessian_at_mode =\
            -1 * self.log_posterior_hessian(self.posterior_mode)
        return None
