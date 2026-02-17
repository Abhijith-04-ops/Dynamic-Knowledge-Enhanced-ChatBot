from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import warnings
warnings.filterwarnings("ignore")

EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
DB_PATH = "vector_db"

def load_db():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Vector DB not found. Run data_updater.py first.")
    return FAISS.load_local(DB_PATH, 
                            EMBEDDING_MODEL,
                            allow_dangerous_deserialization=True)

def create_db(texts):
    db = FAISS.from_texts(texts, EMBEDDING_MODEL)
    db.save_local(DB_PATH)

def add_texts_to_db(texts):
    db = load_db()
    db.add_texts(texts)
    db.save_local(DB_PATH)


