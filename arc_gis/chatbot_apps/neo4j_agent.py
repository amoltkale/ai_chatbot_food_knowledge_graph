from neo4j_interface import Neo4jDatabaseToolkit
from neo4j_interface import create_sql_agent

from neo4j_database import Neo4jDatabase
from llm_utils import get_default_openai_llm 


if __name__ == "__main__":
    llm = get_default_openai_llm()
    db = Neo4jDatabase()
    toolkit = Neo4jDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
        )