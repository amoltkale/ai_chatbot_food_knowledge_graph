import os
from pathlib import Path

from langchain.agents import Tool

from index_creation import read_llm_index
from load_registrant import server_connect, get_email, get_user_funding_needs, get_user_business_profile

conn = server_connect()
email=get_email()
funding_profile = get_user_funding_needs(conn, email=email)
biz_profile = get_user_business_profile(conn, email=email)

resource_path = Path("../resources")
index_storage_folder = resource_path / "sba_doc_indexes"

index = read_llm_index(index_storage_folder=index_storage_folder)

name = 'funding_doc_index'
description = f'''
                You are assisting a person with a high school education.
                REMEMBER YOU ARE TALKING DIRECTLY TO THE PERSON.
                Find any loans the person might qualify for based on their funding needs and business profile. 
                Additionally provide brief one sentence description for any loans found.
                If they do not qualify for any loans, state the reason.
                REMEMBER YOU ARE TALKING DIRECTLY TO THE PERSON.
                RESPOND IN FIRST PERSON ONLY.
'''
# create an instance of the custom langchain tool
FundingDocIndexTool = Tool(
    name=name,
    func=lambda q: str(index.as_query_engine().query(f"Find loans based on the funding needs: {funding_profile} and business profile: {biz_profile}. {q}")),
    description=description,
    return_direct=False
)