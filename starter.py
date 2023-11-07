from dotenv import load_dotenv

load_dotenv()  # This loads the .env file variables into the environment

import os
import logging
import sys
import os.path
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage



# Load the OPENAI_API_KEY from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable has not been set.")

logging.basicConfig(stream=sys.stdout, level=logging.INFO) #logging.INFO or logging.DEBUG
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# check if storage already exists
if (not os.path.exists('./storage')):
    # load the documents and create the index
    documents = SimpleDirectoryReader('data').load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist()
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context)

# either way we can now query the index
# query_engine = index.as_query_engine(streaming=True)
query_engine = index.as_chat_engine()
# response = query_engine.query("What is a locked room?")
response = query_engine.chat("What is the address of a the fairmount location?")

print(response)

response = query_engine.chat("What is the other two addresses?")

print(response)




