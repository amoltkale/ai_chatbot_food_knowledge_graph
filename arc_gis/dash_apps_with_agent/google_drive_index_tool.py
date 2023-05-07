from pathlib import Path

from langchain import OpenAI
from langchain.agents import Tool
from llama_index import Document, GPTVectorStoreIndex, LLMPredictor, ServiceContext, PromptHelper, SimpleDirectoryReader, GPTSimpleVectorIndex
from langchain.document_loaders import GoogleDriveLoader
from langchain.callbacks import get_openai_callback


import sys
sys.path.append('../../')
from utils import get_config

def create_indexes(service_context, file_name):


    loader = GoogleDriveLoader(
        #folder_id="1PwdIP7WCHrr3LNDHUAs0aU5B0hPmyQJg",  # SBA
        # folder_id="1yyyyc2upDaxy9R7Ul2i8e0l23Vz9rOY3",  # USDA
        folder_id="1-m2xCFkAtSgP_EbyS6D9p35R0dPoqfPb", #welcome prompt
        # Optional: configure whether to recursively fetch files from subfolders. Defaults to False.
        recursive=False
    )

    docs = loader.load()

    documents = []

    for doc in docs:
        documents.append(Document.from_langchain_format(doc))


    index = GPTSimpleVectorIndex.from_documents(documents=documents, service_context=service_context)


    # Save your index to a index.json file
    index.save_to_disk(file_name)

    return index

def read_indexes( service_context, file_name):
    # Load the index from your saved index.json file
    index = GPTSimpleVectorIndex.load_from_disk(file_name, service_context=service_context)
    return index

if __name__ == '__main__':
    #print(Path.home())

        # Prepare openai
    ai_key = get_config("open_ai","key")
    llm = OpenAI(temperature=0, verbose=True, model_name="gpt-4", openai_api_key=ai_key) # temp=0 for most reproducible results
    llm_predictor = LLMPredictor(llm=llm)

    # Configure prompt parameters and initialise helper
    max_input_size = 4096
    num_output = 256
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)


    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    file_name = 'welcome_prompt_doc_index.json'

    index_m = create_indexes(service_context,file_name)
    index = read_indexes(service_context, file_name)
    # Querying the index
    while True:
        prompt = input("Type prompt...")
        response = index.query(prompt)
        print(response)
    #print(docs[0])