import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash
import dash_html_components as html 
import dash_core_components as dcc
import dash_ui as dui
from dash.dependencies import Input, Output
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go 
import pandas
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import copy

start = datetime.datetime.today() - relativedelta(days=30)
end = datetime.datetime.today()

#small-cap

df1_small = pd.read_csv("constituents_sp_600.csv", index_col=False).head(5)
inputStock1 = df1_small['Symbol']
inputSector1 = df1_small['Sector']

df1 = pd.DataFrame()

for (i, j) in zip(inputStock1, inputSector1):

    try:
        df1_ = (web.DataReader(i, 'yahoo', start=start, end=end)).reset_index()
        df1_['Symbol'] = i
        df1_['Sector'] = j
        df1 = pd.concat([df1, df1_])
    except:
        print("cannot fetch data from yahoo.")

df1['daily_returns'] = df1['Adj Close'].pct_change()
df1 = df1.dropna()
df1['daily_cum_returns'] = (df1['daily_returns'] + 1).cumprod()

df1_copy = df1.copy()
df1 = df1.groupby(['Date', 'Sector']).mean().reset_index()


#mid-cap

df1_mid = pd.read_csv("constituents_sp_400.csv", index_col=False).head(5)
inputStock2 = df1_mid['Symbol']
inputSector2 = df1_mid['Sector']

df2 = pd.DataFrame()

for (i, j) in zip(inputStock2, inputSector2):

    try:
        df2_ = (web.DataReader(i, 'yahoo', start=start, end=end)).reset_index()
        df2_['Symbol'] = i
        df2_['Sector'] = j
        df2 = pd.concat([df2, df2_])
    except:
        print("cannot fetch data from yahoo.")

df2['daily_returns'] = df2['Adj Close'].pct_change()
df2 = df2.dropna()
df2['daily_cum_returns'] = (df2['daily_returns'] + 1).cumprod()

df2_copy = df2.copy()
df2 = df2.groupby(['Date', 'Sector']).mean().reset_index()


#large-cap

df1_large = pd.read_csv("constituents_sp_500.csv", index_col=False).head(5)
inputStock3 = df1_large['Symbol']
inputSector3 = df1_large['Sector']

df3 = pd.DataFrame()

for (i, j) in zip(inputStock3, inputSector3):

    try:
        df3_ = (web.DataReader(i, 'yahoo', start=start, end=end)).reset_index()
        df3_['Symbol'] = i
        df3_['Sector'] = j
        df3 = pd.concat([df3, df3_])
    except:
        print("cannot fetch data from yahoo.")

df3['daily_returns'] = df3['Adj Close'].pct_change()
df3 = df3.dropna()
df3['daily_cum_returns'] = (df3['daily_returns'] + 1).cumprod()

df3_copy = df3.copy()
df3 = df3.groupby(['Date', 'Sector']).mean().reset_index()

# Dash app
my_css_urls = ["https://codepen.io/rmarren1/pen/mLqGRg.css"]

#app = dash.Dash(__name__) #, external_stylesheets=[dbc.themes.BOOTSTRAP])

app = dash.Dash(__name__, external_stylesheets=my_css_urls)

grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=5)

grid.add_element(col=1, row=1, width=4, height=6, element=html.Div([
                dcc.Dropdown(
                    id='sector1-dropdown',
                    options=[{'label': i, 'value': i} for i in df1.Sector.unique()],
                    multi=True,
                    value=inputSector1
                    ),

                dcc.Graph(id='graph1')
                ], #close div
                style={'border': '1px solid'}
                ))

grid.add_element(col=5, row=1, width=4, height=6, element=html.Div([
                dcc.Dropdown(
                    id='sector2-dropdown',
                    options=[{'label': i, 'value': i} for i in df2.Sector.unique()],
                    multi=True,
                    value=inputSector2
                    ),

                dcc.Graph(id='graph3')
                ], #close div
                style={'border': '1px solid'}
                ))

grid.add_element(col=9, row=1, width=4, height=6, element=html.Div([
                dcc.Dropdown(
                    id='sector3-dropdown',
                    options=[{'label': i, 'value': i} for i in df3.Sector.unique()],
                    multi=True,
                    value=inputSector3
                    ),

                dcc.Graph(id='graph5')
                ], #close div
                style={'border': '1px solid'}
                ))

