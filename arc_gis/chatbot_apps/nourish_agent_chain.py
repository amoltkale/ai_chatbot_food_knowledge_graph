import sys

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, ConversationalChatAgent, AgentType, initialize_agent
from langchain.callbacks import get_openai_callback


# from tools_agent import agent
from location_recommendation_tool import LocationRecommendation
from load_registrant_tool import LoadRegistrant
from load_registrant import get_welcome_prompt
from llm_utils import bcolors
from funding_recommendation_tool import FundingRecommendation
from nearest_sba_tool import NearestSBATool
from sba_doc_index_tool import SBADocIndexTool
from funding_doc_index_tool import FundingDocIndexTool


# import to read configs
import sys
sys.path.append('../../../../')
from utils import get_config

from llm_utils import get_gpt_4_openai_llm, get_default_openai_llm

openaikey = get_config("open_ai","key")
llm = get_default_openai_llm()



# This part is to create a shared memory
template = """This is a conversation between a human and a bot:

{chat_history}

Help identify location from the {input}:
"""

prompt = PromptTemplate(
    input_variables=["input", "chat_history"], 
    template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")
readonlymemory = ReadOnlySharedMemory(memory=memory)
readonlymemory.clear()
# summry_chain = LLMChain(
#     llm=llm, 
#     prompt=prompt, 
#     verbose=True, 
#     memory=readonlymemory, # use the read-only memory to prevent the tool from modifying the memory
# )

tools = [
         #LoadRegistrant,
         LocationRecommendation,
         NearestSBATool,
         #FundingRecommendation,
         FundingDocIndexTool,
         SBADocIndexTool
         ]



prompt = ConversationalChatAgent.create_prompt(
    tools, 
    input_variables=["input", "chat_history", "agent_scratchpad"]
)


agent_chain = initialize_agent(llm=llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, tools=tools, verbose=True, memory=readonlymemory)

if __name__ == '__main__':
    chat_history = get_welcome_prompt()
    with get_openai_callback() as cb:
        agent_chain.run(chat_history)
        print(cb)


    if len(sys.argv) > 1:
        question = ' '.join(sys.argv[1:])
        print('question: ' + question)

        # run the agent

        with get_openai_callback() as cb:
            answer = agent_chain.run(question)
            print(answer)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
    else:
        # Querying the index
        while True:
            prompt = input(f"{bcolors.WARNING}Question: {bcolors.ENDC}")
            print(f"{bcolors.WARNING}{prompt}{bcolors.ENDC}")
            with get_openai_callback() as cb:
                answer = agent_chain.run(prompt)
                print(cb)
            print(f"{bcolors.OKCYAN}{answer}{bcolors.ENDC}")
    readonlymemory.clear()