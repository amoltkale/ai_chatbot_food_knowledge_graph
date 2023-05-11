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


tools = [
         LoadRegistrant,
         LocationRecommendation,
         NearestSBATool,
         #FundingRecommendation,
         FundingDocIndexTool,
         SBADocIndexTool
         ]



# prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
# suffix = """Begin!"

# {chat_history}
# Question: {input}
# {agent_scratchpad}"""

# prompt = ConversationalChatAgent.create_prompt(
#     tools, 
#     input_variables=["input", "chat_history", "agent_scratchpad"]
# )


memory = ConversationBufferMemory(memory_key="chat_history")

#llm_chain = LLMChain(llm=llm, prompt=prompt)
# agent = ConversationalChatAgent(llm_chain=llm_chain, tools=tools, verbose=True)
#agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)


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
  