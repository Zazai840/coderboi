import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import *
from functions.generate_content import *
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
    for _ in range(20):   
        result = generate_content(client, messages, args.verbose)
        if result: 
            print("Final response:")
            print(result)
            return


    print("Maximum iterations reached without a final response")
    sys.exit(1)
 
    

        
if __name__ == "__main__":
    main()


