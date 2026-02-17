# import requests
# from bs4 import BeautifulSoup
# from vector_store import *
# import schedule
# import time

# def fetch_data_from_url(url):
#     """
#     Extracts text from a webpage
#     """
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     text = soup.get_text(separator=" ")
#     return text

# def chunk_text(text, chunk_size=500):
#     """
#     Splits large text into smaller chunks
#     """
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), chunk_size):
#         chunk = " ".join(words[i:i+chunk_size])
#         chunks.append(chunk)
#     return chunks

# def update_knowledge_base():
#     """
#     Main update pipeline
#     """
#     with open("sources.txt") as f:
#         urls = f.readlines()

#     all_new_chunks = []

#     for url in urls:
#         url = url.strip()
#         print(f"Fetching from {url}")
#         raw_text = fetch_data_from_url(url)
#         chunks = chunk_text(raw_text)
#         all_new_chunks.extend(chunks)

#     add_texts_to_db(all_new_chunks)
#     print("Knowledge base updated!")

# # Run every 24 hours
# schedule.every(24).hours.do(update_knowledge_base)

# while True:
#     schedule.run_pending()
#     time.sleep(60)

# import requests
# from bs4 import BeautifulSoup
# import schedule
# import time
# from vector_store import add_texts_to_db, create_db
# import os
# import warnings
# warnings.filterwarnings("ignore")

# def fetch_text(url):
#     print(f"Fetching url: {url}")
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     return soup.get_text(separator=" ")

# def fetch_text(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Remove scripts, styles, nav
#     for tag in soup(["script", "style", "nav", "footer", "header"]):
#         tag.decompose()

#     text = soup.get_text(separator=" ")
#     return " ".join(text.split())  # normalize whitespace

# def chunk_text(text, chunk_size=600):
#     print('Chunking in progress....')
#     words = text.split()
#     return [
#         " ".join(words[i:i + chunk_size])
#         for i in range(0, len(words), chunk_size)
#     ]

# def chunk_text(text, chunk_size=1000, overlap=200):
#     """
#     Split text into overlapping character-based chunks.
#     This works much better for Wikipedia-style content.
#     """
#     chunks = []
#     start = 0
#     text_length = len(text)

#     while start < text_length:
#         end = start + chunk_size
#         chunk = text[start:end]
#         chunks.append(chunk)
#         start = end - overlap  # overlap preserves context

#     return chunks

# import requests
# from bs4 import BeautifulSoup

# def fetch_text(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     for tag in soup(["script", "style", "nav", "footer", "header"]):
#         tag.decompose()
#     return " ".join(soup.get_text(separator=" ").split())

# def fetch_text(url):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                       "AppleWebKit/537.36 (KHTML, like Gecko) "
#                       "Chrome/120.0 Safari/537.36"
#     }

#     response = requests.get(url, headers=headers, timeout=30)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.text, "html.parser")

#     for tag in soup(["script", "style", "nav", "footer", "header"]):
#         tag.decompose()

#     text = soup.get_text(separator=" ")
#     return " ".join(text.split())


# def chunk_text(text, chunk_size=1000, overlap=200):
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + chunk_size
#         chunks.append(text[start:end])
#         start = end - overlap
#     return chunks

# # url = "https://en.wikipedia.org/wiki/Machine_learning"
# # text = fetch_text(url)
# # chunks = chunk_text(text)

# # print("TEXT LENGTH:", len(text))
# # print("NUMBER OF CHUNKS:", len(chunks))
# # print("FIRST CHUNK PREVIEW:\n", chunks[0][:300])


# def update_knowledge_base():
#     print("Updating Knowledge Base....")
#     with open("sources.txt") as f:
#         urls = [u.strip() for u in f.readlines()]

#     all_chunks = []

#     for url in urls:
#         print(f"Fetching: {url}")
#         text = fetch_text(url)
#         chunks = chunk_text(text)
#         all_chunks.extend(chunks)

#     if not os.path.exists("vector_db"):
#         create_db(all_chunks)
#     else:
#         add_texts_to_db(all_chunks)
#     # create_db(all_chunks)
#     # print("DB rebuilt with chunks:", len(all_chunks))

#     print("✅ Knowledge base updated")

# schedule.every(24).hours.do(update_knowledge_base)

# if __name__ == "__main__":
#     update_knowledge_base()
#     while True:
#         schedule.run_pending()
#         time.sleep(60)

#=================================================================================================================================================================
import requests
from bs4 import BeautifulSoup
import os
import time
import schedule
from vector_store import create_db

# ----------------------------------
# Configuration
# ----------------------------------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 250
DB_PATH = "vector_db"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# ----------------------------------
# Fetch WEB  text
# ----------------------------------
def fetch_text(url: str) -> str:
    response = requests.get(url, headers=HEADERS,timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-content sections
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = " ".join(text.split())  # normalize whitespace
    return text
# ----------------------------------
# Chunking (character-based, overlapping)
# ----------------------------------
def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

# ----------------------------------
# Main update pipeline
# ----------------------------------
def update_knowledge_base():
    with open("sources.txt", "r",encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    all_chunks = []

    print("\n🔄 Starting knowledge base update...\n")

    for url in urls:
        print(f"📥 Fetching: {url}")
        text = fetch_text(url)

        print(f"   Text length: {len(text)} characters")

        chunks = chunk_text(text)
        print(f"   Chunks created: {len(chunks)}")

        all_chunks.extend(chunks)

    print("\n📊 TOTAL CHUNKS BEFORE FAISS:", len(all_chunks))
    

    # ----------------------------------
    # FORCE REBUILD VECTOR DB
    # ----------------------------------
    if os.path.exists(DB_PATH):
        print("\n🗑️ Removing old vector DB...")
        if os.name == "nt":
            os.system("rmdir /s /q vector_db")
        else:
            os.system("rm -rf vector_db")

    print("\n📦 Creating new vector database...")
    create_db(all_chunks)

    print("\n✅ Knowledge base successfully rebuilt!")
    print("✅ You can now start chat_bot.py\n")

# ----------------------------------
# Scheduler (optional – safe to stop)
# ----------------------------------
# schedule.every(24).hours.do(update_knowledge_base)

if __name__ == "__main__":
    update_knowledge_base()

    # Comment out this loop if you don't want scheduling
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)



