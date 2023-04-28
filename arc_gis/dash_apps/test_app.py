import plotly.express as px
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale
from plotly.subplots import make_subplots

from flask import Flask
import flask
import webbrowser

# import plotly.io as pio # used to read in cached file

import dash
from dash import dcc
from dash import html, ctx
from dash.dependencies import Input, Output

import plotly.graph_objects as go
from ipywidgets import widgets

import arcgis
from arcgis.gis import GIS
import os

# https://community.plotly.com/t/how-can-i-use-my-html-file-in-dash/7740/2


STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

server = Flask(__name__)
app = dash.Dash(name = __name__, server = server)

app.layout = html.Div([
#    html.Img(src='/static/test_html.html')
    html.Div(id='target',
        children=html.Embed(src='/static/test_html.html', height="500px", width="1000px"))
])

@app.server.route('/static/<resource>')
def serve_static(resource):
    # print(resource)
    return flask.send_from_directory(STATIC_PATH, resource)



# Create a GIS object, as an anonymous user for this example
# gis = GIS()

# map1 = gis.map('Paris') # Passing a place name to the constructor
#                         # will initialize the extent of the map.
# map1

# print(type(map1))

#############################
###         APP           ###
#############################
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# # https://stackoverflow.com/questions/59568510/dash-suppress-callback-exceptions-not-working
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div([
#     html.Div(id='target',
#             children=html.Iframe(src='./resources/test_html.html'))
#             #  children=html.Iframe(src='https://ucsdonline.maps.arcgis.com/home/webmap/viewer.html?useExisting=1&layers=ce3f25f987ef44b3939248e76b12d9bc'
#             #                     , height="500px", width="1000px"))
#             #  children=html.Embed(src='https://ucsdonline.maps.arcgis.com/home/webmap/viewer.html?useExisting=1&layers=ce3f25f987ef44b3939248e76b12d9bc',
#             #                       height="100%", width="100%")),
#     # dcc.Dropdown(
#     #     id='dropdown',
#     #     options=[
#     #         {'label': 'Video 1', 'value': 'video1'},
#     #         {'label': 'Video 2', 'value': 'video2'},
#     #         {'label': 'Video 3', 'value': 'video3'},
#     #     ],
#     #     value='video1'
#     # )
# ],style={'width': '89px','height':"100px", 'display': 'inline-block', 'padding': '0 20'})


# @app.callback(Output('target', 'children'), [Input('dropdown', 'value')])
# def embed_iframe(value):
#     videos = {
#         'video1': 'sea2K4AuPOk',
#         'video2': '5BAthiN0htc',
#         'video3': 'e4ti2fCpXMI',
#     }
#     return html.Iframe(src='https://ucsdonline.maps.arcgis.com/home/webmap/viewer.html?useExisting=1&layers=ce3f25f987ef44b3939248e76b12d9bc',width='49%',height='90%')
    # return html.Iframe(src='https://ucsdonline.maps.arcgis.com/home/webmap/viewer.html?useExisting=1&layers=ce3f25f987ef44b3939248e76b12d9bc')
    # return html.Iframe(src=f'https://www.youtube.com/embed/{videos[value]}')

# app.layout = html.Div([
#     html.Div(id='test_embed', children=map1)
# ])

# @app.callback(Output('test_embed', 'children'))
# def embed_iframe():
#     return html.Iframe(src=WebMap(map1))

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True) 
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(debug=True)