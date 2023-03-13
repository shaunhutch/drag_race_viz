from dash import dash_table, html, Output, Input, Dash, dcc
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
wins["Win Percent"] = wins["wins"]/wins["participant"]
wins["High Percent"] = wins["highs"]/wins["participant"]
wins["Low Percent"] = wins["lows"]/wins["participant"]
wins["Safe Percent"] = wins["safes"]/wins["participant"]
wins["Bottom Percent"] = wins["btms"]/wins["participant"]

df_columns = ['contestant', 'wins', 'highs', 'safes', 'lows', 'btms', 'participant']
data_columns = ['Drag Queen', 'Wins', 'Highs', 'Safes', 'Lows', 'Bottoms', 'Total Participated']

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.H1('Drag Race Queen Performance',
                style={
                    'backgroundColor': 'white',
                    'padding': 20,
                    'color': 'hotpink',
                    'margin-top': 20,
                    'margin-bottom': 20,
                    'text-align': 'center',
                    'font-size': '48px',
                    'border-radius': 3}), #, 'width': 300}),
            dcc.Dropdown(
                id="dropdown",
                options =["Win Percent", "High Percent", "Safe Percent", "Low Percent", "Bottom Percent"],
                value="Win Percent",
                clearable=False,
            ),
            dcc.Graph(id="graph"),
            
            dash_table.DataTable(id='table', 
                                 page_size=5,
                                 style_data_conditional=[{
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'}],
                                 style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'})
    ]),
        ])
)

@app.callback(
    Output("graph", "figure"), 

    Input("dropdown", "value"))

def update_bar_chart(sort):
    df = wins.sort_values(by=sort, ascending = False).head(14)
    fig = px.bar(df, 
                 x = df["contestant"], 
                 y=df[sort],
                 color_discrete_sequence =['hotpink']*len(df))
    
    return fig

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input("dropdown", "value"))

def update_table(sort):
    columns=[{
      'name': col, 
      'id': df_columns[idx]
    } for (idx, col) in enumerate(data_columns)]
    data=wins.sort_values(by=sort, ascending = False).to_dict('records') 
    return data, columns

if __name__ == '__main__':
    app.run_server(debug=True)