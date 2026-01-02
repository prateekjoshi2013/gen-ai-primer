# ref: https://docs.langchain.com/oss/python/langchain/knowledge-base#installation
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

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

def create_embedding_model():
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-large"  # Example embedding model
    )
    return embedding_model

def create_vector_store(chunks, embedding_model):
    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url="http://qdrant:6333",  # Qdrant server URL
        collection_name="k8s-ops-book"  # Example collection name
    )
    return vector_store

if __name__ == "__main__":
    print("Loading and processing and indexing documents in Qdrant Vector Database...")
    docs = load_documents()
    chunks = split_documents(docs)
    embedding_model = create_embedding_model()
    vector_store = create_vector_store(chunks, embedding_model)