import os
import subprocess

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
        return f"Error occurred: {e}"