import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.historical_data_loader import load_historical_data
from config import Config

vector_store = load_historical_data()
vector_store.save_local(Config.VECTOR_STORE_PATH)
print("Vector store initialized successfully!")