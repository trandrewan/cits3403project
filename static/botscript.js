async function sendMessage() {
    const input = document.getElementById('input-field');  // Corrected ID
    const chat = document.getElementById('chat-window');   // Corrected ID
    
    // Create user message element
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.innerText = input.value;
    chat.appendChild(userMessage);

    // Send POST request to Flask API
    const response = await fetch('/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: input.value })
    });

    const data = await response.text();
    
    // Create API response message element
    const apiMessage = document.createElement('div');
    apiMessage.className = 'response-message';
    apiMessage.innerText = data;
    chat.appendChild(apiMessage);

    // Scroll to the bottom of the chat box
    chat.scrollTop = chat.scrollHeight;

    // Clear the input field
    input.value = '';
}
