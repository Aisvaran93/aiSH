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

        console.log("Response:", data); // Debugging: Print full response

        if (data.response) {
            appendMessage("AI", data.response, "ai");
        } else if (data.choices && data.choices[0].message.content) {
            appendMessage("AI", data.choices[0].message.content, "ai");
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
