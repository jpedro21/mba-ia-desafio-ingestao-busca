import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def create_gemini_embedding():
    """
    Cria e retorna uma instância de GoogleGenerativeAIEmbeddings.
    
    Configurações via variáveis de ambiente:
    - GOOGLE_API_KEY: API key do Google (obrigatório)
    - GEMINI_EMBEDDING_MODEL: modelo de embedding (padrão: models/embedding-001)
    
    Modelos disponíveis:
    - models/embedding-001: 768 dimensões
    - models/text-embedding-004: 768 dimensões (mais recente)
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
    
    # Modelo padrão recomendado para embeddings do Gemini (mais recente)
    embedding_model = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model=embedding_model,
        google_api_key=api_key
    )
    
    return {"embeddings": embeddings, "collection_name": "gemini-2.5-flash-lite"}
