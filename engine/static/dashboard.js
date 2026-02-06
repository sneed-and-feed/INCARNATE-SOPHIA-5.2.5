// Global Error Catcher
window.addEventListener('error', function (event) {
    alert("Sovereign Dashboard Crash: " + event.message + "\nAt: " + event.filename + ":" + event.lineno);
});

const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const lambdaDisp = document.getElementById('stat-lambda');
const coherenceDisp = document.getElementById('stat-coherence');

console.log("[BRIDGE] Sovereign Dashboard Logic Initialized.");

// --- CHAT LOGIC ---

async function sendMessage(text) {
    if (!text || !text.trim()) return;

    console.log("[BRIDGE] Transmitting:", text);

    // Append user message
    appendMessage('user', text);
    userInput.value = '';

    try {
        const response = await fetch('/v1/chat/completions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'sophia-sovereign-5.2',
                messages: [{ role: 'user', content: text }],
                no_stream: true
            })
        });

        if (!response.ok) throw new Error("Server Resonance Failure: " + response.status);

        const data = await response.json();
        const reply = data.choices[0].message.content;

        appendMessage('assistant', reply);
    } catch (err) {
        console.error("Transmission failed:", err);
        appendMessage('assistant', `[ERROR] Failed to communicate with Soul: ${err.message}`);
    }
}

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;

    const header = document.createElement('div');
    header.className = 'message-header';
    header.textContent = role === 'user' ? 'User // Signal' : 'Sophia // Merging';

    const content = document.createElement('div');
    if (text.includes('[TOOL_OUTPUT')) {
        content.innerHTML = formatComplexResponse(text);
    } else {
        content.textContent = text;
    }

    msgDiv.appendChild(header);
    msgDiv.appendChild(content);
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function formatComplexResponse(text) {
    return text.replace(/\n/g, '<br>').replace(/\[TOOL_OUTPUT: (.*?)\]/g, '<strong>[$1 Result]</strong>');
}

// --- SYSTEM UPDATES ---

async function updateStats() {
    try {
        // Mocking slight movement for vibe
        if (lambdaDisp) {
            const val = parseFloat(lambdaDisp.textContent) || 20.64;
            lambdaDisp.textContent = (val + (Math.random() * 0.02 - 0.01)).toFixed(2);
        }
        if (coherenceDisp) {
            const val = parseFloat(coherenceDisp.textContent) || 0.9984;
            coherenceDisp.textContent = (val + (Math.random() * 0.0002 - 0.0001)).toFixed(4);
        }
    } catch (err) { }
}

// Export to window for onclick handlers in HTML
window.sendAction = function (cmd) {
    console.log("[BRIDGE] Action Triggered:", cmd);
    if (userInput) {
        userInput.value = cmd;
        sendMessage(cmd);
    }
};

// --- EVENT LISTENERS ---

if (sendBtn) {
    sendBtn.addEventListener('click', () => {
        console.log("[BRIDGE] Transmit button clicked");
        if (userInput) sendMessage(userInput.value);
    });
}

if (userInput) {
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            console.log("[BRIDGE] Enter key pressed");
            sendMessage(userInput.value);
        }
    });
}

// Initial stats update
setInterval(updateStats, 5000);

// Initial Gateway Sync
async function syncGateway() {
    try {
        const res = await fetch('/gateway/status');
        const data = await res.json();
        const btn = document.getElementById('gate-toggle');
        const status = document.getElementById('gateway-status');

        if (data.active) {
            if (status) {
                status.textContent = 'ONLINE';
                status.className = 'status-pill online';
            }
            if (btn) {
                btn.textContent = 'STOP GATEWAY';
                btn.style.background = 'rgba(255,0,0,0.1)';
                btn.style.color = '#ff3333';
            }
        } else {
            if (status) {
                status.textContent = 'OFFLINE';
                status.className = 'status-pill offline';
            }
            if (btn) {
                btn.textContent = 'START GATEWAY';
                btn.style.background = 'rgba(0,255,0,0.1)';
                btn.style.color = '#33ff33';
            }
        }
    } catch (err) {
        console.error("Gateway sync failed");
    }
}
syncGateway();

// Toggle Gateway
const gateToggle = document.getElementById('gate-toggle');
if (gateToggle) {
    gateToggle.addEventListener('click', async () => {
        const btn = document.getElementById('gate-toggle');
        const status = document.getElementById('gateway-status');

        try {
            const res = await fetch('/gateway/toggle', { method: 'POST' });
            const data = await res.json();

            if (data.active) {
                status.textContent = 'ONLINE';
                status.className = 'status-pill online';
                btn.textContent = 'STOP GATEWAY';
                btn.style.background = 'rgba(255,0,0,0.1)';
                btn.style.color = '#ff3333';
            } else {
                status.textContent = 'OFFLINE';
                status.className = 'status-pill offline';
                btn.textContent = 'START GATEWAY';
                btn.style.background = 'rgba(0,255,0,0.1)';
                btn.style.color = '#33ff33';
            }
        } catch (err) {
            alert("Control link severed: Bridge not responding to Gateway toggles.");
        }
    });
}
