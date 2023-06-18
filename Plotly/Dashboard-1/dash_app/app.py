# Import packages
from datetime import date
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

# import layout functions from views module
from views.view_map import make_view_map
from views.view_table import make_view_table
from views.view_line_chart import make_view_line_chart

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

##### App layout
# Components:
# dbc.Row: Div - Header
# dbc.Row: Div - Range Slider
# dbc.Row, dbc.Column: Div - Map, Div - DataTable  and Div - LineChart
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.Div(
                    "Rossmann Stores - Dashboard 1",
                    className="text-primary text-center fs-3",
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            [
                                "Alle Bundesländer",
                                "BE",  # Berlin
                                "BW",  # Baden Württemberg
                                "BY",  # Bayern
                                "HE",  # Hessen
                                "HH",  # Hamburg
                                "NW",  # Nordrhein Westfalen
                                "RP",  # Rheinland Pfalz
                                "SH",  # Schleswig Holstein
                                "SN",  # Sachsen
                                "ST",  # Sachsen Anhalt
                                "TH",  # Thüringen
                            ],  
                            "Alle Bundesländer",
                            id="dropdown",
                        ),
                    ],
                    width=6,
                ),
                dbc.Col([html.Div(id="dd-output-container")], width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(id="output-view-map"),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Div(id="output-view-table"),
                        dbc.Row([html.Div(id="output-view-line-chart")]),
                    ],
                    width=6,
                ),
            ]
        ),
    ],
    fluid=True,
)


@callback(
    Output("dd-output-container", "children"),
    Output("output-view-map", "children"),
    Output("output-view-table", "children"),
    Output("output-view-line-chart", "children"),
    Input("dropdown", "value"),
)
def update_output_dropdown(value):
    return (
        f"Deine Auswahl: {value}",
        make_view_map(value),
        make_view_table(value),
        make_view_line_chart(value),
    )


# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
