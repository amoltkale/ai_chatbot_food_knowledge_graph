import sys
import argparse
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks import get_openai_callback

from load_registrant import get_welcome_prompt, set_enviro_email, user_menu
from neo4j_database import Neo4jDatabase

# import to read configs
sys.path.append('../')
from utils import bcolors, print_in_color, get_postgres_db_obj

from llm_utils import get_default_openai_llm

def parse_args():
    parser = argparse.ArgumentParser(description = 'Grab some variables about how to run the app')
    parser.add_argument('--email', type=str, default="m.hernandez@gmail.com",
                        help="user email to use")
    parser.add_argument('--question', type=str, default=None,
                        help="Directly ask agent chain a question")
    return parser.parse_args()

def setup_agent_chain():
    # from tools_agent import agent
    from location_recommendation_tool import LocationRecommendation
    from sba_doc_index_tool import SBADocIndexTool
    from funding_doc_index_tool import FundingDocIndexTool
    from neo4j_interface import  RelatedFoodIRIListTool
    from nearest_sba_tool_enhanced import NearestSBAToolEnhanced

    llm = get_default_openai_llm()

    tools = [
            LocationRecommendation,
            FundingDocIndexTool,
            SBADocIndexTool,
            NearestSBAToolEnhanced,
            RelatedFoodIRIListTool(),
            ]

    memory = ConversationBufferMemory(memory_key="chat_history")
    # memory.save_context({"welcome_prompt":get_welcome_prompt()},{"output":""})
    

    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    return agent_chain

if __name__ == '__main__':
    # Set email for chat
    args = parse_args()
    set_enviro_email(args.email)

    # Creating Postgres SQL DB
    sql_db = get_postgres_db_obj()

    agent_chain = setup_agent_chain()
    chat_history = get_welcome_prompt()
    with get_openai_callback() as cb:
        agent_chain.run(chat_history)
        print(cb)


    if args.question is not None:
        print_in_color('Question: ' + args.question, bcolors.YELLOW)

        # run the agent
        with get_openai_callback() as cb:
            answer = agent_chain.run(args.question)
            print_in_color(answer, bcolors.CYAN)
            print_in_color(cb, bcolors.PURPLE)
    else:
        # Querying the index
        while True:
            question = input("Question: ")
            if question == 'bye':
                break
            print_in_color(f"Question: {question}", bcolors.YELLOW)
            with get_openai_callback() as cb:
                answer = agent_chain.run(question)
                print_in_color(cb, bcolors.PURPLE)
            print_in_color(answer, bcolors.CYAN)
            #print_in_color(f"MEMEORY STORED: {agent_chain.memory.buffer}", bcolors.PURPLE)
            
    print_in_color(f"Chat history from memory:\n {agent_chain.memory.buffer}", bcolors.AMBER)
