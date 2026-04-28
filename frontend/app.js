const gameSpecEl = document.getElementById("game-spec");
const generateBtn = document.getElementById("generate-btn");
const statusPanel = document.getElementById("status-panel");
const statusLog = document.getElementById("status-log");
const filesPanel = document.getElementById("files-panel");
const fileTabs = document.getElementById("file-tabs");
const fileContent = document.getElementById("file-content");

let generatedFiles = {};

generateBtn.addEventListener("click", async () => {
    const gameSpec = gameSpecEl.value.trim();
    if (!gameSpec) return;

    // Reset UI
    generatedFiles = {};
    statusLog.innerHTML = "";
    fileTabs.innerHTML = "";
    fileContent.textContent = "";
    filesPanel.classList.add("hidden");
    statusPanel.classList.remove("hidden");
    generateBtn.disabled = true;

    try {
        const response = await fetch("/api/generate_files", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "game_spec": gameSpec }),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            // SSE events are separated by double newlines
            const parts = buffer.split("\n\n");
            // Last part may be incomplete — keep it in the buffer
            buffer = parts.pop();

            for (const part of parts) {
                handleSSEEvent(part);
            }
        }

        // Process any remaining buffer
        if (buffer.trim()) {
            handleSSEEvent(buffer);
        }

        addStatus("Done.");
    } catch (err) {
        addStatus(`Error: ${err.message}`);
    } finally {
        generateBtn.disabled = false;
    }
});

function handleSSEEvent(raw) {
    let eventType = "message";
    let data = "";

    for (const line of raw.split("\n")) {
        if (line.startsWith("event: ")) {
            eventType = line.slice(7);
        } else if (line.startsWith("data: ")) {
            data += line.slice(6);
        }
    }

    if (!data) return;

    if (eventType === "status") {
        addStatus(data);
    } else if (eventType === "status_done") {
        addStatus(data, "done");
    } else if (eventType === "file") {
        const parsed = JSON.parse(data);
        generatedFiles[parsed.name] = parsed.content;
        addStatus(`Generated ${parsed.name}`);
        showFiles();
    } else if (eventType === "error") {
        addStatus(`Error: ${data}`);
    }
}

function addStatus(message, className) {
    const li = document.createElement("li");
    if (className) li.classList.add(className);
    li.textContent = message;
    statusLog.appendChild(li);
    statusLog.scrollTop = statusLog.scrollHeight;
}

function showFiles() {
    const names = Object.keys(generatedFiles);
    if (names.length === 0) return;

    filesPanel.classList.remove("hidden");
    fileTabs.innerHTML = "";

    names.forEach((name, i) => {
        const btn = document.createElement("button");
        btn.textContent = name;
        if (i === 0) btn.classList.add("active");
        btn.addEventListener("click", () => selectFile(name));
        fileTabs.appendChild(btn);
    });

    fileContent.textContent = generatedFiles[names[0]];
}

function selectFile(name) {
    fileContent.textContent = generatedFiles[name];
    Array.from(fileTabs.children).forEach((btn) => {
        btn.classList.toggle("active", btn.textContent === name);
    });
}