from chat import ask_ollama

def review_code(code):
# This replaces the first comment and creates a variable called prompt that hold the instruction as well as the code
    prompt = f"""You are a code reviewer. Review the following code for bugs, 
readability, and best practices. Explain issues clearly.

CODE:
{code}"""
    # Sends the message to ollama to have a look 
    code_answer = ask_ollama(prompt)
    return code_answer


print("Paste your code below. Type END on its own line, or press Ctrl+Z then Enter (Windows) / Ctrl+D (Mac/Linux) when done:")
lines = []
while True:
    try:
        line = input()
        if line == 'END':
            break
        lines.append(line)
    except EOFError:
        break
full_code = '\n'.join(lines)

result = review_code(full_code)

print(f"\nCode Review:\n{result}")