import json
from logging import PlaceHolder
from app import app, API_ENDPOINTS
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import requests
import dash

order_columns = {"orderId": "ID",
                 "customerName": "Customer Name", 
                 "itemDescription": "Product Description",
                 "quantity": "Quantity",
                 "total": "Total Price",
                 "currency": "Currency"}
columns_order = ["orderId", "customerName", "itemDescription", "quantity", "total", "currency"]
order_dict = [{"name": order_columns[k], "id": k} for k in columns_order]

orders_table = html.Div(dash_table.DataTable(id='order-table', columns= order_dict,
style_cell_conditional=[
        {'if': {'column_id': 'orderId'},
         'width': '10%'},
        {'if': {'column_id': 'quantity'},
         'width': '10%'},
         {'if': {'column_id': 'currency'},
         'width': '10%'}],
style_data_conditional=[
        {'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }],
style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }, 
style_as_list_view=True,
), className='page-card')


customer_o_input = dbc.FormGroup(
    [
        dbc.Label("Customer ordering", html_for="customer_o_input"),
        dcc.Dropdown(id="customer_o_input", placeholder="Choose customer")
    ], className='form-component'
)

product_o_input = dbc.FormGroup(
    [
        dbc.Label("Product to order", html_for="product_o_input"),
        dcc.Dropdown(id='product_o_input', placeholder="Choose product")
    ], className='form-component'
)

quantity_o_input = dbc.FormGroup(
    [
        dbc.Label("Quantity needed", html_for="quantity_o_input"),
        dbc.Input(type="number", id="quantity_o_input", placeholder="Enter quantity needed"),
    ], className='form-component'
)

total_price = dbc.FormGroup(
    [
        dbc.Label("Total price"),
        dbc.Spinner(html.H4(id='total_price')),
    ], className='form-component'
)

card_o_input = dbc.FormGroup(
    [
        dbc.Label("Card Number", html_for="card_o_input"),
        dbc.Input(type="text", maxLength=14, id="card_o_input", placeholder="Enter card number"),
    ], className='form-component'
)

type_o_input = dbc.FormGroup(
    [
        dbc.Label("Type of payment"),
        dbc.RadioItems(
            options=[
                {"label": "Credit", "value": "CREDIT"},
                {"label": "Debit", "value": "DEBIT"},
            ],
            id="type_o_input",
            inline=True,
        ),
    ]
)

order_form = dbc.Form([customer_o_input, product_o_input, quantity_o_input, total_price, card_o_input, type_o_input, dbc.Button('Submit', id='order_submit', className="mb-3", color='primary')])

create_order = html.Div(
    [
            html.H3("Order operations"),
        dbc.Button(
            "Create Order",
            id="order-collapse-button",
            className="mb-3 order-button",
            color="primary",
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([order_form])),
            id="order-collapse",
        ),
    ]
, className='page-card')


orders_layout = [html.Div([html.H3("Camunzon Orders"),
                           orders_table,
                           create_order], className='layout-container')]

@app.callback(
    Output("order-collapse", "is_open"),
    [Input("order-collapse-button", "n_clicks")],
    [State("order-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('order-table', 'data'),
    [Input('location', 'pathname'),
    Input('order_submit', 'n_clicks')],
    [State("customer_o_input", "value"),
    State("product_o_input", "value"),
    State("quantity_o_input", "value"),
    State("card_o_input", "value")]
)
def stock_table(pathname, create, customerId, itemId, quantity, cardNumber):
    ctx = dash.callback_context
    if not ctx.triggered:
        pass
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'order_submit':
            order = {
                "customerId": customerId,
                "itemId": itemId,
                "quantity": quantity,
                "customerEmail": requests.get(API_ENDPOINTS['CUSTOMERS']['GET1']+str(customerId)).json()['email'],
                "cardNumber": cardNumber
            }
            print(order)
            requests.post(API_ENDPOINTS['ORDER']['POST'], json=order)
        else:
            pass
    orders = requests.get(API_ENDPOINTS['ORDER']['GET']).json()
    for order in orders:
        order["total"] = order["quantity"] * order["pricePerUnit"] 
    return orders


@app.callback(
    Output("customer_o_input", "options"),
    [Input("location", "pathname")]
)
def update_customer(pathname):
    customers = requests.get(API_ENDPOINTS['CUSTOMERS']['GET']).json()
    return [{"value": c['customerId'], "label": c['name']} for c in customers]


@app.callback(
    Output("product_o_input", "options"),
    [Input("location", "pathname")]
)
def update_product(pathname):
    products = requests.get(API_ENDPOINTS['STOCK']['GET']).json()
    return [{"value": p['productId'], "label": p['productDescription']} for p in products]

@app.callback(
    Output("total_price", "children"),
    [Input("quantity_o_input", "value"), Input("product_o_input", "value")]
)
def update_price(quantity, productId):
    if quantity and productId:
        product = requests.get(API_ENDPOINTS['STOCK']['GET1']+str(productId)).json()
        productPrice = product['pricePerUnit']
        currency = product['currency']
        return str(productPrice * quantity) + " " + currency
    else:
        dash.exceptions.PreventUpdate