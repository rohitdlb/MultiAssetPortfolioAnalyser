import logging

from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def model_metrics(y_train, y_pred, n, p):
    mse = mean_squared_error(y_train, y_pred)
    logger.info(f'Mean Squared Error: {mse}')

    r2_score_new = r2_score(y_train, y_pred)
    logger.info(f'R2 Score: {r2_score_new}')

    adj_R2 = 1 - ((1 - r2_score_new) * (n - 1) / (n - p - 1))
    logger.info(f'Adjusted R2: {adj_R2}')


def run_regression(port_returns, independent_variables_df):
    """
    Runs linear regression after variable selection
    :param port_returns: Y variables dataframe
    :param independent_variables_df: X variables dataframe
    :return: coefficients and selected features
    """

    x_train = independent_variables_df.to_numpy()
    y_train = port_returns['port_delta'].to_numpy()

    # Use SFS to perform stepwise feature selection
    sfs = SequentialFeatureSelector(LinearRegression(fit_intercept=True), direction='forward', cv=5, scoring='r2')
    sfs.fit(x_train, y_train)

    # Get selected features
    feature_idx = sfs.get_support(indices=True)
    all_features = independent_variables_df.columns.values
    selected_features = all_features[feature_idx]
    logger.info(f"Selected features = {selected_features}")

    # Get new train with selected features only
    x_train_sfs = sfs.transform(x_train)

    # Run linear regression only on selected features
    model_final = LinearRegression(fit_intercept=True)
    model_final.fit(x_train_sfs, y_train)

    # Predict the target values on the testing set
    y_pred = model_final.predict(x_train_sfs)

    # Get model metrics
    model_metrics(y_train, y_pred, x_train_sfs.shape[0], x_train_sfs.shape[1])

    return model_final.coef_, selected_features