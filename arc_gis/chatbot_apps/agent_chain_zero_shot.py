import sys
import argparse

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, ConversationalChatAgent, AgentType, initialize_agent
from langchain.callbacks import get_openai_callback

from load_registrant import get_welcome_prompt, set_enviro_email
from llm_utils import bcolors

# import to read configs
import sys
sys.path.append('../../../../')
from utils import get_config

from llm_utils import get_gpt_4_openai_llm, get_default_openai_llm

def parse_args():
    parser = argparse.ArgumentParser(description = 'Grab some variables about how to run the app')
    parser.add_argument('--email', type=str, default="m.hernandez@gmail.com",
                        help="user email to use")
    parser.add_argument('--question', type=str, default=None,
                        help="Directly ask agent chain a question")
    return parser.parse_args()

def setup_zeroshot_chain():
    from location_recommendation_tool import LocationRecommendation
    from load_registrant_tool import LoadRegistrant
    from funding_recommendation_tool import FundingRecommendation
    from nearest_sba_tool import NearestSBATool
    from sba_doc_index_tool import SBADocIndexTool
    from funding_doc_index_tool import FundingDocIndexTool

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


    tools = [
            LoadRegistrant,
            LocationRecommendation,
            NearestSBATool,
            #FundingRecommendation,
            FundingDocIndexTool,
            SBADocIndexTool
            ]



    prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
    suffix = """Begin!"

    {chat_history}
    Question: {input}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools, 
        prefix=prefix, 
        suffix=suffix, 
        input_variables=["input", "chat_history", "agent_scratchpad"]
    )


    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)
    return agent_chain

if __name__ == '__main__':
    args = parse_args()
    set_enviro_email(args.email)

    agent_chain = setup_zeroshot_chain

    chat_history = get_welcome_prompt()
    with get_openai_callback() as cb:
        agent_chain.run(chat_history)
        print(cb)


    if args.question is not None:
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
else:
    agent_chain = setup_zeroshot_chain