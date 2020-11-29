from app import app
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from views.home import home_layout
from views.customers import customers_layout
from views.orders import orders_layout
from views.stock import stock_layout

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.NavItem(dbc.NavLink("Customers", href="/customers")),
        dbc.NavItem(dbc.NavLink("Stock", href="/stock")),
        dbc.NavItem(dbc.NavLink("Orders", href="/orders"))
    ],
    brand="Camunzon E-Commerce",
    brand_href="#",
    color="primary",
    dark=True,
)
app.layout = html.Div([
    dcc.Location(id='location', refresh=False),
    navbar,
    html.Div(id='page-content')
], className="container")

not_found_layout = [html.H3("404"), html.H5("Page not found")]
layout_dict = {
    '/': home_layout,
    '/home': home_layout,
    '/stock': stock_layout,
    '/orders': orders_layout,
    '/customers': customers_layout
}

@app.callback(Output('page-content', 'children'), [Input('location', 'pathname')])
def page_content_update(pathname):
    if layout_dict.get(pathname):
        return layout_dict[pathname]
    else:
        return not_found_layout


if __name__ == '__main__':
    app.run_server(debug=True)