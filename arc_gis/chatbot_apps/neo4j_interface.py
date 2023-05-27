"""Cypher Agent"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, Field, root_validator

from langchain.agents.agent import AgentExecutor
#from langchain.agents.agent_toolkits.sql.prompt import SQL_PREFIX, SQL_SUFFIX
from langchain.agents.mrkl.base import ZeroShotAgent
#from langchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.chains import RetrievalQA

from neo4j_database import Neo4jDatabase

from pydantic import Field

class BaseNeo4jDatabaseTool(BaseModel):
    """Base tool for interacting with a Neo4j database."""

    db: Neo4jDatabase = Field(exclude=True)

    # Override BaseTool.Config to appease mypy
    # See https://github.com/pydantic/pydantic/issues/4173
    class Config(BaseTool.Config):
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
        extra = Extra.forbid

class FoodIRITool(BaseNeo4jDatabaseTool, BaseTool):
    """Tool to create the cypher query with fulltext index search to get Food IRI property"""
    name = 'food_iri'
    description = f'''
    Helps to return the node iri property value and node label from the neo4j database .
    Input should be a cypher query with food type as parameter as per example provided here.
    Output would be the Food iri from the query execution post this as a question to give related food products.

    Example:
    Here to get the node iri and the node label for food = apple slice, cypher query to be executed would be as below:
    CALL db.index.fulltext.queryNodes("label_index", "apple slice") YIELD node, score RETURN node.iri as food_iri limit 1
    '''
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the query, return the results or an error message."""
        return self.db.query_no_throw(query)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("QuerySqlDbTool does not support async")

class RelatedFoodListTool(BaseNeo4jDatabaseTool, BaseTool):
    """Tool to create the cypher query with fulltext index search to get Food IRI property"""
    name = 'food_list'
    description = f'''
    Helps to return the connected food products give a food iri value .
    Input should be a cypher query with iri as parameter as per example provided here.
    Output would be list of related food products using is_a relationship as per the query execution.

    Example Cypher Query:
    Here to get the related food products with iri = "http://purl.obolibrary.org/obo/FOODON_00001009", cypher query to be executed would be as below:
    MATCH p=(n:Concept)<-[r:is_a*..2]-(m) WHERE n.iri = "http://purl.obolibrary.org/obo/FOODON_00001009" return collect(n.label[0])[0] + collect(m.label[0]) as related_food_products_list
    '''
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the query, return the results or an error message."""
        return self.db.query_no_throw(query)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("QuerySqlDbTool does not support async")


class QueryNeo4jDataBaseTool(BaseNeo4jDatabaseTool,BaseTool):
    """Tool for querying a Neo4j database."""

    name = "query_neo4j_db"
    description = """
    Input to this tool is a detailed and correct Cypher query, output is a result from the database.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the query, return the results or an error message."""
        return self.db.query_no_throw(query)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("QuerySqlDbTool does not support async")

class InfoNeo4jDatabaseTool(BaseNeo4jDatabaseTool, BaseTool):
    """Tool for getting metadata about a Neo4j database."""

    name = "schema_neo4j_db"
    description = """
    Input to this tool is list of labels and relationship labels , output is the properties associated with.
    Be sure that the labels and relationships actually exist by calling list_tables_sql_db first!
    Output 
    Example Input: "neo4j"
    """

    def _run(
        self,
        table_names: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get the schema for tables in a comma-separated list."""
        return self.db.get_table_info_no_throw(table_names.split(", "))

    async def _arun(
        self,
        table_name: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("SchemaSqlDbTool does not support async")

class ListNeo4jDatabaseTool(BaseNeo4jDatabaseTool, BaseTool):
    """Tool for getting list of all node labels and relationship labels."""

    name = "get_node_and_egde_labels"
    description = """
    Input to this tool is the database name, output is json with node labels and edge labels.

    Example Input: "neo4j"
    """



class Neo4jDatabaseToolkit(BaseToolkit):
    """Toolkit for interacting with SQL databases."""

    db: Neo4jDatabase  = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)

    # @property
    # def dialect(self) -> str:
    #     """Return string representation of dialect to use."""
    #     return self.db.dialect

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            QueryNeo4jDataBaseTool(db=self.db),
            #InfoNeo4jDatabaseTool(db=self.db),
            #ListNeo4jDatabaseTool(db=self.db),
            #CypherQueryCheckerTool(db=self.db, llm=self.llm),
        ]

CYPHER_PREFIX = """You are an agent designed to interact with a Neo4j database.
Given an input question, create a syntactically correct query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.
"""

CYPHER_SUFFIX = """Begin!

Question: {input}
Thought: I should look at the tables in the database to see what I can query.
{agent_scratchpad}"""

FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""

def create_sql_agent(
    llm: BaseLanguageModel,
    toolkit: Neo4jDatabaseToolkit,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = CYPHER_PREFIX,
    suffix: str = CYPHER_SUFFIX,
    format_instructions: str = FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    top_k: int = 10,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct a sql agent from an LLM and tools."""
    tools = toolkit.get_tools()
    prefix = prefix.format(top_k=top_k)
    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        format_instructions=format_instructions,
        input_variables=input_variables,
    )
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        callback_manager=callback_manager,
    )
    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, **kwargs)
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        max_iterations=max_iterations,
        max_execution_time=max_execution_time,
        early_stopping_method=early_stopping_method,
        **(agent_executor_kwargs or {}),
    )


