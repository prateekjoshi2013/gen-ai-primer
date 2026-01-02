# ref: https://docs.langchain.com/oss/python/langchain/knowledge-base#installation
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents():
    pdf_path = Path(__file__).parent / "k8s-ops-book.pdf"
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return docs

def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Adjusted chunk size for better context
        chunk_overlap=400, # Adjusted overlap for better context retention so that important information is not lost between chunks
    )
    chunks = text_splitter.split_documents(docs)
    return chunks

if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)