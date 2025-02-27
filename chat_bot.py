from chromadb import PersistentClient
from utils.prompt import get_prompt
from utils.llm import run_chat
from sentence_transformers import SentenceTransformer 


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="vectordb/")
collection = client.get_collection(name="knowlage_base")

print(collection.count())
def chatbot(question):
    question_embedding = model.encode(question)
    context = collection.query(
    query_embeddings=question_embedding,  
    n_results=5
    )   
    print(f"Retrived context: {context}")
    prompt = get_prompt(context['documents'],question)
    return run_chat(prompt)

print(chatbot("How do I change my name on my policy ?"))
    