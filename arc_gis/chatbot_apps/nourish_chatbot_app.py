import json
import os
import sys
import argparse

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html

from flask import Flask
import flask

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.callbacks import get_openai_callback

# import to read configs
sys.path.append('../../')
from utils import get_config, get_postgres_db_obj

from load_registrant import get_welcome_prompt, set_enviro_email

# set up response style
recieved_style={
    'text-align':'right',
    'color':'white',}

response_style={
    'text-align':'left',
    # 'color':'rgb(80,36,97)',
    # 'backgroundColor':'rgb(100, 100, 100)'
    }

def parse_args():
    parser = argparse.ArgumentParser(description = 'Grab some variables about how to run the app')
    parser.add_argument('--email', type=str, default="m.hernandez@gmail.com",
                        help="user email to use")
    parser.add_argument('--ui_dev', type=bool, default=False,
                        help="Directly ask agent chain a question")
    return parser.parse_args()

# Pull params and set environment variable
args = parse_args()

# https://community.plotly.com/t/how-can-i-use-my-html-file-in-dash/7740/2
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

if not args.ui_dev:
    # Set up agent chains
    from agent_chain_conversational import setup_agent_chain
    from neo4j_database import Neo4jDatabase

    # Prepare openai
    ai_key = get_config("open_ai","key")

    # Get AI key
    os.environ['OPENAI_API_KEY'] = ai_key

    # Establish user email
    set_enviro_email(args.email)

    db:Neo4jDatabase = Neo4jDatabase()

    # Creating Postgres SQL DB
    sql_db = get_postgres_db_obj()

    agent_chain = setup_agent_chain(neo4j_db=db,sql_db=sql_db)

    # intial_response = "Hello"
    with get_openai_callback() as cb:
        intial_response = agent_chain.run(get_welcome_prompt())
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")
else:
    intial_response = "Hello, welcome to ui development. " \
                        "If you don't want to be here, restart the app with ui_dev set to False"

# init app and add stylesheet
# Flask app 
server = Flask(__name__)
app = dash.Dash(name = __name__, server = server)
# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# init a list of the sessions conversation history
#conv_hist = [html.H5(html.I(intial_response), style={'text-align': 'left'})] + [html.Hr()]
conv_hist = [html.Hr()] + [html.H5(html.I(intial_response), style=response_style)] + [html.Hr()]

# credit to initial UI: https://github.com/AdamSpannbauer/app_rasa_chat_bot/blob/master/dash_demo_app.py

# app ui
app.layout = html.Div([
    html.Img(src='static/nourish_logo.png', height="100px", width="100px"),
        html.H3('Nourish Chatbot',style={'text-align': 'center'}),
        html.H4('Please answer all questions as accurately as possible. If you are unsure, please ask the bot to try again.',
                style={'text-align':'center'}),
        html.Div([
            html.Div(id='conversation'),
            # html.Br(),
            # dcc.Loading(
            #             id="loading-1",
            #             type="default",
            #             children=html.Div([
            #             dcc.Input(id='msg_input', value='', type='text',style={'width':'925px'}),
            #             html.Button('>', id='send_button', type='submit',style={'width':'40px'})
            #             ],)
            #             ),
            ],
            id='screen',
            style={'width': '1000px', 'margin': '0 auto'}),
        html.Div([
            html.Br(),
            dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=html.Div([
                        dcc.Input(id='msg_input', value='', type='text',style={'width':'925px'}),
                        html.Button('>', id='send_button', type='submit',style={'width':'40px'})
                        ],)
                        ),
        ], style={'width': '1000px', 'margin': '0 auto'}),
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
        return "", conv_hist
    if click > 0:
        # call bot with user inputted text

        if not args.ui_dev:
            with get_openai_callback() as cb:
                agent_response = agent_chain.run(text)
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost (USD): ${cb.total_cost}")
            try:
                output_json = json.loads(agent_response)
                if 'file_path' in output_json:
                    additional_text = [html.H5(html.I(output_json['verbal_desc']), style=response_style)]
                    rspd =  [html.Iframe(src=output_json['file_path'], height="400px", width="1000px")] + additional_text
                else:
                    rspd = [html.H5(html.I(output_json['response']), style=response_style)]
            except:
                rspd = [dcc.Markdown(agent_response, style=response_style)]
        else:
            rspd = [dcc.Markdown("""
You are still in ui dev. Restart app with ui_dev flag set to false to run agent.  
Currently Available parameters are the following:  
------
* --email: email of desired user. default = m.hernandez@gmail.com
* --ui_dev: Boolean flag to control ui dev  
------
Example run:  
```py
python nourish_chatbot_app.py --ui_dev True
```  
""", style=response_style)]


        # user message aligned left
        rcvd = [html.H5(html.B(text), style=recieved_style)]
        

        # append interaction to conversation history
        conv_hist = conv_hist + rcvd + rspd + [html.Hr()]

        return "", conv_hist
    else:
        return "", ""

# Embed html
@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)


# run app
if __name__ == '__main__':
    #webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True) 
    app.run_server(debug=True, use_reloader=False)
    # app.run_server()