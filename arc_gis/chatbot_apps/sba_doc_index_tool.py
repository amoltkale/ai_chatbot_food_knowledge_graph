
from pathlib import Path

from langchain.agents import Tool

from index_creation import read_llm_index

resource_path = Path("../resources")
index_storage_folder = resource_path / "sba_doc_indexes"

index = read_llm_index(index_storage_folder=index_storage_folder)

name = 'sba_doc_index'

description = f'''
Useful for when you want to answer questions about the information or explaination on loans from documents.
'''
# create an instance of the custom langchain tool
SBADocIndexTool = Tool(
    name=name,
    func=lambda q: str(index.as_query_engine().query(f"Find information on loan. {q}")),
    description=description,
    return_direct=True
)