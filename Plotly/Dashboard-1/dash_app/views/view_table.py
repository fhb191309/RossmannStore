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

##### Prep Data for Data Table
# Add Column quarter
df["quarter"] = pd.PeriodIndex(df["Date"], freq="Q")

# Convert "quarter" column to string
df["quarter"] = df["quarter"].astype(str)

# Split the "quarter" column into year and quarter components
df[["year", "quarter"]] = df["quarter"].str.split("Q", expand=True)

# Create a new column "formatted_quarter" by concatenating the year and quarter with a hyphen
df["formatted_quarter"] = df["year"] + "-" + df["quarter"]

##### Limit Page Size for Datatables to limit data being loaded
PAGE_SIZE = 100

##### Function for creating a layout for the Data Table
# input: selected_state (Input from Dropdown in app.py) 
# output: html.Div with figure
def make_view_table(selected_state):
    
    if selected_state == "Alle Bundesländer":
        # Group By "Store", "quarter" and "State", aggregate by sum of Sales
        df_table_sales = df.groupby(
            ["Store", "State", "formatted_quarter"], as_index=False
        ).agg({"Sales": "sum"})

        # Transform columns values from column "quarter" in independent columns
        df_table_sales = df_table_sales.pivot(
            index=["Store", "State"], columns="formatted_quarter", values="Sales"
        )

        # Reset the index to make "Store" and "StateName" regular columns
        df_table_sales = df_table_sales.reset_index()

    else:
        # Filter data based on selected state
        df_table_sales_filtered = df[df["State"] == selected_state]

        # Group By "Store", "quarter" and "State", aggregate by sum of Sales
        df_table_sales_filtered = df_table_sales_filtered.groupby(
            ["Store", "State", "formatted_quarter"], as_index=False
        ).agg({"Sales": "sum"})

        # Transform columns values from column "quarter" in independent columns
        df_table_sales_filtered = df_table_sales_filtered.pivot(
            index=["Store", "State"], columns="formatted_quarter", values="Sales"
        )

        # Reset the index to make "Store" and "StateName" regular columns
        df_table_sales = df_table_sales_filtered.reset_index()

    return html.Div(
        [
            html.Div(
                "Umsatz pro Quartal und Jahr",
                className="text-primary text-center fs-3",
            ),
            dash_table.DataTable(
                data=df_table_sales.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df_table_sales.columns],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action="custom",
                id="table-sorting",
                style_table={
                    "height": "300px",
                    "overflowY": "auto",
                    "overflowX": "scroll",
                },
            ),
        ]
    )
