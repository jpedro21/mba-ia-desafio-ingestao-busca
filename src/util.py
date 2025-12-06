from gemini_embedding import create_gemini_embedding
from openai_embedding import create_openai_embedding
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI as Gemini


selected_embedding_model = None

def get_embedding_model():
    global selected_embedding_model
    embedding_model = input("Enter the embedding model: (1) OpenAI (2) Gemini: ")
    if embedding_model == "1":
        selected_embedding_model = "openai"
        embeddings = create_openai_embedding()
    elif embedding_model == "2":
        selected_embedding_model = "gemini"
        embeddings = create_gemini_embedding()
    else:
        raise ValueError("Invalid embedding model")
    return embeddings

def get_llm_model():
    if selected_embedding_model == "openai":
        llm = ChatOpenAI(model="gpt-4o-mini")
    elif selected_embedding_model == "gemini":
        llm = Gemini(model="gemini-2.5-flash-lite")
    else:
        raise ValueError("Invalid LLM model")
    return llm