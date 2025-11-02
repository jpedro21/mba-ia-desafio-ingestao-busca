# Desafio MBA Engenharia de Software com IA - Full Cycle

## 📋 Sobre o Projeto

Este projeto implementa um sistema de **RAG (Retrieval-Augmented Generation)** para ingestão e busca em documentos PDF. O sistema permite fazer perguntas sobre o conteúdo de documentos e receber respostas precisas baseadas apenas no contexto fornecido, evitando alucinações do modelo de linguagem.

### Principais Funcionalidades

- **Ingestão de PDFs**: Carrega e processa documentos PDF, dividindo-os em chunks otimizados
- **Embeddings**: Suporte para dois modelos de embedding:
  - OpenAI (text-embedding-3-small)
  - Google Gemini (text-embedding-004)
- **Armazenamento Vetorial**: Utiliza PostgreSQL com extensão PGVector para busca semântica eficiente
- **Busca Inteligente**: Sistema de busca por similaridade que retorna os trechos mais relevantes
- **Chat Interativo**: Interface de chat que responde perguntas baseadas no contexto dos documentos

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**: Linguagem principal
- **LangChain**: Framework para aplicações com LLMs
- **PostgreSQL + PGVector**: Banco de dados vetorial
- **OpenAI API**: Embeddings e modelo de linguagem
- **Google Gemini API**: Embeddings alternativos
- **Docker**: Containerização do banco de dados

## 📦 Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- Chaves de API (pelo menos uma):
  - OpenAI API Key
  - Google API Key (para Gemini)

## 🚀 Configuração e Instalação

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

### 2. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configuração do Banco de Dados
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documents_collection

# Caminho do PDF a ser processado
PDF_PATH=./document.pdf

# Configuração OpenAI (obrigatório para usar embeddings OpenAI e chat)
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_BASE_URL=https://api.openai.com/v1

# Configuração Google Gemini (obrigatório apenas se usar embeddings Gemini)
GOOGLE_API_KEY=sua_chave_google_aqui
GEMINI_EMBEDDING_MODEL=models/text-embedding-004
```

**⚠️ Importante**: Nunca compartilhe suas chaves de API. Adicione o arquivo `.env` ao `.gitignore`.

### 3. Inicie o Banco de Dados PostgreSQL

Execute o Docker Compose para subir o PostgreSQL com PGVector:

```bash
docker-compose up -d
```

Isso irá:
- Criar um container PostgreSQL com a extensão PGVector
- Expor o banco na porta 5432
- Criar automaticamente a extensão vector no banco de dados

### 4. Crie o Ambiente Virtual e Instale as Dependências

```bash
# Criar ambiente virtual
python3.12 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate  # No Linux/Mac
# ou
.\venv\Scripts\activate   # No Windows

# Instalar dependências
pip install -r requirements.txt
```

## 📚 Como Usar

### Passo 1: Ingestão do Documento

Antes de fazer buscas, você precisa processar e ingerir o documento PDF:

```bash
python src/ingest.py
```

Durante a execução, você será solicitado a escolher o modelo de embedding:
- Digite `1` para usar **OpenAI**
- Digite `2` para usar **Google Gemini**

O script irá:
1. Carregar o PDF especificado em `PDF_PATH`
2. Dividir o documento em chunks de 1000 caracteres com overlap de 150
3. Gerar embeddings para cada chunk
4. Armazenar os embeddings no PostgreSQL/PGVector

**Saída esperada**:
```
Starting PDF ingestion...
Loading PDF from: ./document.pdf
Successfully split PDF into 245 chunks
Creating embeddings model...
Enter the embedding model: (1) OpenAI (2) Gemini: 1
Connecting to PGVector database...
✓ Successfully ingested 245 documents into collection 'gpt5_collection'
```

### Passo 2: Realizar Buscas

Após a ingestão, você pode iniciar o chat interativo:

```bash
python src/chat.py
```

Durante a execução, você será solicitado a escolher o modelo de embedding (deve ser o mesmo usado na ingestão):
- Digite `1` para usar **OpenAI**
- Digite `2` para usar **Google Gemini**

**Exemplo de uso**:
```
Enter the embedding model: (1) OpenAI (2) Gemini: 1
Digite sua pergunta ou 'sair' para encerrar: Qual é o tema principal do documento?
[Resposta baseada no contexto do documento]

