# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

##### Incorporate data
# Convert 'Date' from object to Date
df = pd.read_csv("group_rossmann_dataprep.csv", sep=";")
df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")

# Create Column with month and year pair
df["month_year"] = pd.PeriodIndex(df["Date"], freq="M")

# Convert "month_year" column to string
df["month_year"] = df["month_year"].astype(str)

##### Function for creating a layout for the Line Chart
# input: selected_state (Input from Dropdown in app.py) 
# output: html.Div with figure
def make_view_line_chart(selected_state):
    
    if selected_state == "Alle Bundesländer":
        # Group By "Date" and "StateName", aggregate by sum of Sales
        df_sales = df.groupby(
            ["State", "month_year"], as_index=False
            ).agg(
            {"Sales": "sum"}
        )

        # Add Graphs for Sales per State and Month
        fig_sales = px.line(df_sales, x="month_year", y="Sales", color="State")

    else:
        # Filter data based on selected state
        df_filtered = df[df["State"] == selected_state]

        # Group By "month_year", aggregate by sum of Sales
        df_sales = df_filtered.groupby(
            "month_year", as_index=False
            ).agg(
            {"Sales": "sum"}
        )

        # Add Graph for Sales per Month
        fig_sales = px.line(df_sales, x="month_year", y="Sales")

    fig_sales.update_layout(height=350, xaxis=dict(tickformat="%m-%Y"))

    return html.Div(
        [
            html.Div(
                "Umsatz pro Bundesland und Monat",
                className="text-primary text-center fs-3",
            ),
            dcc.Graph(figure=fig_sales, id="line-chart"),
        ]
    )
