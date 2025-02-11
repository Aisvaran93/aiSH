function sendMessage() {
    let message = document.getElementById("messageInput").value.trim();
    let fileInput = document.getElementById("fileInput");
    let chatbox = document.getElementById("chatbox");

    if (message === "" && fileInput.files.length === 0) return;

    appendMessage("You", message || "[File Uploaded]", "user");

    let formData = new FormData();
    formData.append("message", message);
    if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
    }

    // Show typing indicator
    let typingIndicator = document.createElement("p");
    typingIndicator.classList.add("typing");
    typingIndicator.textContent = "AI is typing...";
    chatbox.appendChild(typingIndicator);
    chatbox.scrollTop = chatbox.scrollHeight;

    fetch("https://aish-jy9f.onrender.com/chat", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        chatbox.removeChild(typingIndicator); // Remove typing indicator

        if (data.response) {
            appendMessage("AI", data.response, "ai");
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
    fileInput.value = "";
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

// Dark Mode Toggle
document.getElementById("themeToggle").addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    this.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
});
