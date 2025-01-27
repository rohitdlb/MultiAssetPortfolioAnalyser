from dash import Dash
import dash_bootstrap_components as dbc
from dashboard_controller.layout import create_layout
from dashboard_controller.callbacks import register_callbacks

def init_dashboard(server):
    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    dash_app.layout = create_layout()
    register_callbacks(dash_app)
    return dash_app