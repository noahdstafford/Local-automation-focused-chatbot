import chromadb
from chat import ask_ollama

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="my_documents")

print(collection.count())

question = input("What do you want to know? ")

results = collection.query(
    query_texts=[question],
    n_results=3
)

context = "\n\n".join(results["documents"][0])

prompt = f"""Answer the question using only the information below. 
If the answer isn't in the information, say you don't know.

INFORMATION:
{context}

QUESTION:
{question}"""

answer = ask_ollama(prompt)
print(answer)