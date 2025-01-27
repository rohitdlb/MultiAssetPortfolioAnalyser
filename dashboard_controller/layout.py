import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, dash_table, html

from utils.constants import INDICES_UNIVERSE

default_port = pd.DataFrame({'factor': INDICES_UNIVERSE,
                             'port_holding': [10000, 20000, 30000, 40000, 50000, 60000]})

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Portfolio Dashboard", className="text-center text-primary mb-4")),
        ]),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='port-alloc-table',
                    columns=(
                        [{'id': 'factor', 'name': 'Portfolio Constituents', 'presentation': 'dropdown'},  # need a dropdown here
                         {'id': 'port_holding', 'name': 'Holding Amount'}]
                    ),
                    data=default_port.to_dict('records'),
                    editable=True,
                    row_deletable=True,
                    dropdown={
                        'factor': {
                            'options': [
                                {'label': i, 'value': i}
                                for i in default_port['factor'].unique()
                            ]
                        }
                    },
                    style_cell={
                        'textAlign': 'center'
                    },
                    style_table={
                        'overflowY': 'auto',
                        'overflowX': 'auto'
                    },
                    css=[{
                        "selector": ".Select-menu-outer",
                        "rule": 'display : block !important'
                    }]
                ),
                html.Div(id='port-alloc-table-dropdown-container'),
                html.Button('Add Row', id='editing-rows-button', n_clicks=0),
            ], width='4'),
            dbc.Col([
                dcc.Input(
                    id='input-analysis-date',
                    placeholder='Enter analysis date in YYYYMMDD',
                    value=None,
                    type='number',
                    style={'padding': 10, 'width': '300px'},
                ),
                dcc.Input(
                    id='input-rolling-window',
                    placeholder='Enter rolling window in int value',
                    value=None,
                    type='number',
                    style={'padding': 10, 'width': '300px'}
                ),
            ], width='3'),

            html.Button('Update and Compute',
                        id='update-compute-button',
                        className="btn btn-primary mt-2",
                        n_clicks=0,
                        style={'font-size': '12px',
                               'width': '200px', 'margin-bottom': '10px',
                               'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'}),
        ]),
        html.Br(),
        html.H2("Portfolio Contributions Breakdown by Factor", className="text-center text-primary mb-4"),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='factor-contributions-table',
                    style_cell={
                        'textAlign': 'center'
                    },
                    style_table={
                        'overflowY': 'auto',
                        'overflowX': 'auto'
                    }
                ),
            ], width='10')
        ]),
        html.Br(),
        html.H2("Factor Correlations", className="text-center text-primary mb-4"),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='factor-correlations-table',
                    style_cell={
                        'textAlign': 'center'
                    },
                    style_table={
                        'overflowY': 'auto',
                        'overflowX': 'auto'
                    }
                ),
            ], width='15')
        ]),
    ], fluid=True)