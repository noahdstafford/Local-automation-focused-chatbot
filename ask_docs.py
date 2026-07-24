import chromadb
from chat import ask_ollama

# Connects to the exact same database folder created in the read
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="my_documents")

print(collection.count())

question = input("What do you want to know? ")

# Gives question inputted above to the data base as a search query
results = collection.query(
    query_texts=[question],
    # Tells the database to give three most relevant chunks 
    n_results=3
)

#This puts together the chunks that the database gives in one single block of text and saves it
context = "\n\n".join(results["documents"][0])

# Gives the 3 selected chunks in the prompt as well as the users question
prompt = f"""Answer the question using only the information below. 
If the answer isn't in the information, say you don't know.

INFORMATION:
{context}

QUESTION:
{question}"""

# Gives teh huge designed prompt to ollama to process
answer = ask_ollama(prompt)
# Prints ollama's answer
print(answer)