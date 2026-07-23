# Goes into other file and uses the ask_ollama function 
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
#Creates an empty list  where the users code will be stored line by line 
lines = []
while True:
    #Tells python to 'try' the block of code and lookout for the specific block of code
    try:
        line = input()
        if line == 'END':
            break
        # Takes the lie of code the user psted and puts it inti our lines bucket
        lines.append(line)
    # This sends a hardcore system signal that absolutely no more text is coming
    except EOFError:
        break
# Command takes all the seperate induvidual ines and puts the m back togetehr as one full block of text 
full_code = '\n'.join(lines)

print("\nAnalyzing your code, please wait...\n")

#Takes the giant, glued-together block of user code and passes it into your review_code function at the top of the script.
result = review_code(full_code)

print(f"\nCode Review:\n{result}")