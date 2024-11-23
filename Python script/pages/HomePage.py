import dash
from dash import dcc, html, Dash, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from Data_prep import dropdown_list_fy
from Charts import evolution_bookings,materials_category_fy

# register page

register_page(__name__, name = "Yearly KPIs", path='/')


#--------------------------------------------
# Web app layout

layout = dbc.Container(
    [
        dbc.Row(
    [
        dbc.Col(
            html.Div(' Financial Year filter:', className="dropdown-label"),
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
    ],
    className = "dropdown-row"
        ), 
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='chart5',
                        figure={}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id = 'chart20',
                        figure={}
                    ),
                    width=6
                )
            ],
            className="mb-4",
        ),
    ],
    fluid=True
)

#--------------------------------------------------------------------

@callback(
    [
        Output(component_id='chart5',component_property='figure'),
        Output(component_id='chart20',component_property='figure')
    ],
    [
        Input(component_id='slct_fy', component_property='value')
    ]
)

def update_plots(slct_fy):

    fig5 = evolution_bookings(slct_fy)
    fig20 = materials_category_fy(slct_fy)

    return fig5, fig20

#--------------------------------------------------------------------
