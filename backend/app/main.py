from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ChatRequest, ChatResponse
from app.services.ai_service import get_chat_response

app = FastAPI(title="Context-Aware ChatBot API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    print(f"--- Incoming Message: {request.message} ---")
    try:
        response_text = get_chat_response(request.message)
        print(f"--- AI Response Success ---")
        return ChatResponse(response=response_text)
    except Exception as e:
        print(f"--- ERROR IN CHAT ENDPOINT: {e} ---")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
