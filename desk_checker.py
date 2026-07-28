import cv2
import base64
import requests

def run_desk_checker():
    camera = cv2.VideoCapture(1)
    success, frame = camera.read()
    print("Camera capture success:", success)
    cv2.imwrite("webcam_snapshot.jpg", frame)
    camera.release()

    with open("webcam_snapshot.jpg", "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

# You are setting up the same local API call as beofore
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            # New model that uses Vision-language to hel read images
            "model": "qwen2.5vl:7b",
            "prompt": "Whats visible on this desk?",
            # Passes the base 64 string of the image to the AI alongside the prompt here 
            "images": [image_data],
            "stream": False
        }
    )

    data = response.json()
    answer = data["response"]
    print(answer)

if __name__ == "__main__":
    run_desk_checker()