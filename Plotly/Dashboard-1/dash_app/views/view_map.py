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

# # Initialize the app - incorporate a Dash Bootstrap theme
# external_stylesheets = [dbc.themes.CERULEAN]
# app = Dash(__name__, external_stylesheets=external_stylesheets)

def make_view_map():
    return html.Div([
        # Todo: Fix Map
        html.Div('Umsatz pro Bundesland', className="text-primary text-center fs-3"),
        html.Div(dcc.Graph(figure=fig_map))
    ])