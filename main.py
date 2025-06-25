# On program start, load environment variables
# from .env file using dotenv library and reading
# API key
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types # used for roles

# Variables
user_prompt = None

def sysCheck():
    if len(sys.argv) < 2:
        print('Usage: python3 main.py "Prompt to give Google Gemini"')
        sys.exit(1)

    global user_prompt 
    user_prompt = sys.argv[1]

def main():
    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)],)
        ]
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key) # create new instance of Gemini client
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print("We are using Google Gemini AI.\n")

    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}\n")

    print(f"Google Gemini's response: {response.text}\n")

sysCheck()
main()