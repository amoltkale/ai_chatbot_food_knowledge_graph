import sys
import os

sys.path.append('../')
from utils import get_config

from langchain.agents import initialize_agent
# from langchain.llms import OpenAI
from langchain import OpenAI, ConversationChain
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI


def get_bot_response(llm, in_str):
    #TODO actually add more interfacing here to process in_str
    # could add param to check if initial load (aka: if click == 0: get_bot_response(llm, in_str, int_load=True)
    return llm(in_str)

def get_bot_prediction(conversation, text):
    #TODO verifiy conversation is needed
    return conversation.predict(input=text)

def get_default_openai_llm(temperature=0):
    ai_key = get_config("open_ai","key")
    return OpenAI(temperature=temperature, verbose=True, openai_api_key=ai_key)

def get_gpt_4_openai_llm(temperature=0):
    ai_key = get_config("open_ai","key")
    return ChatOpenAI(temperature=temperature, model_name="gpt-4", verbose=True, openai_api_key=ai_key)