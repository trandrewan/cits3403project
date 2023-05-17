<script>
const input = document.getElementById('input-field');

    input.addEventListener('keyup', function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.key === 'Enter' || event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            sendMessage();
        }
    });

async function sendMessage() {
    const input = document.getElementById('input-field');
    const chat = document.getElementById('chat');

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

    const data = await response.json();

    // Create API response message element
    const apiMessage = document.createElement('div');
    apiMessage.className = 'response-message';
    apiMessage.innerText = data.message;
    chat.appendChild(apiMessage);

    // Scroll to the bottom of the chat box
    chat.scrollTop = chat.scrollHeight;

    // Clear the input field
    input.value = '';
}
</script>