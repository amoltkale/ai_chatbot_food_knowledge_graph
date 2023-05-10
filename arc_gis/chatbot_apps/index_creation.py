import logging
import sys
import os
from pathlib import Path


from llama_index import GPTVectorStoreIndex, download_loader, Document, StorageContext, load_index_from_storage
from llama_index.output_parsers import LangchainOutputParser
from llama_index.llm_predictor import StructuredLLMPredictor
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from llama_index.prompts.prompts import QuestionAnswerPrompt, RefinePrompt
from llama_index.prompts.default_prompts import DEFAULT_TEXT_QA_PROMPT_TMPL, DEFAULT_REFINE_PROMPT_TMPL
from langchain.document_loaders import GoogleDriveLoader

sys.path.append('../../')
from utils import get_config
from llm_utils import get_gpt_4_openai_llm

def create_gdrive_index(*, folder_id:str, index_storage_folder:Path):
    # ## Reading Google Drive Folder
    # GoogleDriveReader = download_loader("GoogleDriveReader")
    # loader = GoogleDriveReader(credentials_path=Path.home() / ".credentials/credentials.json")

    # #### Using folder id
    # documents = loader.load_data(folder_id="1PwdIP7WCHrr3LNDHUAs0aU5B0hPmyQJg") #SBA
    # #### Using file ids
    # # documents = loader.load_data(file_ids=["fileid1", "fileid2"])

    if os.path.exists(index_storage_folder):
        print(f"Index folder already exists at {index_storage_folder}. Returning index from the disk!!")
        return read_llm_index(index_storage_folder=index_storage_folder)
    else:
        #print("Index folder does not exist")

        loader = GoogleDriveLoader(
                folder_id=folder_id,
                # folder_id="1PwdIP7WCHrr3LNDHUAs0aU5B0hPmyQJg",  # SBA
                # folder_id="1yyyyc2upDaxy9R7Ul2i8e0l23Vz9rOY3",  # USDA
                # folder_id="1-m2xCFkAtSgP_EbyS6D9p35R0dPoqfPb", #welcome prompt
                # Optional: configure whether to recursively fetch files from subfolders. Defaults to False.
                recursive=False
            )

        docs = loader.load()

        print(f"length of docs: {len(docs)}")

        documents = []

        for doc in docs:
            documents.append(Document.from_langchain_format(doc))



        index = GPTVectorStoreIndex.from_documents(documents, chunk_size_limit=512)

        index.storage_context.persist(persist_dir=str(index_storage_folder))
        return index

def create_rdf_index(*, file_p:Path, index_storage_folder:Path):
    RDFReader = download_loader("RDFReader")
    loader = RDFReader()
    documents = loader.load_data(file=file_p)

    index = GPTVectorStoreIndex.from_documents(documents, chunk_size_limit=512)

    index.storage_context.persist(persist_dir=str(index_storage_folder))
    return index

def read_llm_index(*, index_storage_folder:Path):
    os.environ['OPENAI_API_KEY'] = get_config("open_ai","key")
    if index_storage_folder is None:
        raise ValueError("Give valid path")
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=str(index_storage_folder))
    # load index
    index = load_index_from_storage(storage_context)
    return index

def create_all_doc_indexes():
    # SBA
    resource_path = Path("../resources")
    create_gdrive_index(folder_id="1PwdIP7WCHrr3LNDHUAs0aU5B0hPmyQJg", index_storage_folder=resource_path / "sba_doc_indexes")
    #USDA
    create_gdrive_index(folder_id="1yyyyc2upDaxy9R7Ul2i8e0l23Vz9rOY3", index_storage_folder=resource_path / "usda_doc_indexes")



if __name__ == '__main__':
    create_all_doc_indexes()
    # is_sba = False
    # # Get AI key
    # os.environ['OPENAI_API_KEY'] = get_config("open_ai","key")

    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    # resource_path = Path("../resources")
    # index_storage_folder = resource_path / "indexes"
    # index_storage_folder.mkdir(exist_ok=True)

    # llm = get_gpt_4_openai_llm()
    # llm_predictor = StructuredLLMPredictor(llm=llm)

    # if is_sba:
    #     create_gdrive_index(folder_id="1PwdIP7WCHrr3LNDHUAs0aU5B0hPmyQJg", index_storage_folder=index_storage_folder)
    #     index = read_llm_index(index_storage_folder=index_storage_folder)
    #     response_schemas = [
    #         ResponseSchema(name="QualifyingLoan", description="Describes the type of loans use may qualify for."),
    #         ResponseSchema(name="LoanEligibilityCriteria", description="Describes the eligibilty Criteria for identified loan types.")
    #     ]
    #     request = """
    #         I am trying to open up a food truck in San Diego City, I need to borrow $150,000. 
    #         And I need the loan immediately.  My yearly revenue will be less that $1 million. 
    #         I have less than 40 employees. What loans do I qualify for?
    #      """
    # else:
    #     # create_rdf_index(file_p=Path("../resources/financial-ontology.rdf"), index_storage_folder=index_storage_folder)
    #     # raise NotImplementedError
    #     index = read_llm_index(index_storage_folder=index_storage_folder)
    #     response_schemas = [
    #         ResponseSchema(name="rdfInfo", description="Give information about the loans found"),
    #         ResponseSchema(name="rdfName", description="Root node of RDF entity"),
    #         ResponseSchema(name="rdfChildren", description="list of all children under root node of RDF entity"),
    #     ]
    #     # request = """
    #     #     What loans are available from the SBA?
    #     #  """
    #     # request = """
    #     #     Who gives the 7a loan?
    #     #  """
    #     request = """
    #         What loans does the SBA offer?
    #      """
    #     # request = """
    #     #     What loans would a small business owner have access to?
    #     #  """
    #     # request = """
    #     #     What loans would a farmer have access to?
    #     #  """
    #     # request = """
    #     #     What loans does the USDA offer?
    #     #  """
    #     # request = """
    #     #     I am trying to expand my farm. What loans do I qualify for?
    #     #  """
    #     # raise NotImplementedError

    # lc_output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    # output_parser = LangchainOutputParser(lc_output_parser)

    # # NOTE: we use the same output parser for both prompts, though you can choose to use different parsers
    # # NOTE: here we add formatting instructions to the prompts.

    # fmt_qa_tmpl = output_parser.format(DEFAULT_TEXT_QA_PROMPT_TMPL)
    # fmt_refine_tmpl = output_parser.format(DEFAULT_REFINE_PROMPT_TMPL)

    # qa_prompt = QuestionAnswerPrompt(fmt_qa_tmpl, output_parser=output_parser)
    # refine_prompt = RefinePrompt(fmt_refine_tmpl, output_parser=output_parser)

    # # take a look at the new QA template! 
    # #print(fmt_qa_tmpl)

    # query_engine = index.as_query_engine(
    #     text_qa_template=qa_prompt, 
    #     refine_template=refine_prompt, 
    #     llm_predictor=llm_predictor
    # )
    # response = query_engine.query(request)

    # print(response)