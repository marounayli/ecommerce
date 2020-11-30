from app import app
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

home_layout = [html.Div([html.H3("Welcome to Camunzon !"),
html.Img(src=app.get_asset_url('meme1.png'), className='meme'),
 html.Img(src=app.get_asset_url('meme2.png'), className='meme'), html.Img(src=app.get_asset_url('meme3.jpg'), className='meme'),], className='layout-container')]