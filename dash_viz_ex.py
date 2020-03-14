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

suppress_callback_exceptions=True

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

inputStock = ["FB"]#, "GE"]

df = pd.DataFrame()

for i in inputStock:
	df_ = web.DataReader(i, 'yahoo', start=start, end=end)
	df_['Symbol'] = i
	df = pd.concat([df, df_])

df = df.groupby("Symbol")

print(df.get_group("FB"))

trace_close = []

for i in inputStock:
	trace_close.append(go.Scatter(x=list(df.get_group(i).index), 
						 y =list(df.get_group(i).Close),
						 name=i
))

print("trace_close: ", trace_close)


data = [trace_close]

#layout = dict(title=inputStock,	showlegend=False)

fig = dict(data=data) #, layout=layout)
print("fig: ", fig)

opts = [{'label': i, 'value': i} for i in inputStock]

app = dash.Dash(__name__)

app.layout = html.Div([
	html.H1(children="Hello World!"),
	html.Label("Dash Graph"),	

	dcc.Dropdown(
                id='opt',
                options=opts,
                value= inputStock[0]                
            ),

	dcc.Graph(id="Stock_Chart")#,	figure=fig)
		
])


@app.callback(Output('Stock_Chart', 'figure'), [Input('opt', 'value')])


def update_figure(X):

	dff = df.loc[df['Symbol'].isin(X)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Symbol'] == country]['index'],
            y=dff[dff['Symbol'] == country]['Close'],
            mode='lines+markers',
            name=country,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for Symbol in dff.Symbol.unique()],
        'layout': go.Layout(
            title="GDP over time, by country",
            xaxis={'title': 'Year'},
            yaxis={'title': 'Close'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == "__main__":
	app.run_server(debug=True)