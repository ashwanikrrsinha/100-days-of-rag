import os
import google.generativeai as genai
from dotenv import load_dotenv  # <--- Import this

load_dotenv()  # <--- This reads the .env file
api_key = os.getenv("GEMINI_API_KEY") # <--- Get the key safely

os.environ["Gemini_API_Key"] = api_key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")