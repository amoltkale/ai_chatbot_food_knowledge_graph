import sys
import argparse

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, ConversationalChatAgent, AgentType, initialize_agent
from langchain.callbacks import get_openai_callback

from load_registrant import get_welcome_prompt, set_enviro_email, user_menu
from neo4j_database import Neo4jDatabase

# import to read configs
sys.path.append('../../../../')
from utils import get_config, bcolors, print_in_color

from llm_utils import get_gpt_4_openai_llm, get_default_openai_llm

def parse_args():
    parser = argparse.ArgumentParser(description = 'Grab some variables about how to run the app')
    parser.add_argument('--email', type=str, default="m.hernandez@gmail.com",
                        help="user email to use")
    parser.add_argument('--question', type=str, default=None,
                        help="Directly ask agent chain a question")
    return parser.parse_args()

def setup_agent_chain(db:Neo4jDatabase):
    # from tools_agent import agent
    from location_recommendation_tool import LocationRecommendation
    from load_registrant_tool import LoadRegistrant
    from funding_recommendation_tool import FundingRecommendation
    from nearest_sba_tool import NearestSBATool
    from sba_doc_index_tool import SBADocIndexTool
    from funding_doc_index_tool import FundingDocIndexTool
    from neo4j_interface import FoodIRITool, RelatedFoodListTool
    from nearest_sba_tool_enhanced import NearestSBAToolEnhanced

    llm = get_default_openai_llm()

    tools = [
            # LoadRegistrant,
            LocationRecommendation,
            FundingDocIndexTool,
            SBADocIndexTool,
            #NearestSBATool,
            NearestSBAToolEnhanced,
            FoodIRITool(db=db),
            RelatedFoodListTool(db=db),
            ]

    memory = ConversationBufferMemory(memory_key="chat_history")
    # memory.save_context({"welcome_prompt":get_welcome_prompt()},{"output":""})
    

    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    return agent_chain

if __name__ == '__main__':
    # Set email for chat
    args = parse_args()
    #set_enviro_email(args.email)
    
    set_enviro_email(user_menu())
    db:Neo4jDatabase = Neo4jDatabase()
    agent_chain = setup_agent_chain(db)

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
                db.close_session()
                break
            print_in_color(f"Question: {question}", bcolors.YELLOW)
            with get_openai_callback() as cb:
                answer = agent_chain.run(question)
                print_in_color(cb, bcolors.PURPLE)
            print_in_color(answer, bcolors.CYAN)
            #print_in_color(f"MEMEORY STORED: {agent_chain.memory.buffer}", bcolors.PURPLE)
            
    print_in_color(f"Chat history from memory:\n {agent_chain.memory.buffer}", bcolors.AMBER)
else:
    db:Neo4jDatabase = Neo4jDatabase()
    agent_chain = setup_agent_chain(db)