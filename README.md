# 🤖 RAG-Based AI Knowledge Assistant

> **A document-grounded AI assistant that lets users upload their own documents and ask natural-language questions using Retrieval-Augmented Generation (RAG).**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![RAG](https://img.shields.io/badge/AI-RAG-purple)
![Sentence Transformers](https://img.shields.io/badge/Embeddings-Sentence--Transformers-orange)
![Ollama](https://img.shields.io/badge/LLM-Ollama-white)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Overview

The **RAG-Based AI Knowledge Assistant** is an AI-powered document question-answering system that allows users to upload documents and interact with their content using natural language.

Instead of relying only on information learned during model training, the application retrieves relevant information directly from the uploaded documents and uses that information to generate grounded answers.

The system combines:

* 📄 Document processing
* ✂️ Intelligent text chunking
* 🧠 Semantic embeddings
* 🔎 Vector similarity search
* 🤖 Local LLM generation using Ollama
* 📚 Source-aware answers
* 🔄 Automatic fallback when the LLM is unavailable

This makes the application useful for **students, researchers, developers, organizations, and knowledge-management systems**.

---

## 🎯 Objectives

The main objectives of this project are:

1. Build a document-based AI question-answering system.
2. Implement a complete Retrieval-Augmented Generation pipeline.
3. Convert document content into semantic vector embeddings.
4. Retrieve the most relevant information for a user query.
5. Generate answers using a local Large Language Model.
6. Provide source information for retrieved content.
7. Maintain functionality even when the local LLM is unavailable.

---

## ✨ Key Features

### 📄 Multi-Format Document Support

Users can upload:

* PDF
* DOCX
* TXT
* Markdown (`.md`)

### 🧹 Automatic Document Processing

Uploaded documents are automatically:

1. Loaded
2. Cleaned
3. Split into overlapping chunks
4. Converted into embeddings
5. Added to the vector store

### 🧠 Semantic Search

The system uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to generate vector representations of documents and questions.

### 🔎 Top-K Retrieval

For every question, the system retrieves the **5 most relevant document chunks** using vector similarity.

### 🤖 Local AI with Ollama

The application can use an Ollama-hosted local LLM to generate grounded answers.

Default model:

```text
llama3.2:3b
```

### 🔄 Automatic Fallback

If Ollama is unavailable, the application automatically switches to an extractive fallback mechanism.

This means the application can still provide useful information without requiring a running LLM.

### 📚 Source Display

The application returns:

* Source document
* Similarity score
* Relevant text preview

This improves transparency and helps users understand where the answer came from.

### 🌐 Web Interface

A responsive Flask web interface provides:

* Document upload
* Document listing
* Question input
* AI-generated answers
* Retrieved source information

---

# 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Flask Web UI     │
                  └─────────┬───────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
      ┌───────────────┐           ┌────────────────┐
      │ Document      │           │ User Question  │
      │ Upload        │           └───────┬────────┘
      └───────┬───────┘                   │
              ▼                           ▼
      ┌───────────────┐           ┌────────────────┐
      │ Document      │           │ Query          │
      │ Loader        │           │ Embedding      │
      └───────┬───────┘           └───────┬────────┘
              ▼                           │
      ┌───────────────┐                   │
      │ Text Cleaning │                   │
      │ & Chunking    │                   │
      └───────┬───────┘                   │
              ▼                           │
      ┌───────────────┐                   │
      │ Sentence      │                   │
      │ Embeddings    │                   │
      └───────┬───────┘                   │
              │                           │
              └─────────────┬─────────────┘
                            ▼
                  ┌─────────────────────┐
                  │    Vector Store     │
                  │ Cosine Similarity   │
                  └─────────┬───────────┘
                            │
                         Top-K
                        Results
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Context + Question  │
                  └─────────┬───────────┘
                            ▼
              ┌────────────────────────────┐
              │       Ollama LLM           │
              │            OR              │
              │   Extractive Fallback      │
              └────────────┬───────────────┘
                           ▼
                  ┌─────────────────────┐
                  │ Answer + Sources    │
                  └─────────────────────┘
```

---

# 🔬 How the RAG Pipeline Works

## 1️⃣ Document Upload

The user uploads one or more supported documents.

Supported formats:

```text
PDF
DOCX
TXT
MD
```

---

## 2️⃣ Document Extraction

The application extracts text using:

* `pypdf` for PDF files
* `python-docx` for DOCX files
* Python file handling for TXT and Markdown

---

## 3️⃣ Text Cleaning

The extracted text is cleaned by:

* Removing null characters
* Normalizing spaces
* Removing excessive blank lines
* Removing unnecessary whitespace

---

## 4️⃣ Text Chunking

Large documents are divided into smaller chunks.

Default configuration:

```text
Chunk Size: 900 characters
Overlap:    150 characters
```

The overlap helps preserve context between neighboring chunks.

---

## 5️⃣ Embedding Generation

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

These embeddings allow the system to compare the semantic meaning of questions and document sections.

---

## 6️⃣ Similarity Search

When the user asks a question:

```text
Question
   ↓
Query Embedding
   ↓
Similarity Calculation
   ↓
Top 5 Relevant Chunks
```

The application uses normalized embeddings and vector dot products to perform cosine-similarity-style retrieval.

---

## 7️⃣ Context Construction

The retrieved document chunks are combined into a context that is provided to the language model.

The model is instructed to answer using only the supplied context.

---

## 8️⃣ Answer Generation

If Ollama is available:

```text
Question + Retrieved Context
             ↓
        Ollama LLM
             ↓
       Grounded Answer
```

If Ollama is unavailable:

```text
Retrieved Context
       ↓
Keyword/Sentence Matching
       ↓
Fallback Answer
```

---

# 🛠️ Technologies Used

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Core programming language |
| Flask                 | Web application framework |
| Sentence Transformers | Semantic embeddings       |
| NumPy                 | Vector operations         |
| pypdf                 | PDF text extraction       |
| python-docx           | DOCX processing           |
| Ollama                | Local LLM inference       |
| HTML/CSS/JavaScript   | Frontend interface        |

---

# 📁 Project Structure

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
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── scripts/
    └── run_windows.bat
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Priyadhashinipalanisami/RAG-Based-AI-Knowledge-Assistant.git
```

Move into the project directory:

```bash
cd RAG-Based-AI-Knowledge-Assistant
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
py -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

# 🤖 Optional Ollama Setup

Ollama can be used to provide local LLM-powered responses.

Install Ollama and download the recommended model:

```bash
ollama pull llama3.2:3b
```

Start Ollama:

```bash
ollama serve
```

The default configuration is:

```text
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

You can customize these values using environment variables.

Example:

```text
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

> **Note:** Ollama is optional. If it is unavailable, the application automatically uses the built-in fallback generator.

---

# 📄 Example Questions

After uploading the sample documents, try questions such as:

```text
What is RAG?

What are the stages of a RAG pipeline?

What is supervised learning?

What is Random Forest?

What is cloud computing?

What are the three cloud service models?
```

You can also upload your own documents and ask questions about their contents.

---

# 🧪 Example Workflow

```text
1. Start the Flask application
        ↓
2. Open the web interface
        ↓
3. Upload a PDF/DOCX/TXT/MD document
        ↓
4. Document is automatically indexed
        ↓
5. Enter a natural-language question
        ↓
6. Query is converted into an embedding
        ↓
7. Relevant chunks are retrieved
        ↓
8. Ollama generates a grounded response
        ↓
9. Answer and source information are displayed
```

---

# 📊 Example Output

The application provides:

```text
Answer:
RAG stands for Retrieval-Augmented Generation.
It combines information retrieval with language generation
to provide answers based on external documents.

Mode:
Ollama LLM

Sources:
1. rag_overview.txt
   Similarity Score: 0.82

2. machine_learning.txt
   Similarity Score: 0.61
```

---

# 🎓 Applications

This project can be adapted for:

* 📚 Educational knowledge assistants
* 📑 Research paper assistants
* 🏢 Enterprise document search
* 📋 Policy/document analysis
* 👨‍💻 Technical documentation assistants
* 🧑‍🎓 Student study assistants
* 📖 Personal knowledge bases
* 🏥 Domain-specific information systems
* ⚖️ Legal document search
* 💼 Business knowledge management

---

# 🔐 Privacy Advantage

When Ollama is configured for local inference, the language model can run on the user's own machine.

This can be useful for applications where documents should remain within the local environment rather than being sent to an external AI API.

---

# ⚡ Advantages

* Uses user-provided documents as the knowledge source
* Supports multiple document formats
* Semantic rather than simple keyword retrieval
* Local LLM support
* No mandatory external AI API
* Automatic fallback mechanism
* Source information is displayed
* Easy to extend
* Simple Flask architecture
* Suitable for academic and prototype projects

---

# 🚀 Future Enhancements

Possible improvements include:

* [ ] Persistent vector database using FAISS, Chroma, or Qdrant
* [ ] Chat history and conversation memory
* [ ] Streaming LLM responses
* [ ] User authentication
* [ ] Multiple LLM provider support
* [ ] OCR for scanned documents
* [ ] PDF page-level citations
* [ ] Reranking models
* [ ] Conversation-aware retrieval
* [ ] Docker support
* [ ] Cloud deployment
* [ ] Admin document management
* [ ] Multi-user support
* [ ] Advanced analytics dashboard

---

# 🎥 Demo Video

A recommended demonstration should show:

1. Project introduction
2. System architecture
3. Starting the application
4. Uploading a document
5. Asking a question
6. Displaying the generated answer
7. Showing retrieved sources
8. Uploading another document
9. Asking a question about the new document
10. Demonstrating the Ollama/fallback mechanism

---

# 📸 Screenshots

For a professional GitHub repository, add screenshots such as:

```text
screenshots/
├── home.png
├── document-upload.png
├── question-answer.png
├── retrieved-sources.png
└── architecture.png
```

Then display them in this README:

```markdown
## 📸 Screenshots

### 🏠 Home Page
![Home Page](screenshots/home.png)

### 📄 Document Upload
![Document Upload](screenshots/document-upload.png)

### 🤖 AI Question Answering
![Question Answering](screenshots/question-answer.png)

### 📚 Retrieved Sources
![Retrieved Sources](screenshots/retrieved-sources.png)
```

---

# 🐙 GitHub Repository

Recommended repository name:

```text
RAG-Based-AI-Knowledge-Assistant
```

Suggested GitHub description:

> **A document-grounded AI knowledge assistant using RAG, Sentence Transformers, cosine similarity search, Flask, and Ollama.**

Suggested topics:

```text
python
artificial-intelligence
rag
retrieval-augmented-generation
llm
ollama
flask
nlp
machine-learning
sentence-transformers
vector-search
ai-assistant
document-qa
```

---

# 📜 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# 👩‍💻 Author

**Priyadharshini**

MCA Final Year Student

Interested in:

* Artificial Intelligence
* Machine Learning
* Generative AI
* Natural Language Processing
* Data Science
* Python Development

---

## ⭐ If You Find This Project Useful

Consider giving the repository a ⭐ **Star** on GitHub!

Feel free to fork the project, experiment with different documents and LLMs, and extend the RAG pipeline with your own features.
