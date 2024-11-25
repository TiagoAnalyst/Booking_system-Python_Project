import dash
from dash import dcc, html, Dash, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from Data_prep import dropdown_list_month,dropdown_list_fy
from Charts import materials_brought_summary, materials_brought_recycling_cat,materials_brought_non_recyclables_cat,materials_brought_DIY_cat

# register page 

register_page(__name__, name = "Waste KPIs", path='/Waste_KPIs')

layout = dbc.Container(
    [
        dbc.Row(
    [
        dbc.Col(
            html.Div('Please choose a financial year:',className="dropdown-label"),
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
            html.Div('Please choose a month:',className="dropdown-label"),
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
                        id='chart10',
                        figure={}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='chart11',
                        figure={}
                    ),
                    width=6
                )
            ],
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='chart12',
                        figure={}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='chart13',
                        figure={}
                    ),
                    width=6
                )
            ],
            className="mb-4"
        )
    ],
    fluid=True
)


#--------------------------------------------------------------------

@callback(
    [
        Output(component_id='chart10',component_property='figure'),
        Output(component_id='chart11',component_property='figure'),
        Output(component_id='chart12',component_property='figure'),
        Output(component_id='chart13',component_property='figure')
    ],    
    [
        Input(component_id='slct_fy', component_property='value'),
        Input(component_id='slct_month', component_property='value')
    ]
)

def update_plots(slct_fy,slct_month):

    fig10 = materials_brought_summary(slct_fy,slct_month)
    fig11 = materials_brought_recycling_cat(slct_fy,slct_month)
    fig12 = materials_brought_non_recyclables_cat(slct_fy,slct_month)
    fig13 = materials_brought_DIY_cat(slct_fy,slct_month)
    
    return fig10, fig11, fig12, fig13

