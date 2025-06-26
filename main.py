# On program start, load environment variables
# from .env file using dotenv library and reading
# API key
import sys
import os
from google import genai
from google.genai import types # used for roles
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions

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
        config=types.GenerateContentConfig(
            tools = [available_functions], system_instruction=system_prompt
        ),
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print("We are using Google Gemini AI.\n")

    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}\n")

    function_calls = response.function_calls #returns list[FunctionCall]
    if len(function_calls) > 0:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

    print(f"Google Gemini's response: {response.text}\n")

if __name__ == "__main__":
    sysCheck()
    main()