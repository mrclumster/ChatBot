import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# In-memory history for Phase 1
# This stores the chat history objects from the SDK
chat_session = None

def get_chat_response(user_input: str):
    global chat_session
    
    # Initialize session if it doesn't exist
    if chat_session is None:
        model_name = 'gemini-3.5-flash'
        print(f"Initializing Gemini with model: {model_name}")
        model = genai.GenerativeModel(model_name)
        chat_session = model.start_chat(history=[])
    
    # Send message and get response
    response = chat_session.send_message(user_input)
    
    return response.text
