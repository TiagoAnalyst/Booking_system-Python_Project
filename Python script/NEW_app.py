import dash
from dash import Dash, dcc, html, page_container, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, 
           use_pages=True, 
           external_stylesheets=[dbc.themes.SLATE, '/assets/custom.css']
           )

#define navigation bar

navbar=dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Yearly KPIs', href='/')),
        dbc.NavItem(dbc.NavLink('Monthly KPIs', href='/Detailed_KPIs')),
        dbc.NavItem(dbc.NavLink('Vehicles KPIs', href='/Vehicles_KPIs')),
        dbc.NavItem(dbc.NavLink('Waste KPIs', href='/Waste_KPIs'))
    ],
    brand = "Booking system dashboard - Recycling Centre A",
    brand_href='/',
    color="dark",
    dark=True,
)

#define footer

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.A("Tiago Santos | Github", href='https://github.com/TiagoAnalyst')),
        ],
    ),
    className='footer',
    fluid=True
)
#define layout

app.layout = html.Div([
    navbar,
    page_container,
    footer,
])

if __name__ == '__main__':
    app.run_server(debug=True)