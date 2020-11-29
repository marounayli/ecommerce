import flask
import dash
import dash_bootstrap_components as dbc

server = flask.Flask('app')
app = dash.Dash('app', external_stylesheets=[dbc.themes.FLATLY], server=server)

app.config['suppress_callback_exceptions'] = True
# Setting app title
app.title = 'Camunzon'

API_ENDPOINTS = {
    'CUSTOMERS':
        {"GET" : "http://localhost:5000/customers",
        "GET1": "http://localhost:5000/customer/",
        "POST": "http://localhost:5000/customer"},
    'STOCK':
        {"GET" : "http://localhost:5000/products",
        "GET1" : "http://localhost:5000/product/",
        "POST" : "http://localhost:5000/product"},
    'ORDER':
        {"GET" : "http://localhost:5000/orders",
        "POST": "http://localhost:5000/order"},
    'PAYMENT':
        {
            "ORDERID": "http://localhost:5001/payment/by_order/"
        },
    'SHIPMENT':
    {
            "ORDERID": "http://localhost:5002/shipment/by_order/"
    },
}
