from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from langchain_qdrant import QdrantVectorStore


# needs the OPENAI_API_KEY environment variable set
client = OpenAI()


def create_embedding_model():
    '''
    Create and return an OpenAI embedding model.
    '''
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
    return embedding_model

# Define system prompt for the chat model
def system_prompt(c):
    return f"""

    You are a kubernetes expert in writing kubernetes operators and are going to help with kubernetes operators
    related questions using the context provided as CONTEXT only and 
    also suggest which pages to refer to from Page Number and File mentioned in the context.
    If the question is not related to kubernetes operators, politely refuse to answer.

    CONTEXT:
    {c}    
    """

# Initialize Qdrant vector store client from existing collection
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://qdrant:6333", collection_name="k8s-ops-book", embedding=create_embedding_model()
)


def process_query(query):
    '''
    Process a user query by retrieving context from the vector database and generating a response.
    '''
    if query.lower() == "exit":
        return

    search_results = vector_db.similarity_search(query)
    context = "\n\n\n".join(
        [
            f"Page Content:{doc.page_content}\nPage Number: {doc.metadata['page_label']}\nFile: {doc.metadata['source']}"
            for doc in search_results
        ]
    )
    print("🧠 Retrieved Context: ", context)
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": system_prompt(context)},
            {"role": "user", "content": query},
        ],
    )
    return response.choices[0].message.content
