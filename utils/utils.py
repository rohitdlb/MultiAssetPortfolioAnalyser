from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_dates(analysis_date, no_observations_regression, rolling_window):
    """
    Adjusts given date to 1st of month and pushes back
    :param analysis_date:
    :param no_observations_regression:
    :param rolling_window:
    :return start_date, end_date:
    """
    # Get nearest 1st of month date
    str_date = str(analysis_date)
    datetime_obj = datetime(year=int(str_date[0:4]), month=int(str_date[4:6]), day=1)
    end_date = int(datetime_obj.strftime('%Y%m%d'))
    start_date = datetime_obj - relativedelta(months=no_observations_regression + rolling_window - 1)
    start_date = int(start_date.strftime('%Y%m%d'))
    return start_date, end_date

