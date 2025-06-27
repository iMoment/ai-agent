import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    # if file_path is outside working directory
    if not target_file_abs_path.startswith(working_directory_abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # if file_path doesn't exist
    if not os.path.exists(target_file_abs_path):
        return f'Error: File "{file_path}" not found.'
    # if not a Python file
    if not target_file_abs_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    # execute python file
    try:
        commands = ["python3", target_file_abs_path]
        if args:
            commands.extend(args)
        completed_process = subprocess.run(
            commands, 
            capture_output=True, 
            timeout=30, 
            text=True,
            cwd=working_directory_abs_path,
        )
        output = []
        output.append("Process has been completed.")
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
# Builds the schema supplied to LLM, tells it how to use the function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python files located at the filepath, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file. If not provided, attempts to execute a single python file located by the given filepath in the preceding argument.",
                ),
                description="Optional arguments to pass to the Python file. If not provided, attempts to execute a single python file located by the given filepath in the preceding argument.",
            ),
        },
        required=["file_path"],
    ),
)