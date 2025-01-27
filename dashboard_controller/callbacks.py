from dash import Input, Output, State

from services.port_calc.portfolio_calc_service import calculate_factor_holdings_and_correlations


def register_callbacks(app):
    @app.callback(
        [Output('factor-contributions-table', 'data'),
         # Output('factor-contributions-table', 'columns'),
         Output('factor-correlations-table', 'data'),
         Output('update-compute-button', 'n_clicks')],
        [Input('port-alloc-table', 'data'),
         Input('input-analysis-date', 'value'),
         Input('input-rolling-window', 'value'),
         Input('update-compute-button', 'n_clicks')]
    )
    def update_dashboard(asset_allocation, analysis_date, rolling_window, n_clicks):
        if n_clicks > 0 and asset_allocation is not None and rolling_window is not None and analysis_date is not None:
            # Fetch data and perform calculations
            factor_contributions_df, rolling_correlations_df = calculate_factor_holdings_and_correlations(asset_allocation, analysis_date, rolling_window)
            # factor_contributions_columns = [{'name': col, 'id': col, 'type' :'numeric', 'format': Format(precision=6)} for col in factor_contributions_df.columns]
            # Generate visualizations
            # contributions_fig=px.bar(factor_contributions, x='Factor', y='Contribution', title="Factor Contributions")
            return factor_contributions_df.to_dict('records'), rolling_correlations_df.to_dict('records'), 0
        return [], [], 0


    @app.callback(
        Output('port-alloc-table', 'data'),
        Input('editing-rows-button', 'n_clicks'),
        State('port-alloc-table', 'data'),
        State('port-alloc-table', 'columns'))
    def add_row(n_clicks, rows, columns):
        if n_clicks > 0:
            rows.append({c['id']: '' for c in columns})
        return rows