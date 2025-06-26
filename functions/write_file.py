import os

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
