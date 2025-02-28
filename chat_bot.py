from chromadb import PersistentClient  # type: ignore
from utils.prompt import get_prompt, get_validation_prompt
from utils.llm import run_chat
from sentence_transformers import SentenceTransformer   # type: ignore
 
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="vectordb/")
collection = client.get_collection(name="knowlage_base")

print(collection.count())

def chatbot(question):
    question_embedding = model.encode(question)
    context = collection.query(
    query_embeddings=question_embedding,  
    n_results=3
    )   
    print(f"Retrived context: {context}")
    prompt = get_prompt(context['documents'],question)
    response = run_chat(prompt)
    print(f"Initial Response: {response}")

    validation_prompt = get_validation_prompt(response, question)
    print(f"Validation prompt: {validation_prompt}")
    validation_result = run_chat(validation_prompt)
    print(f"Final result: {validation_result}")

    return validation_result

print(chatbot("How do I change my name on my policy ?")) 
# print(chatbot("How does an agent sell their plans?")) 