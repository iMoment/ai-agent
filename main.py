# On program start, load environment variables
# from .env file using dotenv library and reading
# API key
import os
from dotenv import load_dotenv
from google import genai

prompt_str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) # create new instance of Gemini client
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=prompt_str
)
prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count
print("We are using Google Gemini AI.\n")
print(f"Here is the prompt: {prompt_str}\n")
print(f"Google Gemini's response: {response.text}\n")
print(f"Prompt tokens: {prompt_token_count}")
print(f"Response tokens: {candidates_token_count}")