import time
from urllib.parse import quote
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, Extra
from langchain.tools import BaseTool
from langchain import OpenAI, SQLDatabase
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import sys

sys.path.append('../../')
from utils import get_config
from llm_utils import get_default_openai_llm

username = get_config("nourish_db","username")
password = get_config("nourish_db","passkey")
host = get_config("nourish_db","host")
db = get_config("nourish_db","db")

#since password can have @ character, encoding the URL
db = SQLDatabase.from_uri(f"postgresql://{username}:%s@{host}/{db}" % quote(password))
#db = SQLDatabase.from_uri(f"postgresql://{username}:{password}s@{host}/{db}")


#llm = get_default_openai_llm()
#db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

class BasePostGresDatabaseTool(BaseModel):
    """Base tool for interacting with a Postgres sql database."""

    db: SQLDatabase = Field(exclude=True)

    # Override BaseTool.Config to appease mypy
    # See https://github.com/pydantic/pydantic/issues/4173
    class Config(BaseTool.Config):
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
        extra = Extra.forbid

class HealthyAndUnheathyFoodTool(BasePostGresDatabaseTool, BaseTool):
    """Tool to create the postgres sql query to return the healthy and unhealthy food"""
    name = 'ranked_food_list'
    description = f'''
    Helps give markdown table for top 3 food items ranked foods according to ranks and another markdown table for bottom 3 ranked foods according to ranks by using output from related_food_iri_name_list tool.
    Input should be a postgres array of food iri names.
    
    Output would be top 3 food items ranked foods according to ranks and another markdown table for bottom 3 ranked foods according to ranks. Additionally mention the count of related ranked food items from the initial output.
    Output format can be as below "
    
    Top 3 food alternatives:
    * food item1
    * food item2
    * food item3

    Bottom 3 food alternatives:
    * food item1
    * food item2
    * food item3

    '''
    def _run(
        self,
        iri_names_list: List[str],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the query created by using the list or arrat of iri"""
        query = f"""WITH fdc_list as
                                (SELECT DISTINCT fdc_id, matched_components, product_desc
                                FROM lexmapr_iri
                                WHERE match_id = 1 AND
                                    component_iri = any(array{iri_names_list}))
                            , hpf_fdc_list AS (SELECT DISTINCT ON (fdc_list.matched_components)
                                fdc_list.matched_components,
                                fdc_list.product_desc,
                                hpf.n,
                                hpf.hpf_score
                            FROM fdc_list INNER JOIN avg_hpf_scores as hpf
                                ON fdc_list.matched_components = hpf.matched_components)
                            SELECT ROW_NUMBER() OVER (ORDER BY hpf_score ASC) AS rank, *
                            From hpf_fdc_list
                            ORDER BY rank;"""
        print(f"\nSQL Quey: {query}")
        result = self.db.run_no_throw(query)
        return result

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("RelatedFoodListTool does not support async")


if __name__ == '__main__':
    start_time = time.time()
    output = db.run_no_throw("""
                WITH fdc_list as
                    (SELECT DISTINCT fdc_id, matched_components, product_desc
                    FROM lexmapr_iri
                    WHERE match_id = 1 AND
                        component_iri = any(array['FOODON_00001009','FOODON_03302012','FOODON_03311509','FOODON_03310934','FOODON_03310577','FOODON_03310576','FOODON_03310165','FOODON_03310164','FOODON_03310163','FOODON_03310162','FOODON_03307230','FOODON_00001605','FOODON_00004095','FOODON_00003924','FOODON_00003288','FOODON_00003890','FOODON_00001224']))
                , hpf_fdc_list AS (SELECT DISTINCT ON (fdc_list.matched_components)
                    fdc_list.matched_components,
                    fdc_list.product_desc,
                    hpf.n,
                    hpf.hpf_score
                FROM fdc_list INNER JOIN avg_hpf_scores as hpf
                    ON fdc_list.matched_components = hpf.matched_components)
                SELECT ROW_NUMBER() OVER (ORDER BY hpf_score ASC) AS rank, *
                From hpf_fdc_list
                ORDER BY rank;
                """, fetch="all")
    print(output)
    print("--- %s seconds ---" % (time.time() - start_time))





