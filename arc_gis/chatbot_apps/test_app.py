## COMMENTED OUT
from flask import Flask
import flask
import webbrowser

# import plotly.io as pio # used to read in cached file

import dash
from dash import html

import os

# https://community.plotly.com/t/how-can-i-use-my-html-file-in-dash/7740/2


STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

## READ IN HTML AS STRING INSTEAD OF STARTING FLASK APP AND ROUTING HTML FILE
# fname = "./static/test_html.html"
# HtmlFile = open(fname, 'r', encoding='utf-8')
# source_code = HtmlFile.read()

## COMMENT OUT FLASK APP
server = Flask(__name__)
app = dash.Dash(name = __name__, server = server)

app.layout = html.Div([
    html.Div(id='target',
        children=html.Embed(src='./static/test_html.html', height="500px", width="1000px"))
])

## COMMENTED OUT FLASK SERVER
@app.server.route('/static/<resource>')
def serve_static(resource):
    # print(resource)
    return flask.send_from_directory(STATIC_PATH, resource)

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
# ],style={'width': '89px','height':"100px", 'display': 'inline-block', 'padding': '0 20'})

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True) 
    app.run_server(debug=True, use_reloader=False)
    # app.run_server(debug=True)