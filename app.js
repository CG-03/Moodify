document.getElementById("sendBtn").addEventListener("click", async function () {
    const userInput = document.getElementById("userInput").value;
    const chatBox = document.getElementById("chatBox");

    if (!userInput) return;

    // Display user message in chat
    chatBox.innerHTML += `<div class="user-message">${userInput}</div>`;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userInput }),
        });

        const data = await response.json();
        if (data.response) {
            // Display bot response in chat
            chatBox.innerHTML += `<div class="bot-response">${data.response}</div>`;
        } else {
            chatBox.innerHTML += `<div class="error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        console.error("Error:", error);
        chatBox.innerHTML += `<div class="error">An error occurred while communicating with the server.</div>`;
    }

    // Clear user input
    document.getElementById("userInput").value = "";
});
