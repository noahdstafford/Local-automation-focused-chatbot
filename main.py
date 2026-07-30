import json
import requests
from chat import ask_ollama, run_chat
# Gives a way to call on each python agent of the model
from code_reviewer import run_code_reviewer
from ask_docs import run_ask_docs
from organiser import run_organiser
from receipt_parser import run_receipt_parser
from photo_detective import run_photo_detective
from document_writer import run_document_writer
from website_generator import run_website_generator
from desk_checker import run_desk_checker
from performance_checker import run_performance_checker
from voice_assistant import run_voice_assistant
from news_digest import get_news_digest


# This is the initial input that starts the whole program
user_request = input('Assistant: So what can i help you with today? \n')

# Giving AI a way to make decisions between various agents
router_prompt = f"""You are a router for a local AI assistant with these tools:

1. chat - general conversation, answering questions
2. code_review - reviewing or debugging pasted code
3. ask_docs - answering questions using the user's own documents/notes
4. organise_files - moving, renaming, or organising files in a folder
5. receipt_parser - reading a receipt image and logging it to a budget spreadsheet
6. photo_detective - answering a question about any other image
7. document_writer - Constructing detailed documents, emails or other written texts
8. website_generator - This uses a user prompt and generates the website described
9. desk_checker - checking the webcam to see what's on the desk
10. performance_checker - checking CPU, memory, and disk usage and interpreting system health
11. Voice assistant - communicate with the model verbally and get verbal responses back
12. news_digest - fetches and summarizes today's tech, business, Irish, UK, and world news

Given the user's request below, respond ONLY with JSON in this exact format, no other text:
{{"tool": "one_of_the_names_above"}}


USER REQUEST:
{user_request}"""
# ^ Applies what the user asked for with the prompt above

print("\nFiguring out what you need...\n")


ollama_response = ask_ollama(router_prompt)

print(ollama_response)

# Ensures the text is purely JSON and doesnt include makrdowns and backticks
ollama_response = ollama_response.replace("```json", "").replace("```", "").strip()
# Translates the pure JSON string into python understandable dictionary
parsed = json.loads(ollama_response)
print(parsed)

# Based off what the AI chosese the user needes it selects a program modle to use
if parsed["tool"] == "chat":
    run_chat()
elif parsed["tool"] == "code_review":
    run_code_reviewer()
elif parsed["tool"] == "ask_docs":
    run_ask_docs()
elif parsed["tool"] == "organise_files":
    run_organiser()
elif parsed["tool"] == "receipt_parser":
    run_receipt_parser()
elif parsed["tool"] == "photo_detective":
    run_photo_detective()
elif parsed["tool"] == "document_writer":
    run_document_writer()
elif parsed["tool"] == "website_generator":
    run_website_generator()
elif parsed["tool"] == "desk_checker":
    run_desk_checker()
elif parsed["tool"] == "performance_checker":
    run_performance_checker()
elif parsed["tool"] == "voice_assistant":
        run_voice_assistant()
elif parsed["tool"] == "news_digest":
    news_digest = get_news_digest()
    print(news_digest)