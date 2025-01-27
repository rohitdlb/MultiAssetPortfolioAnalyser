import logging

import pandas as pd

from repository.db_ops import get_macro_factors_data, get_equity_indices_level_data, \
    get_equity_indices_data
from services.port_calc.port_returns import compute_portfolio_returns, decompose_portfolio_returns
from services.port_calc.regression_model import run_regression
from services.port_calc.rolling_calc import roll_level_macro_factors, roll_delta_macro_factors, get_correlation_matrix
from utils.constants import INDICES_UNIVERSE, LEVEL_ONLY_MACROS, ALL_DELTA_MACROS
from utils.utils import get_dates

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

no_observations_regression = 180
observations_start_date = 20010101


def calculate_factor_holdings_and_correlations(allocations, analysis_date, rolling_window):
    """
    Receives request from dashboard callback
    :param allocations: [{'factor': 'A', 'port_holding': 20}, {'factor': 'B', 'port_holding': 30}, {'factor': 'C', 'port_holding': 50}]
    :param analysis_date: YYYYMMDD format
    :param rolling_window: an integer value
    :return: factor_contributions_df, rolling_correlations_df
    """

    logger.info(f'Received request from dashboard callback for analysis date: {analysis_date}, rolling window: {rolling_window} and allocations: {allocations}')
    # Get required dates for computation
    start_date, end_date = get_dates(analysis_date, no_observations_regression, rolling_window)

    # Get Equity Indices Level Data
    allocation_df = pd.DataFrame(allocations)
    list_indices = allocation_df['factor'].values.tolist()
    allocation_df.set_index('factor', inplace=True)
    indices_df = get_equity_indices_level_data(list_indices, start_date, end_date)

    # Compute portfolio returns; acts as Y for regression model
    port_returns = compute_portfolio_returns(allocation_df, indices_df, rolling_window, end_date)


    # Get Macro factors data - acts as X for regression model

    # Get rolled data for Level factors
    levels_macro_data = get_macro_factors_data(LEVEL_ONLY_MACROS, start_date, end_date)
    levels_macro_data = roll_level_macro_factors(levels_macro_data, rolling_window)

    # Get all indices data
    # TODO:
    all_indices_df = get_equity_indices_data(INDICES_UNIVERSE, start_date, end_date)

    # Get rolled data for delta factors
    # TODO:
    delta_macro_data = get_macro_factors_data(ALL_DELTA_MACROS, start_date, end_date)
    delta_macro_data = pd.concat([delta_macro_data, all_indices_df], ignore_index=True) # merging all ratio factor data
    delta_macro_data = roll_delta_macro_factors(delta_macro_data, rolling_window)

    # Merge all independent variables ; Drop rows where all are NaN
    independent_variables_df = delta_macro_data.merge(levels_macro_data, left_index=True, right_index=True)
    independent_variables_df.dropna(axis=0, inplace=True)     # removed how='all'

    # Run Regression here
    logger.info(f'Shape of Train Data: {independent_variables_df.shape}')
    logger.info(f'Shape of Target Data: {port_returns.shape}')
    coefficients, selected_features = run_regression(port_returns, independent_variables_df)

    # Get portfolio returns decomposition
    factor_contributions_df = decompose_portfolio_returns(coefficients, selected_features, independent_variables_df, port_returns, end_date)

    # Get rolling correlations
    rolling_correlations_df = get_correlation_matrix(independent_variables_df, selected_features)
    return factor_contributions_df, rolling_correlations_df