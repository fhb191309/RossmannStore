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

##### Prep Data for Data Table
# Add Column quarter
df_table = df
df_table["quarter"] = pd.PeriodIndex(df_table["Date"], freq='Q')

# Convert "quarter" column to string
df_table["quarter"] = df_table["quarter"].astype(str)

# Split the "quarter" column into year and quarter components
df_table[["year", "quarter"]] = df_table["quarter"].str.split("Q", expand=True)

# df_table["quarter"] = df_table["quarter"].strftime('%Y-%m-%d')
# Create a new column "formatted_quarter" by concatenating the year and quarter with a hyphen
df_table["formatted_quarter"] = df_table["year"] + "-" + df_table["quarter"]

# Group By "Store", "quarter" and "State", aggregate by sum of Sales -> nyc.groupby (....).agg(....)
df_table_sales = df_table.groupby(["Store", "State", "formatted_quarter"], as_index=False).agg({"Sales": "sum"})

# Transform columns values from column "quarter" in independent columns
df_table_sales = df_table_sales.pivot(index=["Store", "State"], columns='formatted_quarter', values='Sales')

# Reset the index to make "Store" and "StateName" regular columns
df_table_sales = df_table_sales.reset_index()

##### Limit Page Size for Datatables to limit data being loaded
PAGE_SIZE = 10

def make_view_table():
    return html.Div([
        html.Div('Umsatz pro Quartal und Jahr', className="text-primary text-center fs-3"),
        dash_table.DataTable(
            df_table_sales.to_dict('records'),
            columns=[
                {'name': i, 'id': i} for i in df_table_sales.columns
            ],

            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',

            sort_action='custom',
            sort_mode='single',
            sort_by=[],

            id='table-multicol-sorting',
            style_table={'overflowX': 'scroll'}
        )
    ])

# Add controls to build the interaction
@callback(
    Output('table-multicol-sorting', 'data'),
    Input('table-multicol-sorting', "page_current"),
    Input('table-multicol-sorting', "page_size"),
    Input('table-multicol-sorting', "sort_by")
)
# Function for updating data table
def update_table(page_current, page_size, sort_by):
    if len(sort_by):
        dff = df_table_sales.sort_values(
            [col['name'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = df_table_sales

    return dff.iloc[
        page_current * page_size: (page_current + 1) * page_size
    ].to_dict('records')
