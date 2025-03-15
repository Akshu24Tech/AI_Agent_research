from dotenv import load_dotenv
import os
from anthropic import BadRequestError
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

def check_api_key():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not found in .env file")
    return api_key

def main():
    try:
        load_dotenv()
        api_key = check_api_key()
        
        # Initialize the model with basic configuration
        chat = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            anthropic_api_key=api_key,
            temperature=0
        )
        
        while True:
            query = input("What can I help you research? (or 'quit' to exit): ").strip()
            
            if query.lower() == 'quit':
                break
                
            if not query:
                print("Please enter a valid query")
                continue
            
            try:
                # Simple message structure
                messages = [
                    SystemMessage(content="You are a helpful research assistant."),
                    HumanMessage(content=query)
                ]
                
                response = chat.invoke(messages)
                print("\nResponse:", response.content)
                
            except BadRequestError as e:
                if "credit balance is too low" in str(e):
                    print("\nError: Your Anthropic API credit balance is too low.")
                    print("Please visit https://console.anthropic.com/settings/billing to add credits.")
                    break
                else:
                    print(f"\nAPI Error: {str(e)}")
            except Exception as e:
                print(f"\nError during processing: {str(e)}")
                
    except Exception as e:
        print(f"Startup Error: {str(e)}")

if __name__ == "__main__":
    main()