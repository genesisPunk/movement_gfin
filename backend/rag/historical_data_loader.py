from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config import Config

def load_historical_data():
    loader = CSVLoader(
        Config.HISTORICAL_DATA_PATH,
        csv_args={'delimiter': ','},
        metadata_columns=['Date', 'Time']
    )
    docs = loader.load()
    return FAISS.from_documents(
        docs,
        OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
    )