from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import *

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config = types.GenerateContentConfig(
                                            system_instruction=system_prompt,
                                            temperature=0,
                                            tools = [available_functions]
                                        )
        
    )
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
   

    if response.candidates: 
        for candidates in response.candidates: 
            if candidates.content:
                messages.append(candidates.content)
    
    if response.function_calls:
        function_results = []
        for call in response.function_calls:
            function_call_result = call_function(call, verbose)
            if not function_call_result.parts:
                raise Exception("empty function call result parts")
            if not function_call_result.parts[0].function_response:
                raise Exception("function response none")
            if function_call_result.parts[0].function_response.response and function_call_result.parts[0].function_response.response == None:
                raise Exception("function result is none")
            function_results.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        if function_results:
            messages.append(types.Content(role="user", parts=function_results))
        return 
    else:
        return response.text
