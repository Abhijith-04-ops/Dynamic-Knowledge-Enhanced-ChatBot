# Dynamic-Knowledge-Enhanced-ChatBot

## Overview
This project implements a Retrieval-Augmented Generation (RAG) chatbot that dynamically updates its knowledge base using external web sources.

## Features
- Web scraping from trusted sources
- Text chunking and embedding generation
- FAISS-based semantic vector search
- Context-grounded response generation
- No model retraining required

## Architecture

```User Query → Retriever → Context Injection → LLM → Answer```

## Setup Instructions

### 1. Create virtual environment
```
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Pull Ollama model
```
ollama pull llama3
```

### 4. Build knowledge base
```
python data_updater.py
```

### 5. Run chatbot
```
python chat_bot.py
```
## Technologies Used
- LangChain (LCEL)
- FAISS
- Sentence Transformers
- Ollama (LLaMA3)
