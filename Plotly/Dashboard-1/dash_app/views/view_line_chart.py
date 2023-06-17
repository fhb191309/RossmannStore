# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

##### Incorporate data
# Convert 'Date' from object to Date
df = pd.read_csv('group_rossmann_dataprep.csv', sep=';')
df["Date"]=pd.to_datetime(df["Date"], format="%d.%m.%Y")

##### Prep Data for line Chart
# Group By "Date" and "StateName", aggregate by sum of Sales -> nyc.groupby (....).agg(....)
df_sales=df.groupby(["StateName", "Date"], as_index=False).agg({"Sales": "sum"})

# Add Graphs for Sales per State and Month
fig_sales_per_state_and_month = px.line(df_sales, x="Date", y="Sales", color="StateName")
fig_sales_per_state_and_month.update_layout(xaxis=dict(tickformat="%m-%Y"))

# # Initialize the app - incorporate a Dash Bootstrap theme
# external_stylesheets = [dbc.themes.CERULEAN]
# app = Dash(__name__, external_stylesheets=external_stylesheets)

def make_view_line_chart():
    return html.Div([
        # Todo: Fix Graph
        html.Div('Umsatz pro Bundesland und Monat', className="text-primary text-center fs-3"),
        dcc.Graph(figure=fig_sales_per_state_and_month, id='my-first-graph-final'),
    ])

# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='my-range-slider', component_property='value'),
)

# function for updating line chart
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig
