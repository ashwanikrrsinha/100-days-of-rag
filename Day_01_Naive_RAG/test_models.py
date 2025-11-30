import os
import google.generativeai as genai

# Setup API Key
os.environ["GEMINI_API_KEY"] = "AIzaSyBBUcBFEYKEG_4zzubpyQxCrlwRPkHJWtM" # Put your actual key here
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")