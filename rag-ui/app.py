from flask import Flask, render_template_string, request, jsonify, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

API_BASE_URL = "http://rag-api:8001"

CHAT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Terminal</title>
    <link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        body {
            font-family: 'Source Code Pro', monospace;
            background: #000000;
            color: #00ff00;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        /* Matrix Rain Effect */
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            opacity: 0.1;
        }

        .matrix-column {
            position: absolute;
            top: -100px;
            font-size: 14px;
            line-height: 1.2;
            color: #00ff00;
            animation: matrix-fall linear infinite;
            text-shadow: 0 0 3px #00ff00;
        }

        @keyframes matrix-fall {
            0% { transform: translateY(-100vh); opacity: 1; }
            100% { transform: translateY(100vh); opacity: 0; }
        }

        /* Main Interface */
        .container {
            position: relative;
            z-index: 10;
            width: 90%;
            max-width: 1000px;
            margin: 20px auto;
            background: rgba(0, 20, 0, 0.95);
            border: 2px solid #00ff00;
            border-radius: 10px;
            box-shadow: 
                0 0 20px #00ff00,
                inset 0 0 20px rgba(0, 255, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .header {
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 100, 0, 0.3));
            color: #00ff00;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }

        .header h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
            animation: glow-pulse 2s infinite;
        }

        .header p {
            font-size: 0.9rem;
            opacity: 0.8;
        }

        @keyframes glow-pulse {
            0%, 100% { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
            50% { text-shadow: 0 0 15px #00ff00, 0 0 30px #00ff00, 0 0 40px #00ff00; }
        }

        .project-selector {
            padding: 20px;
            background: rgba(0, 30, 0, 0.7);
            border-bottom: 1px solid #004400;
        }

        .chat-container {
            height: 450px;
            overflow-y: auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.8);
            scrollbar-width: thin;
            scrollbar-color: #00ff00 #001100;
        }

        .chat-container::-webkit-scrollbar {
            width: 8px;
        }

        .chat-container::-webkit-scrollbar-track {
            background: #001100;
        }

        .chat-container::-webkit-scrollbar-thumb {
            background: #00ff00;
            border-radius: 4px;
            box-shadow: 0 0 5px #00ff00;
        }

        .message {
            margin: 15px 0;
            padding: 12px 18px;
            border-radius: 8px;
            max-width: 85%;
            position: relative;
            animation: message-appear 0.3s ease-out;
        }

        @keyframes message-appear {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .user-message {
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 150, 0, 0.3));
            border: 1px solid #00ff00;
            margin-left: auto;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
            text-shadow: 0 0 3px #00ff00;
        }

        .bot-message {
            background: linear-gradient(135deg, rgba(0, 100, 0, 0.15), rgba(0, 50, 0, 0.25));
            border: 1px solid #004400;
            color: #00cc00;
            box-shadow: 0 0 8px rgba(0, 255, 0, 0.2);
        }

        .input-container {
            padding: 20px;
            border-top: 1px solid #004400;
            background: rgba(0, 20, 0, 0.9);
        }

        .input-group {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        input, select, button {
            padding: 12px 15px;
            border: 2px solid #00ff00;
            border-radius: 6px;
            font-size: 14px;
            font-family: 'Source Code Pro', monospace;
            background: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            transition: all 0.3s ease;
        }

        input[type="text"] {
            flex: 1;
            box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.1);
        }

        input[type="text"]:focus {
            outline: none;
            box-shadow: 
                inset 0 0 10px rgba(0, 255, 0, 0.2),
                0 0 15px rgba(0, 255, 0, 0.5);
            text-shadow: 0 0 3px #00ff00;
        }

        button {
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 150, 0, 0.3));
            color: #00ff00;
            border: 2px solid #00ff00;
            cursor: pointer;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        button:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.3), transparent);
            transition: left 0.5s;
        }

        button:hover:before {
            left: 100%;
        }

        button:hover {
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
            text-shadow: 0 0 5px #00ff00;
            transform: translateY(-2px);
        }

        button:disabled {
            background: rgba(50, 50, 50, 0.3);
            color: #666;
            border-color: #333;
            cursor: not-allowed;
            box-shadow: none;
            transform: none;
        }

        .loading {
            text-align: center;
            color: #00ff00;
            font-style: italic;
            animation: loading-dots 1.5s infinite;
        }

        @keyframes loading-dots {
            0%, 20% { opacity: 0.2; }
            50% { opacity: 1; }
            80%, 100% { opacity: 0.2; }
        }

        .error {
            color: #ff4444;
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(150, 0, 0, 0.2));
            border: 1px solid #ff4444;
            padding: 12px;
            border-radius: 6px;
            margin: 10px 0;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
            text-shadow: 0 0 3px #ff4444;
        }

        .project-info {
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.15), rgba(0, 200, 0, 0.25));
            color: #00ff00;
            padding: 12px;
            border-radius: 6px;
            margin: 10px 0;
            border: 1px solid #00aa00;
            box-shadow: 0 0 8px rgba(0, 255, 0, 0.2);
            text-shadow: 0 0 2px #00ff00;
        }

        .terminal-prompt {
            color: #00ff00;
            font-weight: bold;
        }

        .terminal-prompt:before {
            content: '> ';
            color: #00ff00;
            font-weight: bold;
        }

        /* Glitch effect for loading */
        .glitch {
            animation: glitch 0.3s infinite;
        }

        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .container { width: 95%; margin: 10px auto; }
            .header h1 { font-size: 1.5rem; }
            .chat-container { height: 350px; }
            .input-group { flex-direction: column; }
            input[type="text"], button { width: 100%; }
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <h1> AI TERMINAL</h1>
            <p class="terminal-prompt">Initialize neural link and select target project...</p>
        </div>
        
        <div class="project-selector">
            <div class="input-group">
                <input type="text" id="projectName" placeholder="[ENTER PROJECT DESIGNATION]..." 
                       value="{{ session.get('current_project', '') }}">
                <button onclick="setProject()">INITIALIZE</button>
                <button onclick="clearProject()">TERMINATE</button>
            </div>
            <div id="projectInfo"></div>
        </div>
        
        <div class="chat-container" id="chatContainer">
            {% if session.get('current_project') %}
                <div class="project-info">
                    <span class="terminal-prompt">ACTIVE PROJECT: <strong>{{ session.get('current_project') }}</strong></span>
                    <br>NEURAL LINK ESTABLISHED - READY FOR QUERIES
                </div>
            {% else %}
                <div class="project-info">
                    <span class="terminal-prompt">SYSTEM STATUS: STANDBY</span>
                    <br>Please initialize a project to begin neural interface...
                </div>
            {% endif %}
        </div>
        
        <div class="input-container">
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="[ENTER QUERY TO NEURAL NETWORK]..." 
                       onkeypress="if(event.key==='Enter') sendMessage()" 
                       {% if not session.get('current_project') %}disabled{% endif %}>
                <button onclick="sendMessage()" id="sendBtn" 
                        {% if not session.get('current_project') %}disabled{% endif %}>
                    TRANSMIT
                </button>
            </div>
        </div>
    </div>

    <script>
        let isLoading = false;
        
        // Matrix Rain Effect
        function createMatrixRain() {
            const matrixBg = document.getElementById('matrixBg');
            const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
            const columns = Math.floor(window.innerWidth / 20);
            
            for (let i = 0; i < columns; i++) {
                const column = document.createElement('div');
                column.className = 'matrix-column';
                column.style.left = i * 20 + 'px';
                column.style.animationDuration = (Math.random() * 3 + 2) + 's';
                column.style.animationDelay = Math.random() * 2 + 's';
                
                let columnText = '';
                for (let j = 0; j < 20; j++) {
                    columnText += chars[Math.floor(Math.random() * chars.length)] + '<br>';
                }
                column.innerHTML = columnText;
                
                matrixBg.appendChild(column);
                
                // Remove and recreate columns periodically
                setTimeout(() => {
                    if (column.parentNode) {
                        column.parentNode.removeChild(column);
                    }
                }, (Math.random() * 3 + 2) * 1000);
            }
        }
        
        // Initialize matrix effect
        createMatrixRain();
        setInterval(createMatrixRain, 5000);
        
        function setProject() {
            const projectName = document.getElementById('projectName').value.trim();
            if (!projectName) {
                showError('PROJECT DESIGNATION REQUIRED');
                return;
            }
            
            showSystemMessage('INITIALIZING NEURAL LINK...');
            
            fetch('/set_project', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({project: projectName})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('projectInfo').innerHTML = 
                        `<div class="project-info">✓ NEURAL LINK ESTABLISHED WITH "${projectName}"<br>STATUS: OPERATIONAL</div>`;
                    document.getElementById('messageInput').disabled = false;
                    document.getElementById('sendBtn').disabled = false;
                    
                    // Clear chat and show project info
                    const chatContainer = document.getElementById('chatContainer');
                    chatContainer.innerHTML = `
                        <div class="project-info">
                            <span class="terminal-prompt">ACTIVE PROJECT: <strong>${projectName}</strong></span><br>
                            NEURAL INTERFACE READY - AWAITING INSTRUCTIONS
                        </div>
                    `;
                    
                    // Focus on input
                    document.getElementById('messageInput').focus();
                } else {
                    document.getElementById('projectInfo').innerHTML = 
                        `<div class="error">⚠ CONNECTION FAILED: ${data.error}</div>`;
                }
            })
            .catch(error => {
                document.getElementById('projectInfo').innerHTML = 
                    `<div class="error">⚠ SYSTEM ERROR: ${error.message}</div>`;
            });
        }
        
        function clearProject() {
            showSystemMessage('TERMINATING NEURAL LINK...');
            
            fetch('/clear_project', {method: 'POST'})
            .then(() => {
                document.getElementById('projectName').value = '';
                document.getElementById('projectInfo').innerHTML = 
                    '<div class="project-info"><span class="terminal-prompt">NEURAL LINK TERMINATED</span><br>SYSTEM STATUS: STANDBY</div>';
                document.getElementById('messageInput').disabled = true;
                document.getElementById('sendBtn').disabled = true;
                document.getElementById('chatContainer').innerHTML = 
                    '<div class="project-info"><span class="terminal-prompt">SYSTEM STATUS: STANDBY</span><br>Please initialize a project to begin neural interface...</div>';
                document.getElementById('messageInput').value = '';
            });
        }
        
        function sendMessage() {
            if (isLoading) return;
            
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessageToChat(`> ${message}`, 'user');
            messageInput.value = '';
            
            // Show loading
            isLoading = true;
            const loadingDiv = addMessageToChat('NEURAL NETWORK PROCESSING...', 'bot', true);
            document.getElementById('sendBtn').disabled = true;
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: message})
            })
            .then(response => response.json())
            .then(data => {
                // Remove loading message
                loadingDiv.remove();
                
                if (data.success) {
                    addMessageToChat(`SYSTEM: ${data.response}`, 'bot');
                } else {
                    addMessageToChat(`ERROR: ${data.error}`, 'bot');
                }
            })
            .catch(error => {
                loadingDiv.remove();
                addMessageToChat(`[CRITICAL ERROR] ${error.message}`, 'bot');
            })
            .finally(() => {
                isLoading = false;
                document.getElementById('sendBtn').disabled = false;
            });
        }
        
        function addMessageToChat(message, type, isLoading = false) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message ${isLoading ? 'loading glitch' : ''}`;
            messageDiv.textContent = message;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            return messageDiv;
        }
        
        function showSystemMessage(message) {
            const infoDiv = document.getElementById('projectInfo');
            infoDiv.innerHTML = `<div class="project-info">${message}</div>`;
        }
        
        function showError(message) {
            const infoDiv = document.getElementById('projectInfo');
            infoDiv.innerHTML = `<div class="error">${message}</div>`;
        }
        
        // Focus management
        {% if session.get('current_project') %}
        document.getElementById('messageInput').focus();
        {% else %}
        document.getElementById('projectName').focus();
        {% endif %}
        
        // Handle window resize for matrix effect
        window.addEventListener('resize', () => {
            document.getElementById('matrixBg').innerHTML = '';
            createMatrixRain();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(CHAT_TEMPLATE)

@app.route('/set_project', methods=['POST'])
def set_project():
    try:
        data = request.get_json()
        project_name = data.get('project', '').strip()
        
        if not project_name:
            return jsonify({'success': False, 'error': 'Project name is required'})
        
        test_url = f"{API_BASE_URL}/ask/{project_name}"
        test_data = {"query": "hello"}
        
        response = requests.post(test_url, json=test_data, timeout=5)
        
        if response.status_code == 200:
            session['current_project'] = project_name
            return jsonify({'success': True, 'project': project_name})
        else:
            return jsonify({
                'success': False, 
                'error': f'Project "{project_name}" not found or API error (Status: {response.status_code})'
            })
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False, 
            'error': f'Cannot connect to API server: {str(e)}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/clear_project', methods=['POST'])
def clear_project():
    session.pop('current_project', None)
    return jsonify({'success': True})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if 'current_project' not in session:
            return jsonify({'success': False, 'error': 'No project selected'})
        
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'})
        
        api_url = f"{API_BASE_URL}/ask/{session['current_project']}"
        api_data = {"query": query}
        
        response = requests.post(api_url, json=api_data, timeout=30)
        
        if response.status_code == 200:
            api_response = response.json()
            answer = api_response.get('answer', api_response.get('response', str(api_response)))
            return jsonify({'success': True, 'response': answer})
        else:
            return jsonify({
                'success': False, 
                'error': f'API error (Status: {response.status_code}): {response.text}'
            })
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False, 
            'error': f'API connection error: {str(e)}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
