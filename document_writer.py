import os
# Imports a pattern-matching language used by programmers to discover highy specific text combinateiosn
import re
from chat import ask_ollama


# Generic openings for any sort of communication drafts
generic_openers = [
    "I hope this message finds you well",
    "I hope you're doing well",
    "I hope you are doing well",
    "I wanted to take a moment to"
]

# Creates a new function to work on AI's final repsonse
def clean_response(text):
    # Takes a huge block of text and chnages it into manageable blocks of text
    lines = text.split("\n")

    # If there is text to read it gets the initial ines and uses the [.strip()] function and deletes any invisible blanks at start or end of sentence
    if lines:
        first_line = lines[0].strip()
        # Checks does the line start with any of the overly generic questions
        matches_phrase = any(first_line.startswith(phrase) for phrase in generic_openers)
        # Uses re, checks for a pattern ignores any of the phrases regardless of case 
        matches_greeting = bool(re.match(r"^(Hello|Hi|Dear|Hey)[\s,]", first_line, re.IGNORECASE))
        if matches_phrase or matches_greeting:
            # Chops of line 1 and keeps everything after
            lines = lines[1:]
    # Sticks remaining text together inot a block then sneds it bakc to main script
    return "\n".join(lines).strip()


def run_document_writer():

    # Asks user what the they wnat to write about
    topic = input("What document do you want written? Describe the topic: ")

    # Buids a prompt for the model tocomperhened and give a full designed response
    prompt = f"""Write a well-structured document on the following topic, with clear sections.

TOPIC:
{topic}"""

    print("\nWriting your document, please wait...\n")

    # Special line, calls on my ollama modle that has been trained off my specific vocab is another document and uses it
    answer = ask_ollama(prompt, model="noah-writer")
    # Takes the answer and removes generic opener
    answer = clean_response(answer)

    # Prints final polished document on the screen
    print(answer)

    # Writes to a document about the history of generated text
    filename = "generated_document.md"
    with open(filename, "w") as f:
        f.write(answer)

    # Tells the user where the file has been saved
    print(f"\nSaved to {filename}")

# If you ever import this script into another file, this keeps it quiet so it doesn't accidentally run
if __name__ == "__main__":
    run_document_writer()