import chromadb
# Imports Python's built-in Operating System toolkit
import os 
# Imports a specific tool from the pypdf library
from pypdf import PdfReader
# Imports a specific tool to read .doc format documents 
from docx import Document

# Prints the exact folder path where the script is currently running 
print(os.getcwd())

# Gives a variable to the name of the folder that contains the files wnated
folder_path = "documents"
# Looks inside the variable and creates a list of file names inside
files = os.listdir(folder_path)

# Creates a Chromadb data base that saves to the computer hard drive and keeps it even when script finishes 
client = chromadb.PersistentClient(path="chroma_db")
# Creates a collection to hold text, or opens it if you already created it in the past 
collection = client.get_or_create_collection(name="my_documents")

# File for every file in the folder variable 
for file in files:
    # Prints name of the file currently being processed 
    print(file)
    # Sets counter for variabel to 0
    chunk_id = 0

    # Combines the folder name and file name safely so python knows here to look
    full_path = os.path.join(folder_path, file)

    # Checks if file is pdf 
    if file.lower().endswith('.pdf'):
        # Opens pdf using pdf tool form above
        reader = PdfReader(full_path)
        # Creates empty string variable 
        text = ""

        # Loops through every single page of the PDF, extracts the raw text, and glues it onto a text string.
        for page in reader.pages:
            text += page.extract_text()
        content = text

    # Loop similar to above but for doc format files instead
    elif file.lower().endswith('.docx'):
        doc = Document(full_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
            content = text
    else:
        #The file is not a pdf and safely opens the file in read and reads all text in time and saves it to 'content'
        with open(full_path, "r") as f:
            content = f.read()

    # Limits chunk size to 500 character sper chunk to fit the context size of the model and so the database is more manageable
    chunk_size = 500
    # Creates an empty list (a bucket) to hold your chopped-up pieces of text.
    chunks = []


    for i in range(0, len(content), chunk_size):
        chunk = content[i:i+chunk_size]
        chunks.append(chunk)

    # Generates a unique ID tag for this specific piece of text
    for chunk in chunks:
        collection.add(
        documents=[chunk],
        ids=[f"{file}_chunk_{chunk_id}"]
        )
        chunk_id += 1

# Once all files are read, chopped, and saved, this prints the total number of individual text and stores them to the database
print(collection.count())