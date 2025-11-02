from gemini_embedding import create_gemini_embedding
from openai_embedding import create_openai_embedding


def get_embedding_model():
    embedding_model = input("Enter the embedding model: (1) OpenAI (2) Gemini: ")
    if embedding_model == "1":
        embeddings = create_openai_embedding()
    elif embedding_model == "2":
        embeddings = create_gemini_embedding()
    else:
        raise ValueError("Invalid embedding model")
    return embeddings