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

# Create Column with month and year pair
df["month_year"] = pd.PeriodIndex(df["Date"], freq='M')

# Convert "month_year" column to string
df["month_year"] = df["month_year"].astype(str)

##### Prep Data for line Chart
# Group By "Date" and "StateName", aggregate by sum of Sales -> nyc.groupby (....).agg(....)
df_sales=df.groupby(["State", "month_year"], as_index=False).agg({"Sales": "sum"})

# Add Graphs for Sales per State and Month
fig_sales = px.line(df_sales, x="month_year", y="Sales", color="State")
fig_sales.update_layout(xaxis=dict(tickformat="%m-%Y"))

def make_view_line_chart():
    return html.Div([
        # Todo: Fix Graph
        html.Div('Umsatz pro Bundesland und Monat', className="text-primary text-center fs-3"),
        dcc.Graph(figure=fig_sales, id='my-first-graph-final'),
    ])
