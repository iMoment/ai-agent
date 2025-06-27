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
from config import MAX_ITERATIONS

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
    
    iterations = 0
    while True:
        iterations += 1
        if iterations > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

# checks proper formatting of system arguments for code execution
def sysCheck(args):
    if not args:
        print("We are using Google Gemini AI Code Assistant.\n")
        print('Usage: python3 main.py "Your prompt here" [--verbose]\n')
        print('Example: python3 main.py "How do I fix the calculator?"')
        sys.exit(1)

# handles generation of content, handle user prompt
def generate_content(client, messages, verbose):
    # sets roles, passes user's prompt, provide function schemas and AI behavior
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools = [available_functions], system_instruction=system_prompt,
        ),
    )

    # show additional meta info if --verbose flag exists
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # add response candidates to our list of messages
    if response.candidates: # list of candidates [candidates]
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    # failed to return valid list[FunctionCall]
    if not response.function_calls:
        return response.text
    
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

    if not function_responses:
        raise Exception("No function responses were generated, exiting.\n")

    messages.append(types.Content(role="tool", parts=function_responses))

if __name__ == "__main__":
    main()