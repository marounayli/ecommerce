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

stock_columns = {"productId": "ID", "productDescription": "Description", "pricePerUnit": "Price", "currency": "Currency", "quantity": "Available",
'unitWeight': 'Unit Weight (kg)'}
columns_order = ["productId", "productDescription", "pricePerUnit", "currency", "quantity", "unitWeight"]
product_dict = [{"name": stock_columns[k], "id": k} for k in columns_order]

stock_table = html.Div(dbc.Spinner(dash_table.DataTable(id='stock-table', columns= product_dict,
style_cell_conditional=[
        {'if': {'column_id': 'productId'},
         'width': '10%'},
        {'if': {'column_id': 'currency'},
         'width': '10%'},
         {'if': {'column_id': 'pricePerUnit'},
         'width': '10%'},
         {'if': {'column_id': 'quantity'},
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
)), className='page-card')


description_input = dbc.FormGroup(
    [
        dbc.Label("Product Description", html_for="product_description"),
        dbc.Textarea(id="product_description", placeholder="Enter description")
    ], className='form-component'
)

price_input = dbc.FormGroup(
    [
        dbc.Label("Price", html_for="product_price"),
        dbc.Input(type="number", id="product_price", placeholder="Enter price"),
    ], className='form-component'
)

currency_input = dbc.FormGroup(
    [
        dbc.Label("Currency", html_for="product_currency"),
        dcc.Dropdown(
            id="product_currency",
            placeholder="Enter currency",
            multi=False,
            options=[{'value':k, 'label':k} for k in ['USD', 'LBP', 'EUR', 'GBP']]
        ),
    ], className='form-component'
)

weight_input = dbc.FormGroup(
        [
        dbc.Label("Unit weight (in kg)", html_for="product_weight"),
        dbc.Input(
            id="product_weight",
            type="number",
            placeholder="Enter unit weight"
        ),
    ], className='form-component'
)

available_input = dbc.FormGroup(
    [
        dbc.Label("Quantity available", html_for="product_available"),
        dbc.Input(type="number", id="product_available", placeholder="Enter quantity available"),
    ], className='form-component'
)


product_form = dbc.Form([description_input, price_input, currency_input, weight_input, available_input, dbc.Button('Submit', id='product_submit', className="mb-3", color='primary')])

create_product = html.Div(
    [
            html.H3("Stock operations"),
        dbc.Button(
            "Create Product",
            id="stock-collapse-button",
            className="mb-3 stock-button",
            color="primary",
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([product_form])),
            id="stock-collapse",
        ),
    ]
, className='page-card')

stock_layout = [html.Div([html.H3("Camunzon Stock"),
                           stock_table,
                           create_product], className='layout-container')]


@app.callback(
    Output("stock-collapse", "is_open"),
    [Input("stock-collapse-button", "n_clicks")],
    [State("stock-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('stock-table', 'data'),
    [Input('location', 'pathname'),
    Input('product_submit', 'n_clicks')],
    [State('product_description', 'value'),
    State('product_price', 'value'),
    State('product_currency', 'value'),
    State('product_available', 'value'),
    State('product_weight', 'value')]
)
def stock_table(pathname, create, description, price, currency, available, weight):
    ctx = dash.callback_context
    if not ctx.triggered:
        pass
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'product_submit':
            product = {"productDescription": description,
                       "pricePerUnit": price,
                        "currency": currency,
                        "quantity": available,
                        'unitWeight': weight}
            requests.post(API_ENDPOINTS['STOCK']['POST'], json=product)
        else:
            pass
    return requests.get(API_ENDPOINTS['STOCK']['GET']).json()

@app.callback(
    [Output('product_description', 'value'),
    Output('product_price', 'value'),
    Output('product_currency', 'value'),
    Output('product_available', 'value'),
    Output('product_weight', 'value')],
    [Input('product_submit', 'n_clicks')]
)
def reset_fields(n_clicks):
    return None, None, None, None, None