from chromadb import PersistentClient  # type: ignore
from utils.prompt import get_prompt, get_validation_prompt, get_query_category
from utils.llm import run_chat_login, run_chat_others
from sentence_transformers import SentenceTransformer   # type: ignore
 
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="new_vector_db/")
collection = client.get_collection(name="login_related_chunks")

print(collection.count())

def chatbot(question):
    question_embedding = model.encode(question)
    context = collection.query(
    query_embeddings=question_embedding,  
    n_results=3
    )   
    print(f"Retrived context: {context}")
    prompt_for_type = get_query_category(question)
    prompt = get_prompt(context['documents'],question)
    prompt_type = run_chat_login(prompt_for_type)
    print(f"Prompt type: {prompt_type}")
    if prompt_type == "login":
        response = run_chat_login(prompt)
    else:
        response = run_chat_others(prompt)
    print(f"Initial Response: {response}")

    validation_prompt = get_validation_prompt(response, question)
    print(f"Validation prompt: {validation_prompt}")
    validation_result = run_chat_others(validation_prompt)
    print(f"Final result: {validation_result}")

    return validation_result

# print(chatbot("How do I purchase an insurance?")) 
# print(chatbot("I forgot my password, how do I reset it?"))