from dash import dash_table, html, Output, Input, Dash, dcc, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd

drag = pd.read_csv("~/data/drag.csv")

wins = drag[drag["outcome"] != "NaN"].groupby(["contestant"]).apply(lambda x: pd.Series(dict(
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
data_columns = ['Drag Queen', 'Wins', 'Highs', 'Safes', 'Lows', 'Bottoms', 'Total Episodes']

app = Dash(__name__)

server = app.server

load_figure_template(["darkly"])
app.config.external_stylesheets = [dbc.themes.DARKLY]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    'backgroundColor': 'rgb(50, 50, 50)',
}


sidebar = html.Div(
    [
        html.H6('Filters controls', 
                style={'color': 'hotpink',
                       'font-size': '35px',
                       'font-family': 'Impact'}),
        html.Br(),
        html.Label([
            html.H6('Outcome Percentage',
                    style={'color': 'hotpink',
                       'font-size': '25px',
                       'font-family': 'Impact'}),
            dcc.RadioItems(
                id="outcome",
                options =["Win Percent", "High Percent", "Safe Percent", "Low Percent", "Bottom Percent"],
                value ="Win Percent",
                inline=False
            )], style={'color': 'hotpink',
                       'font-size': '18px'}),
        html.Br(),
        html.Br(),
        html.Label([
            html.H6('Drag Queen',
                    style={'color': 'hotpink',
                       'font-size': '25px',
                       'font-family': 'Impact'}),
            dcc.Dropdown(
                id="contestant",
                options =drag.sort_values(by="contestant")["contestant"].unique(),
                clearable=True,
                multi = True,
                placeholder="Select a drag queen",
            )],
                   style={
                'width': '100%'
                })
    ],
    style=SIDEBAR_STYLE,
)


content = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.Div([
                html.Img(src ='assets/logo.png', 
                         style={'height':'60%', 
                                'width':'20%',
                                'padding-left': '20px',
                                'margin-top': 20,
                                'margin-bottom': 20,}),
                html.P('Drag Race Queen Performance', 
                       style={'display': 'inline-block', 
                              'vertical-align': 'top', 
                              'padding-left': '20px',
                              'font-family': 'Impact',
                              'color': 'hotpink',
                              'font-size': '46px',
                              'margin-top': 20,
                              'margin-bottom': 20,
                              }
                )])
                    # 'backgroundColor': 'white',
                    # 'padding': 20,
                    # 'color': 'hotpink',
                    # 'margin-top': 20,
                    # 'margin-bottom': 20,
                    # 'font-size': '48px',
                    # 'border-radius': 3,
                    # })]), 
            
            ])
            
        ])
        ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graph"),
            html.Br(),
            html.Br(),
            html.Br(),
             dbc.Row([
            dbc.Col([
                dash_table.DataTable(id='table', 
                                    page_size=5,
                                    style_cell={'padding': '5px'},
                                    style_data={
                                        'backgroundColor': 'rgb(50, 50, 50)',
                                        'color': 'hotpink'},
                                    style_header={
                                        'backgroundColor': 'rgb(30, 30, 30)',
                                        'fontWeight': 'bold',
                                        'color': 'hotpink'})
                                    
    ])])
       ])
])])

app.layout = html.Div([sidebar, content])

@app.callback(
    Output("graph", "figure"), 
    Input("outcome", "value"),
    Input("contestant", "value"))


def update_bar_chart(sort, contestant):
    if contestant: 
        df = wins.query("contestant in @contestant").sort_values(by=sort, ascending = False).head(10)
        fig = px.bar(df, 
                    x = df["contestant"], 
                    y=df[sort],
                    color_discrete_sequence =['hotpink']*len(df),
                    labels={'x': 'Queen'})
    else:
        df = wins.sort_values(by=sort, ascending = False).head(10)
        fig = px.bar(df, 
                    x = df["contestant"], 
                    y=df[sort],
                    color_discrete_sequence =['hotpink']*len(df),
                    labels={"contestant": 'Queen'})
    return fig

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input("outcome", "value"),
    Input("contestant", "value"))

def update_table(sort, contestant):
    if contestant: 
        data=wins[wins.contestant.isin(contestant)].sort_values(by=sort, ascending = False).to_dict('records') 
    else:
        data=wins.sort_values(by=sort, ascending = False).to_dict('records') 
    columns=[{
      'name': col, 
      'id': df_columns[idx]
    } for (idx, col) in enumerate(data_columns)]
    return data, columns

if __name__ == '__main__':
    app.run_server(debug=True)