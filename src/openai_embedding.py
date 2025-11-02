import os
from langchain_openai import OpenAIEmbeddings


def create_openai_embedding():
    openai_base_url = os.getenv("OPENAI_BASE_URL")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    if openai_base_url:
        embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_base=openai_base_url
        )
    else:
        embeddings = OpenAIEmbeddings(model=embedding_model)

    return {"embeddings": embeddings, "collection_name": "gpt5_collection"}