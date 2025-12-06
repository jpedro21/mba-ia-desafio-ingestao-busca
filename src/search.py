import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector

from openai_embedding import create_openai_embedding
from util import get_embedding_model, get_llm_model


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

load_dotenv()

def search_prompt(question=None):

    embeddings = get_embedding_model()

    try:
      store = PGVector(
          embeddings=embeddings["embeddings"],
          collection_name=embeddings["collection_name"],
          connection=os.getenv("DATABASE_URL"),
          use_jsonb=True,
      )

      results = store.similarity_search(question, k=10)
      
      context = "\n".join([result.page_content for result in results])

      prompt = PROMPT_TEMPLATE.format(contexto=context, pergunta=question)

      response = get_llm_model().invoke(prompt)

      return response

    except Exception as e:
      print(f"Error during search: {type(e).__name__}: {str(e)}")
      raise
