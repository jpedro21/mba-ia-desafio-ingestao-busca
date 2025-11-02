import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

from gemini_embedding import create_gemini_embedding
from openai_embedding import create_openai_embedding
from util import get_embedding_model

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    print("Starting PDF ingestion...")
    
    print(f"Loading PDF from: {PDF_PATH}")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    loader = PyPDFLoader(PDF_PATH)
    chunks = splitter.split_documents(loader.load())

    if not chunks:
        print("Failed to split PDF into chunks")
        return
    
    print(f"Successfully split PDF into {len(chunks)} chunks")
    
    enriched = [
        Document(
            page_content=p.page_content,
            metadata={k: v for k, v in p.metadata.items() if v not in ("", None)} 
        )
        for p in chunks
    ]

    print("Creating embeddings model...")
    embeddings = get_embedding_model()

    ids = [f"doc-{embeddings['collection_name']}-{i}" for i in range(len(enriched))]
    
    print("Connecting to PGVector database...")
    print(f"Collection name: {os.getenv('PG_VECTOR_COLLECTION_NAME')}")
    print(f"Database URL: {os.getenv('DATABASE_URL')}")
    
    try:
        store = PGVector(
            embeddings=embeddings["embeddings"],
            collection_name=embeddings["collection_name"],
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )
        print("Connection established successfully")
        
        print(f"Adding {len(enriched)} documents to the vector store...")
        store.add_documents(enriched, ids=ids)
        print(f"✓ Successfully ingested {len(ids)} documents into collection '{embeddings['collection_name']}'")
        
    except Exception as e:
        print(f"Error during ingestion: {type(e).__name__}: {str(e)}")
        raise

if __name__ == "__main__":
    ingest_pdf()