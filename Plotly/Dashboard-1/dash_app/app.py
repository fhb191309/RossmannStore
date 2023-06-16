# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

# import from views
from dash_app.views.view_map import make_view_map
from dash_app.views.view_table import make_view_table
from dash_app.views.view_line_chart import make_view_line_chart

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('Rossmann Stores - Dashboard 1', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        # Todo: Replace RadoItems with RangeSlider
        dcc.RangeSlider(
            id = 'my-range-slider',
            min = 2013.0,
            max = 2015.8,
            step = 0.1,
            marks={
                2013.0: '1.1.2013',
                2013.3: '1.3.2013',
                2013.6: '1.6.2013',
                2013.9: '1.9.2013',
                2014.0: '1.1.2014',
                2014.3: '1.3.2014',
                2014.6: '1.6.2014',
                2014.9: '1.9.2014',
                2015.0: '1.1.2015',
                2015.3: '1.3.2015',
                2015.6: '1.6.2015',
                2015.8: '1.8.2015'
            }, 
            value = [2013.0, 2015.0],
            updatemode='drag',
            tooltip={'always_visible': True, 'placement': 'bottom'}
            ),
    ]),

    dbc.Row([

       make_view_map(),

        dbc.Col([

            make_view_table(),
            make_view_line_chart(),

        ], width=6),
    ]),

], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='Rossmann Stores - Dashboard 1', component_property='children'),
    Input(component_id='my-range-slider', component_property='value'),
)

# function for updating line chart
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
