import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
import argparse

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("add API key to project .env file from Google AI studio")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action = 'store_true', help = 'Enable verbose output')
    args = parser.parse_args()
    
    
    client = genai.Client(api_key = api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    generate_content(client, messages, args.verbose)

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
    print("Response:")
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()


