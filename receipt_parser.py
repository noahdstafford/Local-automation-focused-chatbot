import base64
import requests
import json
import csv
import os

with open("test_receipt.png", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5vl:7b",
        "prompt": """Look at this receipt image and extract the following information.

        Respond ONLY with JSON in this exact format, no other text:
        {"vendor": "...", "date": "...", "total": "..."}""",
        "images": [image_data],
        "stream": False
    }
)

data = response.json()
answer = data["response"]
answer = answer.replace("```json", "").replace("```", "").strip()
receipt_info = json.loads(answer)
print(receipt_info)

file_exists = os.path.exists("budget_log.csv")

with open("budget_log.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["Vendor", "Date", "Total"])
    writer.writerow([receipt_info["vendor"], receipt_info["date"], receipt_info["total"]])

print("CSV write complete")