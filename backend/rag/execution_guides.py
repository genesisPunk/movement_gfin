from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

execution_knowledge = [
    "Buy MOVEMENT: 1. Login 2. Navigate to Spot 3. Enter amount",
    "Sell MOVEMENT: 1. Select limit order 2. Set price 3. Confirm"
]

vector_store = FAISS.from_texts(
    execution_knowledge,
    embedding=OpenAIEmbeddings()
)