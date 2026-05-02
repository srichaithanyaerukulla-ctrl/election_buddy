// Configuration
const API_URL = "http://localhost:8000"; 

// State management
let chatHistory = [];

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const typingIndicator = document.getElementById('typing-indicator');

// Functions
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message to UI
    appendMessage('user', message);
    userInput.value = '';
    
    // Show typing indicator
    typingIndicator.style.display = 'block';
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, history: chatHistory })
        });

        const data = await response.json();
        
        // Hide typing indicator
        typingIndicator.style.display = 'none';

        // Add bot message to UI
        appendMessage('bot', data.response);
        
        // Log to backend
        logInteraction(message, data.response);
        
    } catch (error) {
        console.error('Error:', error);
        typingIndicator.style.display = 'none';
        appendMessage('bot', "I'm having trouble connecting to my servers. Please try again or call the Helpline at 1950.");
    }
}

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}-message`;
    msgDiv.innerHTML = formatText(text);
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatText(text) {
    // Simple markdown-like formatting
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/\*(.*?)\*/g, '<i>$1</i>');
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function suggestQuery(query) {
    userInput.value = query;
    sendMessage();
}

async function logInteraction(query, response) {
    try {
        await fetch(`${API_URL}/log`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_query: query,
                bot_response: response,
                timestamp: new IndianDate().toISOString()
            })
        });
    } catch (e) {
        console.log("Logging skipped (local/error)");
    }
}

// UI Section Toggles
function toggleSection(sectionId) {
    const views = ['timeline', 'checklist', 'crowd'];
    views.forEach(v => {
        document.getElementById(`${v}-view`).style.display = v === sectionId ? 'block' : 'none';
    });

    if (sectionId === 'crowd') {
        fetchCrowdData();
    }
}

async function fetchCrowdData() {
    const boothList = document.getElementById('booth-list');
    boothList.innerHTML = '<p>Updating live status...</p>';
    
    try {
        const response = await fetch(`${API_URL}/crowd`);
        const data = await response.json();
        
        boothList.innerHTML = data.booths.map(booth => `
            <div style="background: rgba(255,255,255,0.05); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid ${getStatusColor(booth.status)}">
                <strong>${booth.name}</strong>
                <div style="font-size: 0.8rem; color: var(--text-muted)">
                    Status: ${booth.status} | Wait: ${booth.wait_time}
                </div>
            </div>
        `).join('');
    } catch (e) {
        boothList.innerHTML = '<p>Unable to load booth data.</p>';
    }
}

function getStatusColor(status) {
    switch(status.toLowerCase()) {
        case 'low': return '#138808';
        case 'medium': return '#FF9933';
        case 'high': return '#ff3333';
        default: return '#ccc';
    }
}

class IndianDate extends Date {
    constructor() {
        super();
    }
    toISOString() {
        return this.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
    }
}
