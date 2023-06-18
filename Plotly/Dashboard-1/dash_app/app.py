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
app.layout = dbc.Container([
    dbc.Row([
        html.Div('Rossmann Stores - Dashboard 1', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.Col([

            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(2013, 1, 1),
                max_date_allowed=date(2015, 7, 31),
                initial_visible_month=date(2013, 1, 1),
                start_date=date(2013, 1, 1),
                end_date=date(2015, 7, 31)
            ),
            html.Div(id='output-container-date-picker-range')

        ], width=6),
        dbc.Col([

            dcc.Dropdown([
                'Alle Bundesländer',
                'BE', # Berlin
                'BW', # Baden Württemberg
                'BY', # Bayern
                'HE', # Hessen
                'HH', # Hamburg
                'NW', # Nordrhein Westfalen
                'RP', # Rheinland Pfalz
                'SH', # Schleswig Holstein
                'SN', # Sachsen
                'ST', # Sachsen Anhalt
                'TH'], # Thüringen
                'Alle Bundesländer',
                id='dropdown'),
            html.Div(id='dd-output-container')

        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([

             make_view_map(),

        ], width=6),
        dbc.Col([

            make_view_table(),

            dbc.Row([

                make_view_line_chart(),

            ]),
        ], width=6),
    ]),

], fluid=True)

@callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'Deine Auswahl: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Datum: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Datum: ' + end_date_string
    if len(string_prefix) == len('Deine Auswahl: '):
        return 'Wähle zur Anzeige Datum aus!'
    else:
        return string_prefix

@callback(
    Output('dd-output-container', 'children'),
    Input('dropdown', 'value')
)
def update_output(value):
    return f'Deine Auswahl: {value}'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
