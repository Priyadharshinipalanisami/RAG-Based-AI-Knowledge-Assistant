import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from rag.document_loader import load_document
from rag.chunker import chunk_text
from rag.vector_store import VectorStore
from rag.generator import generate_answer

app = Flask(__name__)
UPLOAD_FOLDER = "documents"
ALLOWED_EXTENSIONS = {"txt", "md", "pdf", "docx"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

vector_store = VectorStore()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def rebuild_index():
    vector_store.clear()
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.isfile(path) or not allowed_file(filename):
            continue
        try:
            text = load_document(path)
            chunks = chunk_text(text, chunk_size=900, overlap=150)
            vector_store.add_documents(chunks, {"source": filename})
        except Exception as exc:
            print(f"[WARNING] Could not index {filename}: {exc}")

rebuild_index()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/documents")
def documents():
    names = sorted(
        f for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f)) and allowed_file(f)
    )
    return jsonify({"documents": names, "chunks": len(vector_store.documents)})

@app.route("/api/upload", methods=["POST"])
def upload():
    uploaded = []
    errors = []

    for file in request.files.getlist("files"):
        if not file or not file.filename:
            continue
        if not allowed_file(file.filename):
            errors.append(f"{file.filename}: unsupported file type")
            continue

        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        uploaded.append(filename)

    rebuild_index()
    return jsonify({
        "success": True,
        "uploaded": uploaded,
        "errors": errors,
        "chunks": len(vector_store.documents)
    })

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({"success": False, "error": "Please enter a question."}), 400

    results = vector_store.search(question, top_k=5)
    answer, mode = generate_answer(question, results)

    sources = [
        {
            "source": r["metadata"].get("source", "Unknown"),
            "score": round(r["score"], 4),
            "preview": r["text"][:220]
        }
        for r in results
    ]

    return jsonify({
        "success": True,
        "answer": answer,
        "mode": mode,
        "sources": sources
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
