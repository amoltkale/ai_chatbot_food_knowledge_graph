from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.prompts import PromptTemplate

# import custom tools
from weather_tool import Weather

# import to read configs
import sys
sys.path.append('../../../')
from utils import get_config

openaikey = get_config("open_ai","key")
llm = OpenAI(temperature=0, openai_api_key=openaikey)

prompt = PromptTemplate(
    input_variables=[],
    template="Answer the following questions as best you can."
)

# Load the tool configs that are needed.
llm_weather_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True
)

tools = [
    Weather
]

# Construct the react agent type.
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

agent.run("What about the weather today in Genova, Italy")