from typing import List, Optional, Tuple, Dict

from neo4j import GraphDatabase, Result
import sys
sys.path.append('../')
from utils import get_config

class Neo4jDatabase:
    def __init__(self, host: str = "neo4j://localhost:7687",
                 user: str = "neo4j",
                 password: str = "neo4j123"):
        """Initialize the ontology database"""

        self.driver = GraphDatabase.driver(host, auth=(user, password))

    def close_session(self):
        self.driver.close()

    def query(
        self,
        cypher_query: str,
        params: Optional[Dict] = {}
    ) -> List[Dict[str, str]]:
        with self.driver.session() as session:
            result = session.run(cypher_query, params)
            # Limit to at most 50 results
            return [r.values()[0] for r in result]
        
    def query_no_throw(self, cypher_query: str) -> str:
        """Execute a Cypher command and return a string representing the results.

        If the statement returns rows, a string of the results is returned.
        If the statement returns no rows, an empty string is returned.

        If the statement throws an error, the error message is returned.
        """
        try:
            return self.query(cypher_query)
        except Exception as e:
            """Format the error message"""
            print(f"Error: {e}")
            return "Sorry, something went wrong, I cannot get the informationa asked"

if __name__ == "__main__":
    SDSC_DB = 'San Diego Super Computer Neo4j DB'
    LOCAL_DB = 'Localhost Neo4j DB'
    choice = int(input(f'Please choose the Neo4j database. Choose:\n1 for {SDSC_DB}, \n2 for {LOCAL_DB}:\n '))
    database = Neo4jDatabase()
    if (choice == 1):
        username = get_config("neo4j_ontology","username")
        password = get_config("neo4j_ontology","passkey")
        host = get_config("neo4j_ontology","host")
        database = Neo4jDatabase(host=host, user=username, password=password)

    query = """
    CALL db.index.fulltext.queryNodes("label_index", "apple slice") YIELD node, score RETURN node.iri, node.label, score limit 1
    """
    print(f"Cypher Query Generanated:\n{query}")
    print("RESULT:")
    a = database.query_no_throw(query)
    print(a)
    database.close_session()