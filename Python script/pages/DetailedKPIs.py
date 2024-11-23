import dash
from dash import dcc, html, Dash, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from Data_prep import dropdown_list_month,dropdown_list_fy
from Charts import bookingsVScapacity, booking_classification, gauge_chart, average_bookings_week

# register page

register_page(__name__, name = "Detailed KPIs", path='/Detailed_KPIs')


#--------------------------------------------
# Web app layout

layout = dbc.Container(
    [
        dbc.Row(
    [
        dbc.Col(
            html.Div('Financial Year filter:', className="dropdown-label"),
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
            html.Div('Month filter',className="dropdown-label"),
            width="auto",
        ),
        dbc.Col(
            dcc.Dropdown(
                id='slct_month',
                options=[
                    {'label': x, 'value': x} 
                    for x in dropdown_list_month
                    ],
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
                        id='chart3',
                        figure={}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='chart1',
                        figure={}
                    ), 
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='chart2',
                        figure={}
                        ), 
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='chart4',
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


@callback(
    [
        Output(component_id='chart1',component_property='figure'),
        Output(component_id='chart2',component_property='figure'),
        Output(component_id='chart3',component_property='figure'),
        Output(component_id='chart4',component_property='figure')
    ],
    [
        Input(component_id='slct_fy', component_property='value'),
        Input(component_id='slct_month', component_property='value')
    ]
)
#--------------------------------------------------------------------
def update_plots(slct_fy,slct_month):

    fig1 = bookingsVScapacity(slct_fy,slct_month)
    fig2 = booking_classification(slct_fy,slct_month)
    fig3 = gauge_chart(slct_fy,slct_month)
    fig4 = average_bookings_week(slct_fy,slct_month)

    return fig1, fig2, fig3, fig4
#--------------------------------------------------------------------
