# Libraries
import os
from dotenv import load_dotenv

from rag_utils import RAGSystem

from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context


# Load environment variables
load_dotenv("./.env")

# Environment configurations
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

# Set environment variables for Langfuse
os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
os.environ["LANGFUSE_HOST"] = LANGFUSE_HOST


# Configure the Langfuse context
langfuse_context.configure(
    secret_key=LANGFUSE_SECRET_KEY,
    public_key=LANGFUSE_PUBLIC_KEY,
    host=LANGFUSE_HOST,
    enabled=True
)

# Initialize Langfuse client
langfuse_client = Langfuse(
  host=LANGFUSE_HOST
)

@observe(name="RAG")
def main():

    # Initialize the RAG system
    rag = RAGSystem(
    google_api_key=GOOGLE_API_KEY,
    langfuse_client=langfuse_client,
    persist_directory="../chroma_db"
    )
    
    langfuse_context.update_current_trace(
    user_id="Nacho Ojeda Sanchez",
    session_id="test-20241211"
    )
    
    # Load documents
    rag.load_pdf_documents("../documents")

    # Split in chunks
    rag.split_documents()

    # Vector store
    rag.vectorize_storing()

    # Example query
    question = "Where does count Dracula live at the beginning of the story?"

    relevant_docs = rag.retrieve(question)
    response = rag.query(relevant_docs=relevant_docs, question=question)
    
    print(f"Question: {question}")
    print(f"Answer: {response}")

main()