import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash
import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input, Output
import datetime
from iexfinance.stocks import get_historical_data
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go 
import pandas
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import copy

df1 = pd.read_csv("constituents_sp_400.csv", index_col=False).head(5)
inputStock = df1['Symbol'] #["FB", "GE", "AAPL", "GOOGL", "HPT", "A"]
inputSector = df1['Sector']

start = datetime.datetime.today() - relativedelta(days=30)
end = datetime.datetime.today()

df = pd.DataFrame()

for (i, j) in zip(inputStock, inputSector):
    #print("i: ", i)
    #print("j: ", j)
    try:
        df_ = (web.DataReader(i, 'yahoo', start=start, end=end)).reset_index()
        df_['Symbol'] = i
        df_['Sector'] = j
        df = pd.concat([df, df_])
    except:
        print("hi")

df['daily_returns'] = df['Adj Close'].pct_change()
df = df.dropna()
df['daily_cum_returns'] = (df['daily_returns'] + 1).cumprod()
print(df)


df_copy = df.copy()
df = df.groupby(['Date', 'Sector']).mean().reset_index()

# Dash app
app = dash.Dash()

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dbc.Row([html.Div([
    html.H1('Graph 1',
    ),

    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': i, 'value': i} for i in df.Sector.unique()],
        multi=True,
        value=inputSector
    ),

    dcc.Graph(id='graph1')],
    style={'width': '48%', 'display': 'inline-block'})
        ]),

    dbc.Row([html.Div([
    html.H1('Graph 2',
    ),

    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': i, 'value': i} for i in df_copy.Symbol.unique()],
        multi=True,
        value=[inputStock[0]]
    ),

    dcc.Graph(id='graph2')],
    style={'width': '48%', 'display': 'inline-block'})
    ])
            
]
)


'''
app.layout = html.Div([
html.Div([
    html.H1('Graph 1',
    ),

    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': i, 'value': i} for i in df.Sector.unique()],
        multi=True,
        value=inputSector
    ),

    dcc.Graph(id='graph1')],
    style={'width': '48%', 'display': 'inline-block'}),

html.Div([
    html.H1('Graph 2',
    ),

    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': i, 'value': i} for i in df_copy.Symbol.unique()],
        multi=True,
        value=[inputStock[0]]
    ),

    dcc.Graph(id='graph2')],
    style={'width': '48%', 'display': 'inline-block'})

])
'''
@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('sector-dropdown', 'value')])
def update_graph1(country_values):
    print("type(country_values): ", country_values, type(country_values))
    dff = df.loc[df['Sector'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Sector'] == Sector].Date,
            y=dff[dff['Sector'] == Sector]['daily_cum_returns'],
            mode='lines',
            name=Sector
        ) for Sector in dff.Sector.unique()],
        'layout': go.Layout(
            title="GDP over time, by country",
            xaxis={'title': 'Year'},
            yaxis={'title': 'GDP Per Capita'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('symbol-dropdown', 'value')])
def update_graph2(country_values):
    print("type(country_values): ", country_values, type(country_values))
    dff = df_copy.loc[df_copy['Symbol'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Symbol'] == Symbol].Date,
            y=dff[dff['Symbol'] == Symbol]['daily_cum_returns'],
            mode='lines',
            name=Symbol
        ) for Symbol in dff.Symbol.unique()],
        'layout': go.Layout(
            title="GDP over time, by country",
            xaxis={'title': 'Year'},
            yaxis={'title': 'GDP Per Capita'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
