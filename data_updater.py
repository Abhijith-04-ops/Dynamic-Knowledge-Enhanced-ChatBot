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



