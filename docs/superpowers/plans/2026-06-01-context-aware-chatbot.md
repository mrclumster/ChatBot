# Context-Aware Web Chatbot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full-stack, industry-standard chatbot using FastAPI and React that maintains conversational memory via the Google Gemini API.

**Architecture:** Monorepo with a FastAPI backend and a React (Vite) frontend. Backend manages AI logic and session memory; frontend handles the interactive UI using Tailwind CSS.

**Tech Stack:** Python (FastAPI, Google GenAI SDK), JavaScript (React, Vite, Tailwind CSS, Lucide React).

---

### Task 1: Backend Scaffolding & Dependencies

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/.env`
- Create: `backend/.gitignore`

- [ ] **Step 1: Create the requirements file**
```text
fastapi
uvicorn
google-generativeai
python-dotenv
pydantic
```

- [ ] **Step 2: Create the .env file (Template)**
```text
GOOGLE_API_KEY=your_api_key_here
```

- [ ] **Step 3: Create backend .gitignore**
```text
.env
__pycache__/
*.pyc
venv/
```

- [ ] **Step 4: Install dependencies**
Run: `cd backend && python -m venv venv && ./venv/Scripts/activate && pip install -r requirements.txt` (Note: Adjust for OS if needed)

---

### Task 2: Backend AI Service & Models

**Files:**
- Create: `backend/app/models.py`
- Create: `backend/app/services/ai_service.py`

- [ ] **Step 1: Define Pydantic Models**
```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
```

- [ ] **Step 2: Implement Gemini Service with Memory**
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# In-memory history for Phase 1
chat_history = []

def get_chat_response(user_input: str):
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=chat_history)
    
    response = chat.send_message(user_input)
    
    # Update global history (simplified for Phase 1)
    global chat_history
    chat_history = chat.history
    
    return response.text
```

---

### Task 3: Backend API Routes

**Files:**
- Create: `backend/app/main.py`

- [ ] **Step 1: Create FastAPI app with CORS**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ChatRequest, ChatResponse
from app.services.ai_service import get_chat_response

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response_text = get_chat_response(request.message)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

### Task 4: Frontend Scaffolding (Vite + Tailwind)

**Files:**
- Modify: `frontend/package.json` (via Vite init)
- Create: `frontend/tailwind.config.js`
- Create: `frontend/src/index.css`

- [ ] **Step 1: Initialize Vite Project**
Run: `npm create vite@latest frontend -- --template react`

- [ ] **Step 2: Install Tailwind CSS**
Run: `cd frontend && npm install -D tailwindcss postcss autoprefixer && npx tailwindcss init -p`

- [ ] **Step 3: Configure Tailwind**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

- [ ] **Step 4: Add Tailwind directives to index.css**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-slate-900 text-slate-100;
}
```

---

### Task 5: Frontend UI Components

**Files:**
- Create: `frontend/src/components/ChatWindow.jsx`
- Create: `frontend/src/components/ChatMessage.jsx`
- Create: `frontend/src/components/InputArea.jsx`

- [ ] **Step 1: Create ChatMessage Component**
```jsx
export default function ChatMessage({ message, isUser }) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] p-3 rounded-lg ${isUser ? 'bg-blue-600' : 'bg-slate-700'}`}>
        <p className="text-sm">{message}</p>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create InputArea Component**
```jsx
import { useState } from 'react';
import { Send } from 'lucide-react';

export default function InputArea({ onSendMessage, isLoading }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border-t border-slate-700 flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
        className="flex-1 bg-slate-800 border border-slate-700 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button 
        type="submit" 
        disabled={isLoading}
        className="bg-blue-600 p-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        <Send size={20} />
      </button>
    </form>
  );
}
```

---

### Task 6: Frontend Integration & App Logic

**Files:**
- Modify: `frontend/src/App.jsx`

- [ ] **Step 1: Implement Main App Logic**
```jsx
import { useState } from 'react';
import ChatMessage from './components/ChatMessage';
import InputArea from './components/InputArea';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (text) => {
    const userMessage = { text, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const data = await response.json();
      setMessages(prev => [...prev, { text: data.response, isUser: false }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { text: 'Error connecting to server.', isUser: false }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto border-x border-slate-700">
      <header className="p-4 border-b border-slate-700 text-center">
        <h1 className="text-xl font-bold">Context-Aware AI</h1>
      </header>
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg.text} isUser={msg.isUser} />
        ))}
        {isLoading && <div className="text-slate-500 text-sm italic">AI is thinking...</div>}
      </div>
      <InputArea onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}

export default App;
```
