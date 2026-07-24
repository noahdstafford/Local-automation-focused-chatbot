# A new toolkit is added that Base64 is a translation tool that converts raw binary image data into a 
# massive string of standard text characters so it can be sent over the internet safely.
import base64
import requests
import json
#Python's built-in toolkit for reading and writing "Comma Separated Values" files
import csv
import os

def run_receipt_parser():
    image_path = input("Enter the receipt image filename: ")

    # This reads the raw image data which encodes it into a massive Base64 string then decodes it after 
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    print("\nReading receipt, please wait...\n")

    # You are setting up the same local API call as beofore
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            # New model that uses Vision-language to hel read images
            "model": "qwen2.5vl:7b",
            "prompt": """Look at this receipt image and extract the following information.

            Respond ONLY with JSON in this exact format, no other text:
            {"vendor": "...", "date": "...", "total": "..."}""",
            # Passes the base 64 string of the reciept image to the AI alongside the prompt here 
            "images": [image_data],
            "stream": False
        }
    )

    # Extracts the raw text response from the API
    data = response.json()
    answer = data["response"]
    # Checks the the file on the harddrive and enusres the header column isnt repeated
    answer = answer.replace("```json", "").replace("```", "").strip()
    receipt_info = json.loads(answer)
    print(receipt_info)

    file_exists = os.path.exists("budget_log.csv")

    # Opens the CSV file in "a" (append) mode so it adds data to the bottom without overwriting what is already there
    with open("budget_log.csv", "a", newline="") as f:
        # Hands the open file over to the CSV toolkit to manage the tricky spreadsheet formatting
        writer = csv.writer(f)
        # If the file didn't exist before this script ran, this writes the top row of column headers
        if not file_exists:
            writer.writerow(["Vendor", "Date", "Total"])
        # Takes 3 pieces of data from AI and writes them to the spreadsheet as a perfectly formatted row
        writer.writerow([receipt_info["vendor"], receipt_info["date"], receipt_info["total"]])
        
    print("CSV write complete")

if __name__ == "__main__":
    run_receipt_parser()