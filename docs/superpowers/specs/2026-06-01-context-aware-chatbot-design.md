# Design Document: Context-Aware Web Chatbot (Phase 1)

**Date:** 2026-06-01
**Status:** Draft
**Author:** Gemini CLI

## 1. Project Overview
The goal of this project is to build an industry-standard, full-stack web application that demonstrates conversational memory using the Google Gemini AI. This project serves as a foundational step for an aspiring AI Engineer, focusing on clean architecture, secure API handling, and modern UI frameworks.

## 2. Success Criteria
- **Conversational Memory:** The AI must remember previous parts of the conversation.
- **Industry Standard UI:** A clean, responsive chat interface built with React and Tailwind CSS.
- **Secure Backend:** API keys are never exposed to the frontend; all AI logic happens on a FastAPI server.
- **Deployable:** The app must be ready for hosting on free tiers (Vercel/Render).

## 3. Tech Stack
- **Frontend:** React (Vite), Tailwind CSS, Lucide React (Icons).
- **Backend:** Python, FastAPI, Uvicorn (Server), `google-generativeai` SDK.
- **Environment Management:** `python-dotenv` for backend secrets.
- **Communication:** REST API (JSON).

## 4. Architecture & Data Flow
The project follows a monorepo structure with strict separation of concerns.

### Data Flow Loop:
1. **User Input:** User types a message in the React frontend.
2. **Request:** Frontend sends a POST request with the message to the FastAPI `/chat` endpoint.
3. **AI Processing:**
   - FastAPI retrieves the session's conversation history.
   - It appends the new message and sends the full context to the Gemini API.
   - It receives the AI response.
4. **Response:** FastAPI saves the AI response to the history and sends it back to the frontend.
5. **Update:** Frontend updates the UI to display the AI's message.

## 5. File Structure
```text
CHATBOT/
├── backend/
│   ├── app/
│   │   ├── main.py         # Routes and CORS config
│   │   ├── models.py       # Pydantic request/response schemas
│   │   └── services/
│   │       └── ai_service.py # Gemini SDK integration & history management
│   ├── .env                # GOOGLE_API_KEY (Excluded from Git)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # ChatWindow, Message, InputArea
│   │   ├── App.jsx         # State management and API calls
│   │   └── index.css       # Tailwind directives
│   ├── tailwind.config.js
│   └── package.json
└── docs/
    └── superpowers/specs/  # Design documents
```

## 6. Memory Management (Phase 1)
- **Strategy:** Server-side in-memory storage.
- **Implementation:** A Python dictionary/list in `ai_service.py` that stores messages for the current session.
- **Future Scale:** This will be replaced by a database (PostgreSQL/Redis) in Phase 2.

## 7. Security
- API keys will be stored in `.env` on the backend.
- The `.gitignore` will ensure secrets are never committed to GitHub.
- Frontend will communicate only with our backend, never directly with Gemini.

## 8. Deployment Plan
- **Frontend:** Vercel (Auto-deploys from `frontend/` folder).
- **Backend:** Render (Auto-deploys from `backend/` folder).
- **Free Tier Strategy:** Use Render's free "Web Service" tier and Vercel's hobby tier.
