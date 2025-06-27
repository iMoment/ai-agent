import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_abs_path.startswith(working_directory_abs_path): # file_path outside work_dir
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_abs_path): #file_path not file
        return f'Error: File not found or is not a regular file: "{file_path}"'
    # Read file, return contents as String
    try:
        with open(target_file_abs_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            if os.path.getsize(target_file_abs_path) > MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
    
# Builds the schema supplied to LLM, tells it how to use the function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns a file from the specified filepath, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read from, relative to the working directory."
            ),
        },
        required=["file_path"],
    ),
)
