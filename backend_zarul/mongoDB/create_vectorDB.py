# Create vector database(mongodb)
import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
  model="models/embedding-001",
  google_api_key=api_key
  )

client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))

DB_NAME = "test_db"
COLLECTION_NAME = "cost_collection_pdf"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "cost-index-pdf"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
  collection=MONGODB_COLLECTION,
  embedding=embeddings,
  index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
  relevance_score_fn="cosine",
)

vector_store.create_vector_search_index(dimensions=768)

print("Vector Store Created!")
client.close()