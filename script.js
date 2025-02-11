function sendMessage() {
    let message = document.getElementById("messageInput").value;
    let chatbox = document.getElementById("chatbox");

    if (!message.trim()) {
        return; // Prevent sending empty messages
    }

    chatbox.innerHTML += `<p><b>You:</b> ${message}</p>`;

    fetch("https://aish-jy9f.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        console.log("Response received:", response); // Log the full response
        return response.json();
    })
    .then(data => {
        console.log("Response JSON:", data); // Log the JSON response

        // Check if API response has expected structure
        if (data.choices && data.choices.length > 0 && data.choices[0].message) {
            let reply = data.choices[0].message.content;
            chatbox.innerHTML += `<p><b>AI:</b> ${reply}</p>`;
        } else {
            chatbox.innerHTML += `<p><b>AI:</b> Error: Unexpected response format</p>`;
            console.error("Unexpected response format:", data);
        }

        chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to the latest message
    })
    .catch(error => {
        console.error("Fetch Error:", error);
        chatbox.innerHTML += `<p><b>AI:</b> Error: Failed to connect to AI</p>`;
    });

    document.getElementById("messageInput").value = ""; // Clear input field
}