Digite sua pergunta ou 'sair' para encerrar: sair
```

### Busca Direta (Opcional)

Você também pode usar o módulo de busca diretamente em seus próprios scripts:

```python
from src.search import search_prompt

resposta = search_prompt("Sua pergunta aqui")
print(resposta)
```

## 🔍 Como Funciona

### 1. Processo de Ingestão

```
PDF → Carregamento → Divisão em Chunks → Geração de Embeddings → Armazenamento no PGVector
```

- **RecursiveCharacterTextSplitter**: Divide o texto mantendo contexto entre chunks
- **Embeddings**: Converte texto em vetores numéricos que capturam o significado semântico
- **PGVector**: Armazena os vetores com índices otimizados para busca de similaridade

### 2. Processo de Busca

```
Pergunta → Embedding da Pergunta → Busca por Similaridade → Recuperação de Contexto → LLM → Resposta
```

- Sua pergunta é convertida em embedding usando o mesmo modelo da ingestão
- O sistema busca os 10 chunks mais similares no banco vetorial
- O contexto relevante é enviado para o GPT-4o-mini junto com sua pergunta
- O modelo responde **apenas** com base no contexto fornecido

### 3. Proteções contra Alucinações

O sistema usa um prompt template rigoroso que:
- Instrui o modelo a responder **apenas** com base no contexto
- Define resposta padrão para perguntas fora do escopo
- Proíbe uso de conhecimento externo ou opiniões

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── docker-compose.yml          # Configuração do PostgreSQL + PGVector
├── document.pdf                # Documento a ser processado
├── requirements.txt            # Dependências Python
├── .env                        # Variáveis de ambiente (não versionado)
├── README.md                   # Documentação
└── src/
    ├── ingest.py              # Script de ingestão de PDFs
    ├── search.py              # Motor de busca e geração de respostas
    ├── chat.py                # Interface de chat interativo
    ├── openai_embedding.py    # Configuração de embeddings OpenAI
    ├── gemini_embedding.py    # Configuração de embeddings Gemini
    └── util.py                # Utilitários compartilhados
```

## 🔧 Troubleshooting

### Erro de Conexão com o Banco

```
Error: connection to server at "localhost" (::1), port 5432 failed
```

**Solução**: Verifique se o Docker está rodando e se o container PostgreSQL está ativo:
```bash
docker-compose ps
docker-compose logs postgres
```

### Erro de API Key

```
Error: Invalid API key
```

**Solução**: Verifique se as chaves estão corretas no arquivo `.env` e se o ambiente foi carregado.

### Embeddings Incompatíveis

Se você mudou o modelo de embedding entre a ingestão e a busca, os resultados serão inconsistentes.

**Solução**: Use sempre o mesmo modelo para ingestão e busca, ou re-ingira os documentos com o novo modelo.

## 🎯 Melhores Práticas

1. **Escolha do Modelo de Embedding**: 
   - Use o mesmo modelo consistentemente para ingestão e busca
   - OpenAI: Mais rápido e preciso
   - Gemini: Alternativa gratuita para volumes menores

2. **Tamanho dos Chunks**: 
   - Ajuste `chunk_size` e `chunk_overlap` em `ingest.py` conforme o tipo de documento
   - Documentos técnicos: chunks menores (500-1000)
   - Documentos narrativos: chunks maiores (1000-2000)

3. **Número de Resultados (k)**: 
   - Ajuste o parâmetro `k` em `search.py` (atualmente 10)
   - Mais contexto: aumentar k
   - Respostas mais focadas: diminuir k

## 📝 Licença

Este projeto foi desenvolvido como parte do MBA em Engenharia de Software com IA da Full Cycle.

## 🤝 Contribuições

Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.
