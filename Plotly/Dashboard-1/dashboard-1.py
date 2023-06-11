# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Incorporate data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_csv('https://raw.github.com/elvoeglo/RossmannStore/blob/main/Plotly/group_rossmann_dataprep.csv', sep=';')

#Add map of Germany
fig = go.Figure(go.Scattergeo())
fig.update_geos(
    visible=False, resolution=110, scope="europe",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Blue"
)
# fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})


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
        dbc.Col([
            html.Div('Umsatz pro Bundesland', className="text-primary text-center fs-3"),
            html.Div(dcc.Graph(figure=fig))
        ], width=6),

        dbc.Col([
            html.Div('Umsatz pro Quartal und Jahr', className="text-primary text-center fs-3"),
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'}),
            dbc.Row([
                html.Div('Umsatz pro Bundesland und Monat', className="text-primary text-center fs-3"),
                dcc.Graph(figure={}, id='my-first-graph-final'),
            ]),
        ], width=6),
    ]),

], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='my-range-slider', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
