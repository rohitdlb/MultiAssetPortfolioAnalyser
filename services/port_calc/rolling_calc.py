def roll_level_macro_factors(levels_macro_data, rolling_window):
    """
    Treating as Difference factors during rolling window calculations
    :param levels_macro_data:
    :param rolling_window:
    :return:
    """
    levels_macro_data = levels_macro_data.pivot(index='date', columns='factor', values='data')
    levels_macro_data.reset_index(inplace=True)
    levels_macro_data.set_index('date', inplace=True)
    levels_macro_data = levels_macro_data - levels_macro_data.shift(rolling_window)
    return levels_macro_data


def rolling_func_for_ratio_factors(data):
    out = 1
    for item in data:
        out = out*(1 + item)
    return out-1


def roll_delta_macro_factors(delta_macro_data, rolling_window):
    """
    Treating as Ratio factors during rolling window calculations
    :param delta_macro_data:
    :param rolling_window:
    """
    delta_macro_data = delta_macro_data.pivot(index='date', columns='factor', values='data')
    delta_macro_data.reset_index(inplace=True)
    delta_macro_data.set_index('date', inplace=True)
    # TODO:
    delta_macro_data = delta_macro_data.rolling(window=rolling_window).apply(rolling_func_for_ratio_factors)
    return delta_macro_data


def get_correlation_matrix(independent_variables_df, selected_features):
    """
    Takes input as rolled variables data and simply returns correlation matrix
    :param independent_variables_df: rolled variables data
    :param selected_features:
    :return:
    """
    selected_features_df = independent_variables_df.loc[:, selected_features]
    rolling_correlations_df = selected_features_df.corr()
    cols = list(rolling_correlations_df.columns.values)
    cols = ['factor_name'] + cols
    rolling_correlations_df['factor_name'] = rolling_correlations_df.columns.values
    rolling_correlations_df = rolling_correlations_df[cols]
    return rolling_correlations_df