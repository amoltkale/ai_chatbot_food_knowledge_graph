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
# Memory
from langchain.memory import ConversationBufferMemory


# import custom tools
from location_recommendation_tool import LocationRecommendation



# import to read configs
import sys
sys.path.append('../../../../')
from utils import get_config

openaikey = get_config("open_ai","key")
llm = OpenAI(temperature=0, openai_api_key=openaikey)


template = '''\
You are a chatbot having coversation with a human.
{chat_history}
Human: {human_input}
Please respond to the questions accurately and succinctly. \
If you are unable to obtain the necessary data after seeking help, \
indicate that you do not know.
'''

prompt = PromptTemplate(input_variables=["chat_history","human_input"], template=template)

memory = ConversationBufferMemory(memory_key="chat_history")
# debug
# print(prompt.format())

# Load the tool configs that are needed.
llm_location_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
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