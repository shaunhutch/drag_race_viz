from dash import Dash, dash_table, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime
import pandas as pd
import altair as alt
from vega_datasets import data


cars = data.cars()

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

collapse = html.Div(
    [
        dbc.Button(
            "Learn more",
            id="collapse-button",
            className="mb-3",
            outline=False,
            style={'margin-top': '10px',
                'width': '150px',
                'background-color': 'white',
                'color': 'steelblue'}
        ),
    ]
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
            dbc.Col([
                html.H1('My splashboard demo',
                    style={
                        'color': 'white',
                        'text-align': 'left',
                        'font-size': '48px',  #, 'width': 300}),
                        }),
               dbc.Collapse(
                    html.P("""
                        This dashboard is helping you understand x, y, and z, 
                        which are really important because a, b, c.
                        Start using the dashboard by clicking on 1, 2, 3
                        and pulling i, ii, and iii.""",
                        style={'color': 'white', 'width': '50%'}),
                    id="collapse",
        ),

                    ],
                    md=10),
                dbc.Col([collapse])

                
            ])
        ], style={'backgroundColor': 'steelblue',
                    'border-radius': 3,
                    'padding': 15,
                    'margin-top': 20,
                    'margin-bottom': 20,
                    'margin-right': 15
        })
                    
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('Global controls'),
            html.Br(),
            dcc.Dropdown(),
            html.Br(),
            dcc.Dropdown(),
            html.Br(),
            dcc.Dropdown(),
            html.Br(),
            dcc.Dropdown(),
            ],
            md=2,
            style={
                'background-color': '#e6e6e6',
                'padding': 15,
                'border-radius': 3}), 
        dbc.Col([
            dash_table.DataTable(
                id='table',
                columns=[{"name": col, "id": col, 'selectable': True if col != 'Name' else False} for col in cars.columns[:5]], 
                data=cars.to_dict('records'),
                style_cell={'padding': '5px'},
                sort_action="native",
                page_action='native',
                column_selectable="single",
                selected_columns=['Miles_per_Gallon'], 
                page_size= 10,
                filter_action='native',
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'}],
                 style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'}),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Variable distrbution', style={'fontWeight': 'bold'}),
                        dbc.CardBody(
                            html.Iframe(
                                id='histogram',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}))])]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Relation to Horsepower', style={'fontWeight': 'bold'}),
                        dbc.CardBody(
                            html.Iframe(
                                id='scatter',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}))])])
            ])
        ])
    ]),
    html.Hr(),
    html.P(f'''
    This dashboard was made by Joel, link to GitHub source.
    The data is from here and there (include links if appropriate), some copyright/license info
    Mention when the dashboard was latest updated (and data if appropriate).
    This will show the date when you last resarted the server: {datetime.now().date()}
    ''')
])
@app.callback(
    Output('histogram', "srcDoc"),
    Input('table', "derived_virtual_data"),
    Input('table', "selected_columns"))
def update_histogram(rows, selected_column):
    chart = alt.Chart(pd.DataFrame(rows)).mark_bar().encode(
        alt.X(selected_column[0], bin=True),
        alt.Y('count()'))
    return chart.properties(width=300, height=300).to_html()

@app.callback(
    Output('scatter', "srcDoc"),
    Input('table', "derived_virtual_data"),
    Input('table', "selected_columns"))
def update_scatter(rows, selected_column):
    chart2 = alt.Chart(pd.DataFrame(rows)).mark_point().encode(
        alt.X(selected_column[0]),
        alt.Y('Horsepower'),
        tooltip='Name')
    return chart2.properties(width=300, height=300).to_html()

if __name__ == '__main__':
    app.run_server(debug=True)