grid.add_element(col=1, row=7, width=4, height=6, element=html.Div([
                dcc.Dropdown(
                    id='symbol1-dropdown',
                    options=[{'label': i, 'value': i} for i in df1_copy.Symbol.unique()],
                    multi=True,
                    value=[inputStock1[0]]
                    ),

                dcc.Graph(id='graph2')
                ], #close div
                style={'border': '1px solid'}
                ))

grid.add_element(col=5, row=7, width=4, height=6, element=html.Div([
                dcc.Dropdown(
                    id='symbol2-dropdown',
                    options=[{'label': i, 'value': i} for i in df2_copy.Symbol.unique()],
                    multi=True,
                    value=[inputStock2[0]]
                    ),

                dcc.Graph(id='graph4')
                ], #close div
                style={'border': '1px solid'}
                ))

grid.add_element(col=9, row=7, width=4, height=6, element=html.Div([
                dcc.Dropdown(
                    id='symbol3-dropdown',
                    options=[{'label': i, 'value': i} for i in df3_copy.Symbol.unique()],
                    multi=True,
                    value=[inputStock3[0]]
                    ),

                dcc.Graph(id='graph6')
                ], #close div
                style={'border': '1px solid'}
                ))


app.layout = html.Div(
    dui.Layout(
        grid=grid,
    )
)

#'width': '33%', 'display': 'inline-block',

server = app.server

app.config.suppress_callback_exceptions = True
'''
app.layout = html.Div([
html.Div([
    html.H1('Graph 1',
    ),

    dcc.Dropdown(
        id='sector1-dropdown',
        options=[{'label': i, 'value': i} for i in df1.Sector.unique()],
        multi=True,
        value=inputSector1
    ),

    dcc.Graph(id='graph1')],
    style={'width': '48%', 'display': 'inline-block'}),

html.Div([
    html.H1('Graph 2',
    ),

    dcc.Dropdown(
        id='symbol1-dropdown',
        options=[{'label': i, 'value': i} for i in df1_copy.Symbol.unique()],
        multi=True,
        value=[inputStock1[0]]
    ),

    dcc.Graph(id='graph2')],
    style={'width': '48%', 'display': 'inline-block'})

])
'''
'''
body = dbc.Container([dbc.Row([
    dbc.Row([
    dbc.Col([
        #dbc.Row([
            html.Div([
                dcc.Dropdown(
                    id='sector1-dropdown',
                    options=[{'label': i, 'value': i} for i in df1.Sector.unique()],
                    multi=True,
                    value=inputSector1
                    ),

                dcc.Graph(id='graph1')
                ], #close div
                style={'width': '33%', 'border': '1px solid'}
                ),
           # ]), #close Col

        #dbc.Row([
            html.Div([
                dcc.Dropdown(
                    id='sector2-dropdown',
                    options=[{'label': i, 'value': i} for i in df2.Sector.unique()],
                    multi=True,
                    value=inputSector2
                    ),

                dcc.Graph(id='graph3')
                ], #close div
                style={'width': '33%', 'border': '1px solid'}
                ), #close div
            #]), #close Col


        #dbc.Row([
            html.Div([
                dcc.Dropdown(
                    id='sector3-dropdown',
                    options=[{'label': i, 'value': i} for i in df3.Sector.unique()],
                    multi=True,
                    value=inputSector3
                    ),

                dcc.Graph(id='graph5')
                ], #close div
                style={'width': '33%', 'border': '1px solid'}
                ) #close div
            #]) #close Col
        ])
        ]), #close Row

    
    dbc.Row([
    dbc.Col([
        #dbc.Row([
                html.Div([

                dcc.Dropdown(
                    id='symbol1-dropdown',
                    options=[{'label': i, 'value': i} for i in df1_copy.Symbol.unique()],
                    multi=True,
                    value=[inputStock1[0]]
                    ),

                dcc.Graph(id='graph2')
                ], #close div
                style={'border': '1px solid'}
                ), #close div
            #]), #close Col

        #dbc.Row([
            html.Div([
                dcc.Dropdown(
                    id='symbol2-dropdown',
                    options=[{'label': i, 'value': i} for i in df2_copy.Symbol.unique()],
                    multi=True,
                    value=[inputStock2[0]]
                    ),

                dcc.Graph(id='graph4')
                ], #close div
                style={'border': '1px solid'}
                ), #close div
            #]), #close Col

        #dbc.Row([
            html.Div([
                dcc.Dropdown(
                    id='symbol3-dropdown',
                    options=[{'label': i, 'value': i} for i in df3_copy.Symbol.unique()],
                    multi=True,
                    value=[inputStock3[0]]
                    ),

                dcc.Graph(id='graph6')
                ], #close div
                style={'border': '1px solid'}
                ) #close div
            #]) #close Col
        ]) # close Row 
        ])  

        ]) #close Row
    ]) #close div

app.layout = html.Div([body])
'''

