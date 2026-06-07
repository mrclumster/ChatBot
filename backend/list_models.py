import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "your_api_key_here":
    print("Error: Please add your real API key to the .env file.")
else:
    genai.configure(api_key=api_key)
    print("Listing models you have access to:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error: {e}")
