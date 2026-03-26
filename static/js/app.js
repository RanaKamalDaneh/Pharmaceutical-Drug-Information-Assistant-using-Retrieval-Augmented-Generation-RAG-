
document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const loadingIndicator = document.getElementById('loading-indicator');

    const addMessage = (text, isUser = false) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        // Basic detection for Arabic to apply RTL
        const isArabic = /[\u0600-\u06FF]/.test(text);
        if (isArabic) {
            msgDiv.setAttribute('dir', 'rtl');
        }

        // Convert line breaks to <br> and handle simple markdown-like formatting
        let formattedText = text.replace(/\n/g, '<br>');
        
        // Simple bold formatting for headings
        formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        msgDiv.innerHTML = `<p>${formattedText}</p>`;
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    const handleSend = async () => {
        const query = userInput.value.trim();
        if (!query) return;

        addMessage(query, true);
        userInput.value = '';
        
        // Show loading
        loadingIndicator.style.display = 'block';
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            const data = await response.json();
            
            if (data.success) {
                addMessage(data.answer);
            } else {
                addMessage("Sorry, I encountered an error while processing your request.", false);
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage("Unable to connect to the server. Please check if the backend is running.", false);
        } finally {
            loadingIndicator.style.display = 'none';
        }
    };

    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
});
