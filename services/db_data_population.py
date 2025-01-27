from repository.db_ops import *
from utils.constants import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def processing_util(data, day_first=False, year_first=False, delta_multiplier=1):
    data.replace('%', '', inplace=True, regex=True)
    data.replace(',', '', inplace=True, regex=True)
    data['date'] = pd.to_datetime(data['date'], dayfirst=day_first, yearfirst=year_first)
    data['date'] = data['date'].dt.strftime('%Y%m%d')
    data = data.astype({'delta': 'float', 'level': 'float', 'date': 'int'})
    data['delta'] = data['delta'] * delta_multiplier / 100
    return data


def populate_factor_definition_data():
    data = pd.DataFrame(columns=['macro_factor_tag', 'type'])
    for factor in LEVEL_ONLY_MACROS:
        data.loc[len(data)] = [factor, LEVEL_FACTOR]
    for factor in ALL_DELTA_MACROS:
        data.loc[len(data)] = [factor, DELTA_FACTOR]
    write_data_to_db(data, FACTOR_DEFINITION_TABLE)


def populate_equity_indices_data():
    # Read Data from csv and write to DB
    for index in INDICES_UNIVERSE:
        data = pd.read_csv('data/indices/{}.csv'.format(index), usecols=['Date', 'Price', 'Change %'])
        data.rename(columns={'Price': 'level', 'Change %': 'delta', 'Date': 'date'}, inplace=True)
        data['ticker'] = index
        data = processing_util(data, True, False)
        write_data_to_db(data, EQUITY_INDEX_TABLE)
        logger.info(f"INSERTED Data for Equity index = {index}")


def populate_level_delta_macro_indices_data():
    # Read Data from csv and write to DB
    for macro_dict in LEVEL_DELTA_MACROS:
        day_first, macro_list = macro_dict.popitem()
        for macro in macro_list:
            data = pd.read_csv('data/macros/{}_MONTHLY.csv'.format(macro), usecols=['Date', 'Price', 'Change %'])
            data.rename(columns={'Price': 'level', 'Change %': 'delta', 'Date': 'date'}, inplace=True)
            data['macro_factor_tag'] = macro
            data = processing_util(data, day_first, False)
            write_data_to_db(data, MACRO_INDEX_TABLE)
            logger.info(f"INSERTED Data for Macro Factor = {macro}")


def populate_level_only_macros_data():
    # Read Data from csv and write to DB
    for macro_factor in LEVEL_ONLY_MACROS:
        data = pd.read_csv('data/macros/{}_MONTHLY.csv'.format(macro_factor), usecols=['level', 'date'])
        data['macro_factor_tag'] = macro_factor
        data['delta'] = data['level'] - data['level'].shift(1)
        data = processing_util(data, False, True, 100)
        write_data_to_db(data, MACRO_INDEX_TABLE)
        logger.info(f"INSERTED Data for Macro Factor = {macro_factor}")


def populate_level_delta_macros_non_monthly_data():
    # Read Data from csv and write to DB
    for macro_factor in LEVEL_DELTA_MACROS_NON_MONTHLY:
        data = pd.read_csv('data/macros/{}.csv'.format(macro_factor), usecols=['level', 'date'])
        data['macro_factor_tag'] = macro_factor
        data['delta'] = data['level'] - data['level'].shift(1) # Need to check this
        data = processing_util(data, False, True, 100)
        write_data_to_db(data, MACRO_INDEX_TABLE)
        logger.info(f"INSERTED Data for Macro Factor = {macro_factor}")


# Invoke this function on server startup
def prepare_all_databases():
    # Create DB Tables if not created already
    if not check_if_tables_already_exist():
        create_equity_indices_table()
        create_factor_definition_table()
        create_macro_indices_table()
        # Populate Data
        populate_factor_definition_data()
        populate_equity_indices_data()
        populate_level_delta_macro_indices_data()
        populate_level_only_macros_data()
        populate_level_delta_macros_non_monthly_data()