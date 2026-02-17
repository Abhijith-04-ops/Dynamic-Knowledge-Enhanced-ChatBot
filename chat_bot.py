from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import warnings
warnings.filterwarnings("ignore")

from vector_store import load_db

# -------------------------
# Load Vector DB
# -------------------------
db = load_db()
print("Total vectors in DB:", db.index.ntotal)
retriever = db.as_retriever(search_kwargs={"k": 5})

# -------------------------
# LLM
# -------------------------
llm = Ollama(model="llama3")

# -------------------------
# Prompt
# -------------------------
prompt = ChatPromptTemplate.from_template(
    """
    You are a domain-specific intelligent assistant.
    Refer the given context and answer the questions.
    Do NOT mention the word "context" in your answer.
    Do NOT say phrases like "according to the context".
    Answer naturally and directly.
    If the answer is not in the context, say "I don't know".
    Also give suggestions on related topics.

    Context:
    {context}

    Question:
    {question}
    """
)

# -------------------------
# LCEL PIPELINE
# -------------------------
rag_pipeline = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# -------------------------
# Chat Loop
# -------------------------
while True:
    query = input("\nYou: ")
    if query.lower() in ["exit", "quit"]:
        break

    response = rag_pipeline.invoke(query)
    print("\nBot :", response)
