import requests

def ask_ollama(prompt, model="qwen2.5:7b"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    data = response.json()
    return data["response"]

def main():
    print("Local AI Assistant — type 'exit' to quit\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        reply = ask_ollama(user_input)
        print(f"\nAssistant: {reply}\n")

if __name__ == "__main__":
    main()
