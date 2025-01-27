import pandas as pd

from utils.constants import INDICES_UNIVERSE, ALL_DELTA_MACROS, US_UNEMPLOYMENT, US_FED_RATES, CPI, PORT_HOLDING

NOT_APPL = 'NA'

PORT_DELTA = 'port_delta'

COEFF_TIMES_RETURN = 'factor_coeff_times_return'
FACTOR_ROLLING_RETURNS = 'factor_rolling_returns'
FACTOR_COEFF = 'factor_coeff'
FACTOR_NAME = 'factor_name'
FACTOR_UNIT = 'Factor Unit'

PERCENT_CHANGE = '% Change'
TOTAL_RETURN = 'Total return'
IDIO_RETURN = 'Idiosyncratic return'
PERCENT_TOTAL_RETURN = '% of Total Return'

factor_units_dict = {
    US_UNEMPLOYMENT: 'Diff. of UR %',
    US_FED_RATES: 'Diff. of IR %',
    CPI: 'Diff. of CPI levels',
    TOTAL_RETURN: 'AMOUNT',
    IDIO_RETURN: 'AMOUNT',
}

for index in INDICES_UNIVERSE:
    factor_units_dict[index] = PERCENT_CHANGE

for factor in ALL_DELTA_MACROS:
    factor_units_dict[factor] = PERCENT_CHANGE

def compute_portfolio_returns(allocation_df, df_indices, rolling_window, run_date):
    """
    Computes the portfolio returns based on constituents and corresponding weights
    :param allocation_df: contains holdings for each constituent
    :param df_indices: contains price levels for each constituent
    :param rolling_window: input from dashboard
    :param run_date: run date
    :return: rolling returns for portfolio assuming weight remains constant
    """
    holdings = allocation_df.index.values
    df_indices = df_indices.pivot(index='date', columns='factor', values='data')
    holding_units = {}
    for holding in holdings:
        holding_units[holding] = allocation_df.loc[holding, PORT_HOLDING] / df_indices.loc[run_date, holding]
    df_indices_returns = df_indices - df_indices.shift(rolling_window)

    for i in range(len(df_indices_returns)):
        row = df_indices_returns.iloc[i]
        for col in row.index:
            row[col] = row[col] * holding_units[col]

    df_indices_returns.dropna(axis=0, inplace=True)  # TODO: removed how='all'
    df_indices_returns[PORT_DELTA] = df_indices_returns.sum(axis=1)
    return pd.DataFrame(df_indices_returns[PORT_DELTA])


def decompose_portfolio_returns(coefficients, selected_features, independent_variables_df, port_returns, date):
    """
     Compute Y = factor_coeff * factor_return for analysis date
    :param coefficients:
    :param selected_features:
    :param independent_variables_df:
    :param port_returns:
    :param date:
    :return:
    """
    factor_contributions_df = pd.DataFrame(
        columns=[FACTOR_NAME, FACTOR_UNIT, FACTOR_COEFF, FACTOR_ROLLING_RETURNS, COEFF_TIMES_RETURN])

    explained_return = 0
    for j in range(len(coefficients)):
        fac_return = independent_variables_df.loc[date, selected_features[j]]
        fac_coeff_return = coefficients[j] * fac_return
        explained_return = explained_return + fac_coeff_return
        factor_contributions_df.loc[len(factor_contributions_df)] = {FACTOR_NAME: selected_features[j],
                                                                     FACTOR_UNIT: factor_units_dict[selected_features[j]],
                                                                     FACTOR_COEFF: coefficients[j],
                                                                     FACTOR_ROLLING_RETURNS: fac_return,
                                                                     COEFF_TIMES_RETURN: fac_coeff_return}

    # Append total and unexplained return rows as well
    total_return = port_returns.loc[date, PORT_DELTA]
    idiosyncratic_return = total_return - explained_return
    factor_contributions_df.loc[len(factor_contributions_df)] = {FACTOR_NAME: IDIO_RETURN,
                                                                 FACTOR_UNIT: factor_units_dict[IDIO_RETURN],
                                                                 FACTOR_COEFF: NOT_APPL,
                                                                 FACTOR_ROLLING_RETURNS: NOT_APPL,
                                                                 COEFF_TIMES_RETURN: idiosyncratic_return}
    factor_contributions_df.loc[len(factor_contributions_df)] = {FACTOR_NAME: TOTAL_RETURN,
                                                                 FACTOR_UNIT: factor_units_dict[TOTAL_RETURN],
                                                                 FACTOR_COEFF: NOT_APPL,
                                                                 FACTOR_ROLLING_RETURNS: NOT_APPL,
                                                                 COEFF_TIMES_RETURN: total_return}

    # Add % of Total Column
    factor_contributions_df[PERCENT_TOTAL_RETURN] = factor_contributions_df[COEFF_TIMES_RETURN] * 100 / total_return
    factor_contributions_df.sort_values(PERCENT_TOTAL_RETURN, ascending=True, inplace=True)

    return factor_contributions_df