from typing import List, Optional, Tuple, Dict

from neo4j import GraphDatabase
import sys
sys.path.append('../../')
from utils import get_config

class Neo4jDatabase:
    def __init__(self, host: str = "neo4j://localhost:7687",
                 user: str = "neo4j",
                 password: str = "neo4j"):
        """Initialize the ontology database"""

        self.driver = GraphDatabase.driver(host, auth=(user, password))

    def query(
        self,
        cypher_query: str,
        params: Optional[Dict] = {}
    ) -> List[Dict[str, str]]:
        print(cypher_query)
        with self.driver.session() as session:
            result = session.run(cypher_query, params)
            # Limit to at most 50 results
            return [r.values()[0] for r in result][:50]


if __name__ == "__main__":

    username = get_config("neo4j_ontology","username")
    password = get_config("neo4j_ontology","passkey")
    host = get_config("neo4j_ontology","host")

    database = Neo4jDatabase(host=host,
                             user=username, password=password)

    a = database.query("""
    MATCH (n) RETURN {count: count(*)} AS count
    """)

    print(a)