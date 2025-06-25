import os

def get_file_content(working_directory, file_path):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_abs_path.startswith(working_directory_abs_path): # file_path outside work_dir
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_abs_path): #file_path not file
        return f'Error: File not found or is not a regular file: "{file_path}"'
    # Read file, return contents as String
    MAX_CHARS = 10000
    try:
        with open(target_file_abs_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            if len(file_content_string) == 10000:
                file_content_string += f'[...File "{target_file_abs_path}" truncated at 10000 characters]'
            return file_content_string

    except Exception as e:
        return f"Error: {e}"



# os.path.abspath: Get an absolute path from a relative path
# os.path.join: Join two paths together safely (handles slashes)
# .startswith: Check if a string starts with a specific substring
# os.path.isfile: Check if a path is a file
