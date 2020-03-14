import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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

# Gapminder dataset GAPMINDER.ORG, CC-BY LICENSE
url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"


inputStock = ["FB", "GE", "AAPL", "GOOGL", "HPT", "A"]

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

df = pd.DataFrame()

for i in inputStock:
    try:
        df_ = web.DataReader(i, 'yahoo', start=start, end=end)
        df_['Symbol'] = i
        df = pd.concat([df, df_])
    except:
        print("hi")


#df = pd.read_csv(url)
#df = df.rename(index=str, columns={"pop": "population", "lifeExp": "life_expectancy", "gdpPercap": "GDP_per_capita"})
print(df.head(10))
print(list(df))
print(df.index)


# Dash app
app = dash.Dash()
#app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([
    html.H1('Dash App Basics',
    ),

    dcc.Markdown("Here's a bare bones look at an example Python Dash app."
    ),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in df.Symbol.unique()],
        multi=True,
        value=['FB']
    ),

    dcc.Graph(id='timeseries-graph')

])

@app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_graph(country_values):
    dff = df.loc[df['Symbol'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Symbol'] == Symbol].index,
            y=dff[dff['Symbol'] == Symbol]['Close'],
            mode='lines+markers',
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
    app.run_server(debug=True)
