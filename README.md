# Instructions to run the Application

## Installation

Get source code from Git repository

Use PyCharm or any other IDE as convenient

Inside the Project directory, run
- For Windows:

```bash 
pip install -r requirements.txt 
```

- For Mac: 

```bash 
pip3 install -r requirements.txt 
```

Run app.py via the IDE (no parameters required or environment variables )

OR

In the project directory, run in terminal
```bash 
.venv/bin/python app.py 
``` 

## Web Dashboard

Link - http://127.0.0.1:5000

## Data
Data has been sourced from multiple sources in web, namely:
- https://fred.stlouisfed.org/categories/106
- https://investing.com

## About the Indices Data
All data ranges from Jan 1st, 2001 to Jan 1st, 2025 on monthly basis. 

Data has been collated for 7 indices namely:
- Dow Jones Industrial Average(DJIA)
- NASDAQ Composite (tech & growth; 3000 stocks)
- Russel 2000 (Small Cap)
- Russel 1000 (covers 92% of US mkt cap)
- SNP500 (Top 500 US companies)
- SNP_MID_400 (SNP Top 400 mid-cap companies)
- MSCI_WRLD_GLOBAL (Global Index)

Exceptions:
- Russell 1000 data is missing for dates before 2008-12-01


## About the Macro Input Data

All data ranges from Jan 1st, 2001 to Jan 1st, 2025 on monthly basis. 
Data is available as of 1st day of the month for entire period
Data for CPI, US_DEBT, US_DEBT, US_GDP start from 1950s onwards, but data from 2001 is only used

Exceptions:
- US CPI Data available on and before Dec 1st, 2024
- US Effective FED Rates Data available on and before Dec 1st, 2024
- US Employment Data available on and before Dec 1st, 2024
- GDP Data available on quarterly basis - last data point is 2024-07-01 (not used for analysis)
- US Debt Data available yearly as of 09/30 for each year (not used for analysis)
- Bitcoin data available only since 2008 Aug 1st (not used for analysis)

