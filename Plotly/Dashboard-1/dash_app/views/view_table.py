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
# Group By "Store", "quarter" and "StateName", aggregate by sum of Sales -> nyc.groupby (....).agg(....)
df_table = df
df_table["quarter"] = pd.PeriodIndex(df_table["Date"], freq='Q')
df_table_sales = df_table.groupby(["Store", "quarter", "StateName"], as_index=False).agg({"Sales": "sum"})

# Transform columns values from column "quarter" in independent columns
df_table_sales = df_table_sales.pivot(index=["Store", "StateName"], columns='quarter', values='Sales')

##### Limit Page Size for Datatables to limit data being loaded
PAGE_SIZE = 5

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

def make_view_table():
    return html.Div([
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
            )
    ])

# Add controls to build the interaction
@callback(
    Output(component_id='Umsatz pro Quartal und Jahr', component_property='figure'),
    Input('table-multicol-sorting', "page_current"),
    Input('table-multicol-sorting', "page_size"),
    Input('table-multicol-sorting', "sort_by")
)

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