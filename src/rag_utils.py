import os
import glob
from typing import List

# Langfuse imports
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

# Other necessary imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document


class RAGSystem:
    def __init__(self, google_api_key: str, langfuse_client: Langfuse, persist_directory: str):
        os.environ["GOOGLE_API_KEY"] = google_api_key
        self.persist_directory = persist_directory
        self.langfuse_client = langfuse_client

        # Initialize Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            # convert_system_message_to_human=True
        )
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Initialize Chroma client
        try:
            self.vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
            print(f"Loaded existing vector store from {persist_directory}")
        except Exception:
            print("No existing vector store found. Will create new one when documents are loaded.")
            self.vector_store = None    

    @observe(name="load_pdf_docs")
    def load_pdf_documents(self, docs_path: str) -> None:
        langfuse_context.update_current_trace(
            metadata={"docs_path": docs_path}
        )
        self.documents = []
        pdf_files = glob.glob(os.path.join(docs_path, '**', '*.pdf'), recursive=True)
        
        for pdf_path in pdf_files:
            try:
                loader = PyPDFLoader(pdf_path)
                pdf_docs = loader.load()
                self.documents.extend(pdf_docs)
            except Exception as e:
                print(f"Error loading {pdf_path}: {e}")
        
        # return documents
    
    @observe(name="split_documents")
    def split_documents(self) -> None: 
        chunk_size=1000
        chunk_overlap=200

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        langfuse_context.update_current_trace(
            metadata={
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap
            }
        )

        self.splits = text_splitter.split_documents(self.documents)
    
    @observe(name="vector_store")
    def vectorize_storing(self, collection_name: str = "default"): #select type for splits arg
        langfuse_context.update_current_trace(
            metadata={
                "collection_name": collection_name
            }
        )

        try:
            self.vector_store = Chroma.from_documents(
                documents=self.splits,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
                collection_name=collection_name
            )
            
            self.vector_store.persist()
            print(f"Vector store persisted to {self.persist_directory}")
            
        except Exception as e:
            print(f"Error during document loading: {e}")
            raise

    @observe(name="retriever")
    def retrieve(self, question: str, collection_name: str = "default") -> str:
        langfuse_context.update_current_trace(
            metadata={"question": question, "collection_name": collection_name}
        )
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please load documents first.")
        
        client = self.vector_store._client
        
        retriever = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=self.embeddings
        ).as_retriever(
            search_kwargs={'k': 1}
        )
        
        relevant_docs = retriever.get_relevant_documents(query=question)
        
        if not relevant_docs:
            return "No relevant documents found to answer the question."
        
        return relevant_docs
    
    @observe(name="query", as_type="generation")
    def query(self, relevant_docs: list[Document], question: str) -> str:
        langfuse_context.update_current_trace(
            metadata={"question": question}
        )
        if not relevant_docs:
            return "No relevant documents found to answer the question."
        
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Get current `production` version of text prompts
        langfuse_prompt = self.langfuse_client.get_prompt(name="RAG-Prompt")
        # langfuse_prompt.config("context":context, "question": question)

        # prompt_template = "Given the context: {context}, answer the question: {question}"
        formatted_prompt = langfuse_prompt.prompt.format(
            context=context, 
            question=question
        )
        # prompt = f"""Use the following context to answer the question. 
        # If you cannot find the answer in the context, say so.

        # Context:
        # {context}

        # Question: {question}"""

        response = self.llm.invoke(formatted_prompt)     
           
        return response.content


