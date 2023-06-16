# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
# from urllib.request import urlopen
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import geojson
# import json

# Load GeoJSON file from Github
# Author: Francesco Schwarz
# source: https://github.com/isellsoap/deutschlandGeoJSON
with open('2_hoch.geo.json') as b:
    bundeslaender = geojson.load(b)
# bundeslaender = json.load('2_hoch.geo.json')

##### Incorporate data
# Convert 'Date' from object to Date
df = pd.read_csv('group_rossmann_dataprep.csv', sep=';')
df["Date"]=pd.to_datetime(df["Date"], format="%d.%m.%Y")

##### Prep Data for line Chart
# Group By "Date" and "StateName", aggregate by sum of Sales -> nyc.groupby (....).agg(....)
df_sales=df.groupby(["StateName", "Date"], as_index=False).agg({"Sales": "sum"})

##### Prep Data for Data Table
# Add Column quarter
# Group By "Store", "quarter" and "StateName", aggregate by sum of Sales -> nyc.groupby (....).agg(....)
df_table = df
df_table["quarter"] = pd.PeriodIndex(df_table["Date"], freq='Q')
df_table_sales = df_table.groupby(["Store", "quarter", "StateName"], as_index=False).agg({"Sales": "sum"})

# Transform columns values from column "quarter" in independent columns
df_table_sales = df_table_sales.pivot(index=["Store", "StateName"], columns='quarter', values='Sales')


##### Limit Page Size for Datatables to limit data being loaded
PAGE_SIZE = 5

# Add map of Germany
# fig_map = px.choropleth(df, geojson=bundeslaender, locations='StateName', color='Sales',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 12),
#                            scope="europe",
#                            labels={'sales':'sales rate'}
#                           )
# fig_map.update_layout(height=780, width = 1080, margin={"r":0,"t":0,"l":0,"b":0})

fig_map = go.Figure(go.Scattergeo())
fig_map.update_geos(
    visible=False, resolution=110, scope="europe",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Blue"
)
fig_map.update_layout(height=780, width = 1080, margin={"r":0,"t":0,"l":0,"b":0})

# Add Graphs for Sales per State and Month
fig_sales_per_state_and_month = px.line(df_sales, x="Date", y="Sales", color="StateName")
fig_sales_per_state_and_month.update_layout(xaxis=dict(tickformat="%m-%Y"))

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
            # Todo: Fix Map
            html.Div('Umsatz pro Bundesland', className="text-primary text-center fs-3"),
            html.Div(dcc.Graph(figure=fig_map))
        ], width=6),

        dbc.Col([
            # Todo: Fix Datatable
            html.Div('Umsatz pro Quartal und Jahr', className="text-primary text-center fs-3"),
            dash_table.DataTable(
                id='table-multicol-sorting',
                columns=[
                    {"name": i, "id": i} for i in sorted(df_table_sales.columns)
                ],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action='custom',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[]
            ),
            dbc.Row([
                # Todo: Fix Graph
                html.Div('Umsatz pro Bundesland und Monat', className="text-primary text-center fs-3"),
                dcc.Graph(figure=fig_sales_per_state_and_month, id='my-first-graph-final'),
            ]),
        ], width=6),
    ]),

], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='my-range-slider', component_property='value'),
    Input('table-multicol-sorting', "page_current"),
    Input('table-multicol-sorting', "page_size"),
    Input('table-multicol-sorting', "sort_by")
)

# function for updating line chart
# def update_graph(col_chosen):
#     fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#     return fig

# Function for updating data table
def update_table(page_current, page_size, sort_by):
    print(sort_by)
    if len(sort_by):
        dff = df_table_sales.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['Store'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = df_table_sales

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('Sales')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
