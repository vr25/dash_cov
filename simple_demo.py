from dash import Dash
import dash_html_components as html
import dash_ui as dui

my_css_urls = ["https://codepen.io/rmarren1/pen/mLqGRg.css"]

app = Dash(__name__, external_stylesheets=my_css_urls)

grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=0)

grid.add_element(col=1, row=1, width=4, height=6, element=html.Div(
    style={"background-color": "red", "height": "100%", "width": "100%"}
))

grid.add_element(col=5, row=1, width=4, height=6, element=html.Div(
    style={"background-color": "blue", "height": "100%", "width": "100%"}
))

grid.add_element(col=9, row=1, width=4, height=6, element=html.Div(
    style={"background-color": "green", "height": "100%", "width": "100%"}
))

grid.add_element(col=1, row=7, width=4, height=6, element=html.Div(
    style={"background-color": "orange", "height": "100%", "width": "100%"}
))

grid.add_element(col=5, row=7, width=4, height=6, element=html.Div(
    style={"background-color": "purple", "height": "100%", "width": "100%"}
))

grid.add_element(col=9, row=7, width=4, height=6, element=html.Div(
    style={"background-color": "yellow", "height": "100%", "width": "100%"}
))

server = app.server

app.layout = html.Div(
    dui.Layout(
        grid=grid,
    ),
    style={
        'height': '100vh',
        'width': '100vw'
    }
)

if __name__ == "__main__":
    app.run_server(debug=True)
