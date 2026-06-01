import os 
import subprocess
from google.genai import types

def run_python_file (working_directory: str, file_path: str, args: list[str] | None = None) -> str: 
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        

        command = ["python", target_dir]
        if args: 
            command.extend(args)
        
        completed_process = subprocess.run(command, 
                                        cwd=working_dir_abs, 
                                        capture_output=True,  
                                        text=True, 
                                        timeout=30)

        output = []

        if completed_process.returncode != 0:
            output.append("Process exited with code X")
        if completed_process.stdout == "" and completed_process.stderr == "": 
            output.append("No output produced")
        else:
            if completed_process.stdout:
                output.append(f"STDOUT: {completed_process.stdout}")
            if completed_process.stderr:
                output.append(f"STDERR: {completed_process.stderr}")
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error: executing python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file from a file path and working directory with extra args",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of file to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type = types.Type.STRING
                ),
                description="Optional list of arguments to pass to Python script"
            )
        },
    ),
)

    

    


    
    
    
        