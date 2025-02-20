function sendMessage() {
    let message = document.getElementById("messageInput").value.trim();
    let chatbox = document.getElementById("chatbox");

    if (message === "") return;

    appendMessage("You", message, "user");

    let typingIndicator = document.createElement("p");
    typingIndicator.classList.add("typing");
    typingIndicator.textContent = "AI is typing...";
    chatbox.appendChild(typingIndicator);
    chatbox.scrollTop = chatbox.scrollHeight;

    fetch("https://aish-jy9f.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chatbox.removeChild(typingIndicator);
        if (data.choices && data.choices[0].message.content) {
            let reply = data.choices[0].message.content;
            appendMessage("AI", reply, "ai");
        } else {
            appendMessage("AI", "Error: Unexpected response format", "ai");
        }
    })
    .catch(error => {
        chatbox.removeChild(typingIndicator);
        appendMessage("AI", "Error: Unable to connect to AI server.", "ai");
        console.error("Error:", error);
    });

    document.getElementById("messageInput").value = "";
}

function appendMessage(sender, text, type) {
    let chatbox = document.getElementById("chatbox");
    let messageElement = document.createElement("div");
    messageElement.classList.add("message", type);
    messageElement.innerHTML = `<b>${sender}:</b> ${text}`;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function handleEnter(event) {
    if (event.key === "Enter") sendMessage();
}

document.getElementById("themeToggle").addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    this.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
});

document.getElementById("fileUpload").addEventListener("change", function(event) {
    let file = event.target.files[0];

    if (file) {
        let chatbox = document.getElementById("chatbox");
        appendMessage("You", `📎 Uploading: ${file.name}...`, "user");

        let formData = new FormData();
        formData.append("file", file);

        fetch("https://your-api-url/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("AI", `File received: ${data.file_url}`, "ai");
        })
        .catch(error => {
            appendMessage("AI", "Error: File upload failed.", "ai");
            console.error("Upload Error:", error);
        });
    }
});

