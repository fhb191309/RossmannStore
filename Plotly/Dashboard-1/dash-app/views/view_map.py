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