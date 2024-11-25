import dash
from dash import dcc, html, Dash, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from Data_prep import dropdown_list_month,dropdown_list_fy
from Charts import most_visitors_month, busiest_times_per_dayofweek

# register page 

register_page(__name__, name = "Vehicles KPIs", path='/Vehicles_KPIs')

layout = dbc.Container(
    [
        dbc.Row(
    [
        dbc.Col(
            html.Div('Financial Year filter:',className="dropdown-label"),
            width="auto"
        ),
        dbc.Col(
            dcc.Dropdown(
                id='slct_fy',
                options=[
                    {'label': x, 'value': x}
                    for x in dropdown_list_fy
                    ],
                multi=False,
                value='2021-2022' #default selection
            ),
            width=2
        ),
        dbc.Col(
            html.Div('Month filter:',className="dropdown-label"),
            width="auto",
        ),
        dbc.Col(
            dcc.Dropdown(
                id='slct_month',
                options=[{'label': x, 'value': x} for x in dropdown_list_month],
                multi=False,
                value= "January" # default selection
            ),
            width=2
        ),
    ],
    className = "dropdown-row"
        ), 
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='chart7',
                        figure={}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='chart8',
                        figure={}
                    ),
                    width=6
                )
            ],
            className="mb-4"
        ),
    ],
    fluid=True
)


#--------------------------------------------------------------------

@callback(
    [
        Output(component_id='chart7',component_property='figure'),
        Output(component_id='chart8',component_property='figure')
    ],    
    [
        Input(component_id='slct_fy', component_property='value'),
        Input(component_id='slct_month', component_property='value')
    ]
)

def update_plots(slct_fy,slct_month):

    fig7 = most_visitors_month(slct_fy,slct_month)
    fig8 = busiest_times_per_dayofweek(slct_fy,slct_month)
    
    return fig7, fig8

