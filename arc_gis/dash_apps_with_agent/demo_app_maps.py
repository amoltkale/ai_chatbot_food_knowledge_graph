from flask import Flask
import flask
import webbrowser

from load_registrant import *
from app_utils import get_bot_response, get_bot_prediction # Rename to bot_utils

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html

from langchain import OpenAI, ConversationChain

from tools_agent import agent

import json

import os

# https://community.plotly.com/t/how-can-i-use-my-html-file-in-dash/7740/2
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# get welcome prompt
prompt = get_welcome_prompt() # for now defaults to email: m.hernandez@gmail.com

# Prepare openai
ai_key = get_config("open_ai","key")
llm = OpenAI(temperature=0, verbose=True, openai_api_key=ai_key) # temp=0 for most reproducible results

conversation = ConversationChain(llm=llm, verbose=True)

# init app and add stylesheet
# Flask app 
server = Flask(__name__)
app = dash.Dash(name = __name__, server = server)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# init a list of the sessions conversation history
conv_hist = []


# credit to initial UI: https://github.com/AdamSpannbauer/app_rasa_chat_bot/blob/master/dash_demo_app.py

# app ui
app.layout = html.Div([
    html.H3('Fresh Start Bot Demo', style={'text-align': 'center'}),
    html.H4('Please answer all questions as accurately as possible. If you are unsure, please ask the bot to try again.',
            style={'text-align': 'center'}),
    html.Div([
        html.Div(id='conversation'),
        html.Br(),
        html.Div([
            html.Table([
                html.Tr([
                    # text input for user message
                    html.Td([dcc.Input(id='msg_input', value=prompt, type='text')],
                            style={'valign': 'middle'}),
                    # message to send user message to bot backend
                    html.Td([html.Button('Send', id='send_button', type='submit')],
                            style={'valign': 'middle'})
                ])
            ])],
            style={'width': '325px', 'margin': '0 auto'}),
        ],
        id='screen',
        style={'width': '400px', 'margin': '0 auto'})
])

# trigger bot response to user inputted message on submit button click
@app.callback(
    Output("msg_input", "value"),
    Output("conversation", "children"),
    Input("send_button", "n_clicks"),
    State('msg_input', 'value'),
)
# function to add new user*bot interaction to conversation history
def update_conversation(click, text):
    global conv_hist

    if click is None:
        # Initial load: Get prompt and welcome user
        response = "Hello World! Please be sure you are ready to use tokens. Then uncomment the code below!"
        # response = get_bot_response(llm, text)
        #response = get_bot_prediction(conversation, text)

        # user message aligned left
        rcvd = [html.H5(text, style={'text-align': 'left'})]
        # bot response aligned right and italics
        rspd = [html.H5(html.I(response), style={'text-align': 'right'})]

        # append interaction to conversation history and return
        # conv_hist = conv_hist + rspd + [html.Hr()]
        conv_hist = rspd + [html.Hr()]
        return "", conv_hist
    if click > 0:
        # call bot with user inputted text

        #response = "Bye Bye"

        output_json = json.loads(agent.run(text))

        # user message aligned left
        rcvd = [html.H5(text, style={'text-align': 'left'})]
        
        rspd =  [html.Iframe(src=output_json['file_path'], height="300px", width="500px")]
        # response = get_bot_response(llm, text)


        # bot response aligned right and italics
        # All return functions from langchain should be in a list so that it can be appended
        # rspd = [html.H5(html.I(response), style={'text-align': 'right'})]
        additional_text = [html.H5(html.I(output_json['verbal_desc']), style={'text-align': 'right'})]

        # append interaction to conversation history
        conv_hist = conv_hist + rcvd + rspd + additional_text + [html.Hr()]
        # conv_hist = conv_hist + rcvd + [html.Embed(src='./static/test_html.html')] + [html.Hr()]

        return "", conv_hist
    else:
        return "", ""

# Embed html
@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)


# run app
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True) 
    app.run_server(debug=True, use_reloader=False)
    # app.run_server()