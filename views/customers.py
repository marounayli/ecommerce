import json
from app import app, API_ENDPOINTS
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import requests
import dash

customer_columns = {"address": "Address", "countryCode": "Country", "customerId": "ID", "email": "Email", "name": "Name"}
columns_order = ["customerId", "name", "email", "address", "countryCode"]
customer_dict = [{"name": customer_columns[k], "id": k} for k in columns_order]

customer_table = html.Div(dbc.Spinner(dash_table.DataTable(id='customer-table', columns= customer_dict,
style_cell_conditional=[
        {'if': {'column_id': 'customerId'},
         'width': '10%'},
        {'if': {'column_id': 'countryCode'},
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


name_input = dbc.FormGroup(
    [
        dbc.Label("Name", html_for="customer_name"),
        dbc.Input(type="text", id="customer_name", placeholder="Enter name")
    ]
)

email_input = dbc.FormGroup(
    [
        dbc.Label("Email", html_for="customer_email"),
        dbc.Input(type="email", id="customer_email", placeholder="Enter email"),
    ]
)

address_input = dbc.FormGroup(
    [
        dbc.Label("Address", html_for="customer_address"),
        dbc.Textarea(
            id="customer_address",
            placeholder="Enter address",
        ),
    ]
)

country_input = dbc.FormGroup(
    [
        dbc.Label("Country code", html_for="customer_country"),
        dbc.Input(type="number", id="customer_country", placeholder="Enter country code")
    ]
)

customer_form = dbc.Form([name_input, email_input, address_input, country_input, dbc.Button('Submit', id='customer_submit', className="mb-3", color='primary')])

create_customer = html.Div(
    [
            html.H3("Customer operations"),
        dbc.Button(
            "Create customer",
            id="customer-collapse-button",
            className="mb-3 customer-button",
            color="primary",
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([customer_form])),
            id="customer-collapse",
        ),
    ]
, className='page-card')

customers_layout = [html.Div([html.H3("Camunzon costumers"),
                           customer_table,
                           create_customer], className='layout-container')]


@app.callback(
    Output("customer-collapse", "is_open"),
    [Input("customer-collapse-button", "n_clicks")],
    [State("customer-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('customer-table', 'data'),
    [Input('location', 'pathname'),
    Input('customer_submit', 'n_clicks')],
    [State('customer_name', 'value'),
    State('customer_email', 'value'),
    State('customer_address', 'value'),
    State('customer_country', 'value')]
)
def customer_table(pathname, create, name, email, address, country):
    ctx = dash.callback_context
    if not ctx.triggered:
        pass
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'customer_submit':
            customer = {"name": name, "address": address, "email": email, "countryCode": country}
            response = requests.post(API_ENDPOINTS['CUSTOMERS']['POST'], json=customer)
        else:
            pass
    return requests.get(API_ENDPOINTS['CUSTOMERS']['GET']).json()
