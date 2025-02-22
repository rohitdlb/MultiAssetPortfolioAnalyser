# DATABASE NAMES CONST
MY_DATABASE = 'my_database'
EQUITY_INDEX_TABLE = 'equity_indices'
FACTOR_DEFINITION_TABLE = 'factor_definition'
MACRO_INDEX_TABLE = 'macro_indices'


# FACTOR DEF CONST
DELTA_FACTOR = 'delta'
LEVEL_FACTOR = 'level'


# LAYOUT Related
FACTOR = 'factor'
PORT_HOLDING = 'port_holding'

# MACRO CONST
US_FED_RATES = 'US_FED_RATES'
US_UNEMPLOYMENT = 'US_UNEMPLOYMENT'
US_DEBT_YEARLY = 'US_DEBT_YEARLY'
GDP_QUARTERLY = 'GDP_QUARTERLY'
CPI = 'CPI'
OIL_WTI = 'OIL_WTI'
GOLD_PRICE = 'GOLD_PRICE'
DXY = 'DXY'
BITCOIN = 'BITCOIN'
US_3M_YIELD = 'US_3M_YIELD'
US_2Y_YIELD = 'US_2Y_YIELD'
US_5Y_YIELD = 'US_5Y_YIELD'
US_10Y_YIELD = 'US_10Y_YIELD'
US_30Y_YIELD = 'US_30Y_YIELD'


# EQUITY INDICES CONST (all ratio factors)
NASDAQ_COMP = 'NASDAQ_COMP' # tech & growth; 3000 stocks
RUSSEL_2000 = 'RUSSEL_2000' # small cap
SNP_MID_400 = 'SNP_MID_400' # mid cap
RUSSEL_1000 = 'RUSSEL_1000' # covers 92% of US mkt cap
SNP500 = 'SNP500' # top 500 US companies
DJIA = 'DJIA' # top 30
MSCI_WRLD_GLOBAL = 'MSCI_WRLD_GLOBAL'
FTSE_100 = 'FTSE_100'
NKK_225 = 'NKK_225'
HANG_SENG = 'HANG_SENG'


# UTILITY LISTS
INDEX_LIST = [NASDAQ_COMP, RUSSEL_2000, SNP_MID_400, RUSSEL_1000, SNP500, DJIA,
              MSCI_WRLD_GLOBAL, FTSE_100, NKK_225, HANG_SENG]  # -,day

# TODO: RUSSELL_1000 to be added here
INDICES_UNIVERSE  = [NASDAQ_COMP, RUSSEL_2000, SNP_MID_400, SNP500, DJIA, MSCI_WRLD_GLOBAL]

LEVEL_DELTA_MACROS = [{False: [
    OIL_WTI,  # /,month
    BITCOIN,  # /,month
    US_3M_YIELD, US_2Y_YIELD, US_5Y_YIELD, US_10Y_YIELD, US_30Y_YIELD]  # /,month
},
    {True: [
        GOLD_PRICE,  # -,day
        DXY]  # -,day
    }
]

# TODO: need to use these as well
LEVEL_DELTA_MACROS_NON_MONTHLY = [GDP_QUARTERLY, US_DEBT_YEARLY ]

LEVEL_ONLY_MACROS = [US_UNEMPLOYMENT, US_FED_RATES, CPI]

# TODO: to add bitcoin here
YIELD_DELTA_MACROS = [US_3M_YIELD, US_2Y_YIELD, US_5Y_YIELD, US_10Y_YIELD, US_30Y_YIELD]
ALL_DELTA_MACROS = YIELD_DELTA_MACROS + [OIL_WTI, GOLD_PRICE, DXY]