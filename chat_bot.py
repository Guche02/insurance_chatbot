from chromadb import PersistentClient  # type: ignore
from utils.prompt import get_prompt, get_validation_prompt, get_query_category
from utils.llm import run_chat_login, run_chat_others
from sentence_transformers import SentenceTransformer   # type: ignore
from dotenv import load_dotenv # type: ignore
import os
from utils.summarize_chat_bot_conversation import summarize
import pymongo
from datetime import datetime

load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="new_vector_db/")
collection = client.get_collection(name="login_related_chunks")

mongo_url = os.getenv("MONGO_URL")
client = pymongo.MongoClient(mongo_url)
db = client.insurance_chat_history
login_collection = db.login_chat_history
enrollment_collection = db.enrollment_chat_history

def chatbot(question, category):
    """Takes in user question and returns answer."""
    # prompt_for_type = get_query_category(question)
    # category = run_chat_login(prompt_for_type)
    # print(f"Prompt type: {category}")
    
    if category == "Login":
      history_collection = login_collection
      response_function = run_chat_login
    else:
        history_collection = enrollment_collection
        response_function = run_chat_others

    print("collection used: ", history_collection)
    print("response function used: ", response_function)
    
    latest_chat = history_collection.find_one(sort=[("created_at", -1)])
    print(f"Latest chat: {latest_chat}")
    
    latest_chat_question = latest_chat['question'] if latest_chat else ""
    latest_chat_answer = latest_chat['answer'] if latest_chat else ""
    latest_chat_formatted = f"User: {latest_chat_question} AI: {latest_chat_answer}" if latest_chat else ""
    print(f"Latest chat formatted: {latest_chat_formatted}")
  
    question_history = f"{question} {latest_chat_formatted}"
    print("Question history: ", question_history)
    
    question_embedding = model.encode(question_history)
    context = collection.query(
        query_embeddings=question_embedding,
        n_results=3
    )
    print(f"Retrieved context: {context}")
      
    latest_documents = list(history_collection.find().sort("created_at", -1).limit(3))
    print("Latest documents: ", latest_documents)

    history_summary = summarize(latest_documents)
    print(f"Chat History Summary: {history_summary}\n")
    prompt = get_prompt(context['documents'], history_summary, history_collection.find_one(sort=[("created_at", -1)]), question)
    print(f"Final Prompt: {prompt}")
      
    response = response_function(prompt)
    print(f"Initial Response: {response}")
    validation_prompt = get_validation_prompt(response, question)
    print(f"Validation prompt: {validation_prompt}")
    validation_result = run_chat_others(validation_prompt)
    print(f"Final result: {validation_result}")

    history_collection.insert_one({
        "question": question,
        "answer": response,
        "created_at": datetime.utcnow()
    })
    return response

# print(chatbot("how to purchase an insurance plan?", "Enrollment"))
# print(chatbot("And as a user?", "Login"))