from load_registrant import *
from app_utils import get_bot_response # Rename to bot_utils

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html

from langchain.llms import OpenAI

# get welcome prompt
prompt = get_welcome_prompt()

# Prepare openai
ai_key = get_config("open_ai","key")
llm = OpenAI(temperature=0, verbose=True, openai_api_key=ai_key)

# init app and add stylesheet
app = dash.Dash()
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
        html.Br(),
        html.Div(id='conversation')],
        id='screen',
        style={'width': '400px', 'margin': '0 auto'})
])

# trigger bot response to user inputted message on submit button click
@app.callback(
    Output("conversation", "children"),
    Input("send_button", "n_clicks"),
    Input('msg_input', 'value'),
)
# function to add new user*bot interaction to conversation history
def update_conversation(click, text):
    global conv_hist

    # call bot with user inputted text
    response = "Hello World"
    # response = get_bot_response(text)

    # user message aligned left
    rcvd = [html.H5(text, style={'text-align': 'left'})]
    # bot response aligned right and italics
    rspd = [html.H5(html.I(response), style={'text-align': 'right'})]
    # append interaction to conversation history
    conv_hist = rcvd + rspd + [html.Hr()] + conv_hist

    return conv_hist

@app.callback(
    Output(component_id='msg_input', component_property='value'),
    [Input(component_id='conversation', component_property='children')]
)
def clear_input(_):
    return ''


# run app
if __name__ == '__main__':
    app.run_server()