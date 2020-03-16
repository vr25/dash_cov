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
import pandas
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import copy

df1 = pd.read_csv("small_cap_group.csv")
df1_copy = pd.read_csv("small_cap.csv") 

inputStock1 = df1_copy['Symbol']
inputSector1 = df1_copy['Sector']

df2 = pd.read_csv("mid_cap_group.csv")
df2_copy = pd.read_csv("mid_cap.csv") 

inputStock2 = df2_copy['Symbol']
inputSector2 = df2_copy['Sector']

df3 = pd.read_csv("large_cap_group.csv")
df3_copy = pd.read_csv("large_cap.csv") 

inputStock3 = df3_copy['Symbol']
inputSector3 = df3_copy['Sector']

# Dash app
my_css_urls = ["https://codepen.io/rmarren1/pen/mLqGRg.css"]

app = dash.Dash(__name__, external_stylesheets=my_css_urls)

grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=5)

grid.add_element(col=1, row=1, width=4, height=6, element=html.Div([
                dcc.Dropdown(
                    id='sector1-dropdown',
                    options=[{'label': i, 'value': i} for i in df1.Sector.unique()],
                    multi=True,
                    value=inputSector1.unique()
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
                    value=inputSector2.unique()
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
                    value=inputSector3.unique()
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
        grid=grid
    )
)

server = app.server

app.config.suppress_callback_exceptions = True



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