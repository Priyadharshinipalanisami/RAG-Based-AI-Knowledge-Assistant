const $ = id => document.getElementById(id);

function escapeHtml(value) {
    return value.replace(/[&<>"']/g, c => ({
        "&":"&amp;",
        "<":"&lt;",
        ">":"&gt;",
        '"':"&quot;",
        "'":"&#039;"
    }[c]));
}

async function loadDocuments() {
    const response = await fetch("/api/documents");
    const data = await response.json();

    $("documentList").innerHTML = data.documents.length
        ? data.documents.map(d =>
            `<li class="list-group-item px-0">📄 ${escapeHtml(d)}</li>`
          ).join("")
        : `<li class="list-group-item px-0 text-secondary">No documents.</li>`;
}

$("uploadBtn").addEventListener("click", async () => {
    const files = $("files").files;

    if (!files.length) {
        $("uploadStatus").innerHTML =
            `<span class="text-danger">Select a document first.</span>`;
        return;
    }

    const form = new FormData();
    [...files].forEach(file => form.append("files", file));

    $("uploadBtn").disabled = true;
    $("uploadStatus").textContent = "Uploading and creating embeddings...";

    try {
        const response = await fetch("/api/upload", {
            method: "POST",
            body: form
        });

        const data = await response.json();

        $("uploadStatus").innerHTML =
            `<span class="text-success">
                Indexed ${data.chunks} chunks successfully.
            </span>`;

        await loadDocuments();
    } catch (error) {
        $("uploadStatus").innerHTML =
            `<span class="text-danger">${escapeHtml(error.message)}</span>`;
    } finally {
        $("uploadBtn").disabled = false;
    }
});

$("askBtn").addEventListener("click", ask);

$("question").addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        ask();
    }
});

async function ask() {
    const question = $("question").value.trim();

    if (!question) {
        $("question").focus();
        return;
    }

    $("loading").classList.remove("d-none");
    $("answerBox").classList.add("d-none");
    $("sourcesBox").classList.add("d-none");
    $("askBtn").disabled = true;

    try {
        const response = await fetch("/api/ask", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({question})
        });

        const data = await response.json();

        if (!data.success) throw new Error(data.error);

        $("answer").textContent = data.answer;
        $("mode").textContent = data.mode;
        $("answerBox").classList.remove("d-none");

        $("sources").innerHTML = data.sources.map(source => `
            <div class="source">
                <strong>📄 ${escapeHtml(source.source)}</strong>
                <div class="score">Similarity: ${source.score}</div>
                <div class="small mt-1">${escapeHtml(source.preview)}...</div>
            </div>
        `).join("");

        $("sourcesBox").classList.remove("d-none");
    } catch (error) {
        $("answer").textContent = "Error: " + error.message;
        $("mode").textContent = "Error";
        $("answerBox").classList.remove("d-none");
    } finally {
        $("loading").classList.add("d-none");
        $("askBtn").disabled = false;
    }
}

loadDocuments();
