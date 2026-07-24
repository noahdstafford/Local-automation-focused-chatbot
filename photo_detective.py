import base64
import requests

checked_image = input('Give the file name of the image you wnat checked: ')
user_question = input('What do you wish to be checked in relation to this image: ')

with open(checked_image, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

# You are setting up the same local API call as beofore
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        # New model that uses Vision-language to hel read images
        "model": "qwen2.5vl:7b",
        "prompt": user_question,
        # Passes the base 64 string of the reciept image to the AI alongside the prompt here 
        "images": [image_data],
        "stream": False
    }
)
data = response.json()
answer = data["response"]
print(answer)