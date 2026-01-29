import os
import fitz
import requests
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


FAISS_PATH = "vectorstore/faiss_index"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ------------------ PDF LOADING ------------------

def load_pdf(pdf_path: str):
    docs = []
    pdf = fitz.open(pdf_path)

    for page_num, page in enumerate(pdf):
        text = page.get_text()
        if text.strip():
            docs.append(
                Document(
                    page_content=text,
                    metadata={"page": page_num + 1}
                )
            )
    return docs

# ------------------ INDEX BUILD ------------------

def build_faiss_index(pdf_path: str):
    docs = load_pdf(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    db = FAISS.from_documents(chunks, embeddings)
    os.makedirs(FAISS_PATH, exist_ok=True)
    db.save_local(FAISS_PATH)

# ------------------ RAG ANSWER ------------------

def rag_answer(query: str) -> str:
    db = FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(query, k=4)

    context = "\n\n".join(
        f"(Page {d.metadata['page']}) {d.page_content}"
        for d in docs
    )

    prompt = f"""
You are a financial document assistant.
Answer ONLY from the context below.
If the answer is not present, say "Not found in the document".

Context:
{context}

Question:
{query}

Answer:
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    return response.json()["response"].strip()
