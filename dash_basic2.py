import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from textwrap import dedent

# Gapminder dataset GAPMINDER.ORG, CC-BY LICENSE
url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
df = pd.read_csv(url)
df = df.rename(index=str, columns={"pop": "population",
                                   "lifeExp": "life_expectancy",
                                   "gdpPercap": "GDP_per_capita"})
print(df.head(50))

# Dash app
app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([
    html.H1('Dash App Basics',
    ),

    dcc.Markdown("Here's a bare bones look at an example Python Dash app."
    ),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in df.country.unique()],
        multi=True,
        value=['Australia']
    ),

    dcc.Graph(id='timeseries-graph')

])

@app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_graph(country_values):
    dff = df.loc[df['country'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['country'] == country]['year'],
            y=dff[dff['country'] == country]['GDP_per_capita'],
            text="Continent: " +
                  f"{dff[dff['country'] == country]['continent'].unique()[0]}",
            mode='lines+markers',
            name=country,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for country in dff.country.unique()],
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