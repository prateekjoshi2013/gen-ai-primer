# ref: https://docs.langchain.com/oss/python/langchain/knowledge-base#installation
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_documents():
    pdf_path = Path(__file__).parent / "k8s-ops-book.pdf"
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return docs

if __name__ == "__main__":
    load_documents()
