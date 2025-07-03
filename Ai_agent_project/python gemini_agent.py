import google.generativeai as genai

def main():
    # Get the API key from the user
    api_key = input("Enter your Google API key: ")
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Set up the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",  # You may need to use "gemini-pro" depending on access
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 2048,
        }
    )
    
    # Start a chat session
    chat = model.start_chat(history=[])
    
    print("Gemini AI Agent is now running. Type 'exit' or 'quit' to end the session.")
    
    # Main interaction loop
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending session. Goodbye!")
            break
        
        # Simple calculator functionality
        if user_input.lower().startswith("calculate "):
            expression = user_input[10:].strip()
            try:
                result = eval(expression)
                response = f"The result of {expression} is {result}"
            except Exception as e:
                response = f"Error calculating: {str(e)}"
        else:
            # Get response from Gemini
            response = chat.send_message(user_input)
            response = response.text
        
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()