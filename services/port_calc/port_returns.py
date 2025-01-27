import pandas as pd


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
        holding_units[holding] = allocation_df.loc[holding, 'port_holding'] / df_indices.loc[run_date, holding]
    df_indices_returns = df_indices - df_indices.shift(rolling_window)

    for i in range(len(df_indices_returns)):
        row = df_indices_returns.iloc[i]
        for col in row.index:
            row[col] = row[col] * holding_units[col]

    df_indices_returns.dropna(axis=0, how='all', inplace=True)
    df_indices_returns['port_delta'] = df_indices_returns.sum(axis=1)
    return pd.DataFrame(df_indices_returns['port_delta'])


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
        columns=['factor_name', 'factor_coeff', 'factor_rolling_returns', 'factor_coeff_times_return'])

    explained_return = 0
    for j in range(len(coefficients)):
        fac_return = independent_variables_df.loc[date, selected_features[j]]
        fac_coeff_return = coefficients[j] * fac_return
        explained_return = explained_return + fac_coeff_return
        factor_contributions_df.loc[len(factor_contributions_df)] = {'factor_name': selected_features[j],
                                                                     'factor_coeff': coefficients[j],
                                                                     'factor_rolling_returns': fac_return,
                                                                     'factor_coeff_times_return': fac_coeff_return}

    # Append total and unexplained return rows as well
    total_return = port_returns.loc[date, 'port_delta']
    idiosyncratic_return = total_return - explained_return
    factor_contributions_df.loc[len(factor_contributions_df)] = {'factor_name': 'Idiosyncratic return',
                                                                 'factor_coeff': 'NA',
                                                                 'factor_rolling_returns': 'NA',
                                                                 'factor_coeff_times_return': idiosyncratic_return}
    factor_contributions_df.loc[len(factor_contributions_df)] = {'factor_name': 'Total return', 'factor_coeff': 'NA',
                                                                 'factor_rolling_returns': 'NA',
                                                                 'factor_coeff_times_return': total_return}
    # Add % Column
    factor_contributions_df['% Return'] = factor_contributions_df['factor_coeff_times_return'] * 100 / total_return
    factor_contributions_df.sort_values('% Return', ascending=True, inplace=True)
    return factor_contributions_df