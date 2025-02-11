function sendMessage() {
    let message = document.getElementById("messageInput").value;
    let chatbox = document.getElementById("chatbox");

    chatbox.innerHTML += `<p><b>You:</b> ${message}</p>`;

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        let reply = data.choices[0].message.content;
        chatbox.innerHTML += `<p><b>AI:</b> ${reply}</p>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
    
    document.getElementById("messageInput").value = ""; // Clear input
}
