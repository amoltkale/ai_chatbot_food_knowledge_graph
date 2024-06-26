
from pathlib import Path

from langchain.agents import Tool

from index_creation import read_llm_index

resource_path = Path("../arc_gis/resources")
index_storage_folder = resource_path / "sba_doc_indexes"

index = read_llm_index(index_storage_folder=index_storage_folder)

name = 'sba_doc_index'

description = f'''
You are assisting a person with a high school education.
REMEMBER YOU ARE TALKING DIRECTLY TO THE PERSON.
Useful for when you want to answer questions about the information or explaination on loans from documents.
Format the answer in a concise summary of what you find.
REMEMBER YOU ARE TALKING DIRECTLY TO THE PERSON.
RESPOND IN FIRST PERSON ONLY.
DO NOT LOSE ANY INFORMATION WHEN YOU REFORMAT THE THOUGHT.
'''
# create an instance of the custom langchain tool
SBADocIndexTool = Tool(
    name=name,
    func=lambda q: str(index.as_query_engine().query(f"Find information on loan. {q}")),
    description=description,
    return_direct=False
)