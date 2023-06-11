# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Incorporate data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_csv('https://raw.githubusercontent.com/elvoeglo/RossmannStore/main/Plotly/group_rossmann_dataprep.csv?token=GHSAT0AAAAAACBCGRFJZAQOZB5KBJPQT3FSZEFXIHA', sep=';')

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
            id='my-range-slider',
            min=pd.Timestamp(2013, 1, 1, 0), 
            max=pd.Timestamp(2015, 7, 31, 0), 
            step=None,
            marks={
                0: '1.1.2013',
                31: '31.7.2015'
            }, 
            value=[2023-1-1, 2015-7-31]
            #updatemode='drag'
            ),
        # dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
        #                value='lifeExp',
        #                inline=True,
        #                id='radio-buttons-final')
    ]),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], width=6),

        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final'),
            dbc.Row([
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
