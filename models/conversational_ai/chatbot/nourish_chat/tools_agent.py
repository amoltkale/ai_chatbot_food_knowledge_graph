#
# tools_agent.py
#
# zero-shot react agent that reply questions using available tools
# - Location
# - FoodBusinessType
#
# The agent gets the question as a command line argument (a quoted sentence).
# $ py tools_agent.py Location and business type question.
#
import sys

from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.prompts import PromptTemplate

# import custom tools
from location_recommendation_tool import LocationRecommendation

# import to read configs
import sys
sys.path.append('../../../../')
from utils import get_config

openaikey = get_config("open_ai","key")
llm = OpenAI(temperature=0, openai_api_key=openaikey)


template = '''\
Utter the question in the form \'Thank you for filling up the form, we understand that \
you want to open a Mexican Grocery Store in Chula Vista within 10 mile radius.\' \
If you are unable to obtain the necessary data after seeking help, \
indicate that you do not know.
'''

prompt = PromptTemplate(input_variables=[], template=template)

# debug
# print(prompt.format())

# Load the tool configs that are needed.
llm_weather_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True
)

tools = [
     LocationRecommendation
]

# Construct the react agent type.
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# DEBUG
# https://github.com/hwchase17/langchain/issues/912#issuecomment-1426646112
# agent.agent.llm_chain.verbose=True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        question = ' '.join(sys.argv[1:])
        print('question: ' + question)

        # run the agent
        answer = agent.run(question)
        print(answer)
    else:
        print('Agent answers questions using Weater and Datetime custom tools')
        print('usage: py tools_agent.py <question sentence>')
        print('example: py tools_agent.py what time is it?')