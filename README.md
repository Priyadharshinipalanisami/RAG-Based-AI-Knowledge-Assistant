# 🤖 RAG-Based AI Knowledge Assistant

A complete Retrieval-Augmented Generation application that lets users upload documents and ask natural-language questions about them.

## ✨ Features

- PDF, DOCX, TXT and Markdown support
- Automatic document extraction
- Text cleaning and overlapping chunking
- Sentence Transformer embeddings
- Cosine-similarity vector retrieval
- Top-K relevant context selection
- Ollama local LLM support
- Extractive fallback when Ollama is unavailable
- Source documents and similarity scores
- Modern responsive dashboard
- Sample knowledge documents
- GitHub-ready project structure

## 🏗️ Architecture

```text
                 ┌───────────────────────┐
                 │       User            │
                 └──────────┬────────────┘
                            │
                            ▼
                 ┌───────────────────────┐
                 │     Flask Web UI      │
                 └───────┬───────┬───────┘
                         │       │
             Upload      │       │ Ask
                         ▼       ▼
              ┌────────────┐  ┌───────────────┐
              │  Document  │  │ Query         │
              │  Loader    │  │ Embedding     │
              └─────┬──────┘  └──────┬────────┘
                    ▼                  │
              ┌────────────┐           │
              │  Chunking  │           │
              └─────┬──────┘           │
                    ▼                  │
              ┌────────────┐           │
              │ Embeddings │           │
              └─────┬──────┘           │
                    ▼                  ▼
              ┌────────────────────────────┐
              │      Vector Store           │
              │   Cosine Similarity Search  │
              └─────────────┬──────────────┘
                            │
                       Top-K Chunks
                            │
                            ▼
                 ┌───────────────────────┐
                 │  Context + Question   │
                 └───────────┬───────────┘
                             ▼
                 ┌───────────────────────┐
                 │ Ollama Local LLM      │
                 │ or Fallback Generator │
                 └───────────┬───────────┘
                             ▼
                 ┌───────────────────────┐
                 │ Answer + Sources      │
                 └───────────────────────┘
```

## 📁 Project Structure

```text
RAG_AI_Knowledge_Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
│
├── documents/
│   ├── rag_overview.txt
│   ├── machine_learning.txt
│   ├── cloud_computing.txt
│   └── .gitkeep
│
├── rag/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── generator.py
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 🛠️ Installation — Windows

Open PowerShell in the project folder:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The first startup may take time because the Sentence Transformer model is downloaded.

## 🧠 Optional: Ollama

Install Ollama and download a model:

```powershell
ollama pull llama3.2:3b
```

Start Ollama:

```powershell
ollama serve
```

Default configuration:

```text
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

If Ollama is not running, the application automatically uses the built-in extractive fallback.

## 📄 Sample Questions

After starting the application, try:

```text
What is RAG?
What are the stages of a RAG pipeline?
What is supervised learning?
What is Random Forest?
What is cloud computing?
What are the three cloud service models?
```

## 🔬 RAG Pipeline

### 1. Document Processing

The application reads PDF, DOCX, TXT and Markdown files.

### 2. Chunking

Documents are divided into approximately 900-character chunks with 150-character overlap.

### 3. Embeddings

The application uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to convert text into numerical vectors.

### 4. Retrieval

The question is embedded and compared with document embeddings using cosine similarity.

The five most relevant chunks are retrieved.

### 5. Generation

The retrieved chunks are inserted into a grounded prompt.

If Ollama is available, the local LLM generates the answer.

Otherwise, the fallback generator extracts relevant sentences from the retrieved context.

## 🎥 Demo Video Plan

Record a 2–3 minute video:

1. Introduce the project.
2. Show the architecture.
3. Start Flask.
4. Open the web application.
5. Show sample documents.
6. Ask a question.
7. Show the generated answer.
8. Show retrieved sources.
9. Upload a new document.
10. Ask a question about the new document.
11. Explain embeddings and vector search.
12. Explain Ollama/fallback generation.

## 📸 Screenshots Checklist

Add these screenshots to your GitHub repository:

```text
screenshots/
├── home.png
├── document-upload.png
├── question-answer.png
├── retrieved-sources.png
└── architecture.png
```

## 🐙 GitHub

Recommended repository name:

```text
RAG-Based-AI-Knowledge-Assistant
```

Upload the complete project folder to GitHub.

Suggested commit:

```text
Initial commit - RAG Based AI Knowledge Assistant
```

## 🚀 Future Improvements

- FAISS/Chroma/Qdrant persistent vector database
- User authentication
- Chat history
- Streaming LLM responses
- Multiple LLM providers
- OCR for scanned PDFs
- Reranking models
- Conversation memory
- Docker deployment
- Cloud deployment
- Admin document management

## 📜 License

MIT License.
