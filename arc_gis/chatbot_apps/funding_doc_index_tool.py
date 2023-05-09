
from pathlib import Path

from langchain.agents import Tool

from index_creation import read_llm_index
from load_registrant import server_connect, run_qry, get_user_funding_needs, get_user_business_profile

conn = server_connect()
email="m.hernandez@gmail.com"
funding_profile = get_user_funding_needs(conn, email=email)
biz_profile = get_user_business_profile(conn, email=email)

resource_path = Path("../resources")
index_storage_folder = resource_path / "sba_doc_indexes"

index = read_llm_index(index_storage_folder=index_storage_folder)

name = 'funding_doc_index'
description = f'''
                Converse as if you are talking to a person who is in high school.
                If the person is eligible for any loan, tell them the loan name. 
                Additionaly provide brief one sentece description on each of them.
                If they do not qualify for any loans, state the reason.
                Phrase the response as if you are addressing the person.
'''
# create an instance of the custom langchain tool
FundingDocIndexTool = Tool(
    name=name,
    func=lambda q: str(index.as_query_engine().query(f"Given the user has funding needs: {funding_profile} and users business profile is {biz_profile}. {q}")),
    description=description,
    return_direct=True
)