#small-cap
@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('sector1-dropdown', 'value')])
def update_graph1(country_values):
    #print("type(country_values): ", country_values, type(country_values))
    dff = df1.loc[df1['Sector'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Sector'] == Sector].Date,
            y=dff[dff['Sector'] == Sector]['daily_cum_returns'],
            mode='lines',
            name=Sector
        ) for Sector in dff.Sector.unique()],
        'layout': go.Layout(
            title="S&P small-cap sector-wise",
            xaxis={'title': 'Year'},
            yaxis={'title': 'Cumulative Returns'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('symbol1-dropdown', 'value')])
def update_graph2(country_values):
    #print("type(country_values): ", country_values, type(country_values))
    dff = df1_copy.loc[df1_copy['Symbol'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Symbol'] == Symbol].Date,
            y=dff[dff['Symbol'] == Symbol]['daily_cum_returns'],
            mode='lines',
            name=Symbol
        ) for Symbol in dff.Symbol.unique()],
        'layout': go.Layout(
            title="S&P small-cap company-wise",
            xaxis={'title': 'Year'},
            yaxis={'title': 'Cumulative Returns'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


#mid-cap
@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    [dash.dependencies.Input('sector2-dropdown', 'value')])
def update_graph3(country_values):
    #print("type(country_values): ", country_values, type(country_values))
    dff = df2.loc[df2['Sector'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Sector'] == Sector].Date,
            y=dff[dff['Sector'] == Sector]['daily_cum_returns'],
            mode='lines',
            name=Sector
        ) for Sector in dff.Sector.unique()],
        'layout': go.Layout(
            title="S&P mid-cap sector-wise",
            xaxis={'title': 'Year'},
            yaxis={'title': 'Cumulative Returns'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('graph4', 'figure'),
    [dash.dependencies.Input('symbol2-dropdown', 'value')])
def update_graph4(country_values):
    #print("type(country_values): ", country_values, type(country_values))
    dff = df2_copy.loc[df2_copy['Symbol'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Symbol'] == Symbol].Date,
            y=dff[dff['Symbol'] == Symbol]['daily_cum_returns'],
            mode='lines',
            name=Symbol
        ) for Symbol in dff.Symbol.unique()],
        'layout': go.Layout(
            title="S&P mid-cap company-wise",
            xaxis={'title': 'Year'},
            yaxis={'title': 'Cumulative Returns'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


#large-cap
@app.callback(
    dash.dependencies.Output('graph5', 'figure'),
    [dash.dependencies.Input('sector3-dropdown', 'value')])
def update_graph5(country_values):
    #print("type(country_values): ", country_values, type(country_values))
    dff = df3.loc[df3['Sector'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Sector'] == Sector].Date,
            y=dff[dff['Sector'] == Sector]['daily_cum_returns'],
            mode='lines',
            name=Sector
        ) for Sector in dff.Sector.unique()],
        'layout': go.Layout(
            title="S&P large-cap sector-wise",
            xaxis={'title': 'Year'},
            yaxis={'title': 'Cumulative Returns'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('graph6', 'figure'),
    [dash.dependencies.Input('symbol3-dropdown', 'value')])
def update_graph6(country_values):
    #print("type(country_values): ", country_values, type(country_values))
    dff = df3_copy.loc[df3_copy['Symbol'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Symbol'] == Symbol].Date,
            y=dff[dff['Symbol'] == Symbol]['daily_cum_returns'],
            mode='lines',
            name=Symbol
        ) for Symbol in dff.Symbol.unique()],
        'layout': go.Layout(
            title="S&P large-cap company-wise",
            xaxis={'title': 'Year'},
            yaxis={'title': 'Cumulative Returns'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)