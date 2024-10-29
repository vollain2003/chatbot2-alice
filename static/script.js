document.getElementById('sendButton').addEventListener('click', async () => {
    const userInput = document.getElementById('userInput').value;
    appendMessage(`You: ${userInput}`);
    document.getElementById('userInput').value = '';

    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();
    appendMessage(`Bot: ${data.reply}`);
});

function appendMessage(message) {
    const chatbox = document.getElementById('chatbox');
    chatbox.innerHTML += `<div>${message}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;
}
