# On program start, load environment variables
# from .env file using dotenv library and reading
# API key
import sys
import os
from google import genai
from google.genai import types # used for roles
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function

# global variables
counter = 0

# main
def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    sysCheck(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key) # create new instance of Gemini client

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ]
    
    while counter < 20:
        generate_content(client, messages, verbose)
        print(f"We are at counter number: {counter}")

# checks proper formatting of system arguments for code execution
def sysCheck(args):
    if not args:
        print("We are using Google Gemini AI Code Assistant.\n")
        print('Usage: python3 main.py "Your prompt here" [--verbose]\n')
        print('Example: python3 main.py "How do I fix the calculator?"')
        sys.exit(1)

# handles generation of content, handle user prompt
def generate_content(client, messages, verbose):
    global counter

    # sets roles, passes user's prompt, provide function schemas and AI behavior
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools = [available_functions], system_instruction=system_prompt,
        ),
    )

    # 1.
    candidates = response.candidates # list of candidates [[candidates]]
    for candidate in candidates:
        messages.append(candidate.content)


    # show additional meta info if --verbose flag exists
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # failed to return valid list[FunctionCall]
    if not response.function_calls:
        # 3.
        print(f"LLM's final response: {response.text}")
        counter = 20
        return
        # return response.text
    
    function_responses = []
    # handle each FunctionCall
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts 
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Empty function call result.\n")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        function_responses.append(function_call_result.parts[0])
        # 2.
        messages.append(function_call_result)

    if not function_responses:
        raise Exception("No function responses were generated.\n")
    
    # 3.
    counter += 1

if __name__ == "__main__":
    main()