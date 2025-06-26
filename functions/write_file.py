import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_abs_path.startswith(working_directory_abs_path): # file_path outside work_dir
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file_abs_path):
        # create filepath
        try:
            os.makedirs(os.path.dirname(target_file_abs_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    # check if file_path leads to directory
    if os.path.exists(target_file_abs_path) and os.path.isdir(target_file_abs_path):
        return f'Error: "{file_path}" is a directory, not a file'
    # overwrite file contents with content
    try:
        with open(target_file_abs_path, "w") as file:
            file.write(content)
        return (
            f'Successfully wrote to "{target_file_abs_path}": ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"

# Builds the schema supplied to LLM, tells it how to use the function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content into a file located at the specified filepath, constrained to the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified filepath.",
            ),
        },
        required=["file_path", "content"],
    ),
)