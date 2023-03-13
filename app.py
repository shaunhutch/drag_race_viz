from dash import dash_table, html, Output, Input, Dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

drag = pd.read_csv("data/drag.csv")

wins = drag[drag["outcome"] != "NaN"].groupby("contestant").apply(lambda x: pd.Series(dict(
    participant=x.participant.sum(),
    wins=(x.outcome=="WIN").sum(),
    highs=(x.outcome=="HIGH").sum(),
    lows=(x.outcome=="LOW").sum(),
    safes=(x.outcome=="SAFE").sum(),
    btms=(x.outcome=="BTM").sum() ))).reset_index()
wins["win_percent"] = wins["wins"]/wins["participant"]
wins["high_percent"] = wins["highs"]/wins["participant"]
wins["low_percent"] = wins["lows"]/wins["participant"]
wins["safe_percent"] = wins["safes"]/wins["participant"]
wins["btm_percent"] = wins["btms"]/wins["participant"]
wins.sort_values(by="win_percent", ascending=False)

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.H1('My splashboard demo',
                style={
                    'backgroundColor': 'steelblue',
                    'padding': 20,
                    'color': 'white',
                    'margin-top': 20,
                    'margin-bottom': 20,
                    'text-align': 'center',
                    'font-size': '48px',
                    'border-radius': 3}), #, 'width': 300}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": col, "id": col, 'selectable': True if col != 'Name' else False} for col in wins.columns[:6]], 
                data=wins.to_dict('records'),
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'}],
                 style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'})
    ]),
        ])
)

if __name__ == '__main__':
    app.run_server(debug=True)