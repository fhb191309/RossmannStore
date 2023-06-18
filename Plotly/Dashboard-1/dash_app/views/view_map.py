# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
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

# Group By State and StateName, aggregate by sum of Sales -> nyc.groupby (....).agg(....)
df_sales=df.groupby(["State", "StateName"], as_index=False).agg({"Sales": "sum"})

# # Add map of Germany
# fig_map = px.choropleth_mapbox(
#         data_frame = df_sales, 
#         geojson = bundeslaender, 
#         featureidkey = 'properties.id', 
#         locations = 'State', 
#         color = 'Sales',
#         hover_name = 'StateName',
#         color_continuous_scale = "Teal",
#         range_color = (200000000, 1800000000),
#         mapbox_style = "carto-positron",
#         zoom = 5.2, 
#         center = {"lat": 51.165691, "lon": 10.451526},
#         opacity = 0.8,
#         labels = {'Sales':'Sales rate'}
#     )
# fig_map.update_layout(height=780, width = 900, margin={"r":0,"t":0,"l":0,"b":0})
# fig_map.update_traces(marker_line_width = 0.3, marker_line_color = 'black')

def make_view_map(selected_state):

    # Filter data based on selected state
    if selected_state == "Alle Bundesländer":
        df_sales_filtered = df_sales.copy()
    else:
        df_sales_filtered = df_sales[df_sales["State"] == selected_state]

    # Add map of Germany
    fig_map_filtered = px.choropleth_mapbox(
        data_frame=df_sales_filtered,
        geojson=bundeslaender,
        featureidkey='properties.id',
        locations='State',
        color='Sales',
        hover_name='StateName',
        color_continuous_scale="Teal",
        range_color=(200000000, 1800000000),
        mapbox_style="carto-positron",
        zoom=5.2,
        center={"lat": 51.165691, "lon": 10.451526},
        opacity=0.8,
        labels={'Sales': 'Sales rate'}
    )
    fig_map_filtered.update_layout(height=700, width=700, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_map_filtered.update_traces(marker_line_width=0.3, marker_line_color='black')

    return html.Div([
        html.Div('Umsatz pro Bundesland', className="text-primary text-center fs-3"),
        html.Div(dcc.Graph(figure=fig_map_filtered), id = 'map-graph')
    ])
