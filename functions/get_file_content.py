import os
from config import *
from google.genai import types
def get_files_content(working_directory, file_path):
    try:   
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        is_files = os.path.isfile(target_dir)
        if not is_files:
            return f'Error: File not found or is not a regular file: "{file_path}"'
         
        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content

    except Exception as e:
       return f"Error: {e}"

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves specified file content relative to the working directory, providing file content truncated to {MAX_CHARS} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required = ["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to retrieve content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
        
