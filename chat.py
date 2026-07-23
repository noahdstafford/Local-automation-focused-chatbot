# This imports the request library allowing the script to send requests to a local server page for ollama via a URL link
# Then it drops off the prompt and waits for the text back from ollama 
import requests

# This feines a function taht can be reused giving it a specific name, it requires a text prompt then calls upon the intended model
def ask_ollama(prompt, model="qwen2.5:7b"):
    # Sends a specific HTTP request (basically to submit data for a response) 
    response = requests.post(
        "http://localhost:11434/api/generate",
        # Tells the request library to send the following data formatted as JSON object
        json={
            "model": model,
            "prompt": prompt,
            # Tells ollama to process the entire response, then give a single response all togetehr instead of streaming it word by word
            "stream": False
        }
    )
    # Takes the raw response from the server converts back from JSON to standard language python can understand so python can pull data out easily
    data = response.json()
    #Looks inisde the dictionary for the specific key named 'response' and returns it back to the function called
    return data["response"]

# This defines the main bit of program that the user interacts with
def main():
    # Prints a welcome message message and soem commands to help the user
    print("Local AI Assistant — type 'exit' to quit\n")
    # Creates the loop to create a communication loop with the user until ended
    while True:
        # Gives the text where the user inputs
        user_input = input("You: ")
        # Gives teh reasoning to break the loop
        if user_input.lower() == "exit":
            break
        # Sends the message to ollama via the function explained above
        reply = ask_ollama(user_input)
        # Gives the text where the ollama model replies
        print(f"\nAssistant: {reply}\n")

# This is a standard Python safeguard to check if you are running this script directly. 
# If you were to import this script into another script, it prevents the interactive loop from starting automatically.
if __name__ == "__main__":
    main()
