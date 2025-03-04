from chromadb import PersistentClient  # type: ignore
from utils.prompt import get_prompt_login, get_validation_prompt, get_query_category
from utils.llm import run_chat_login, run_chat_others
from sentence_transformers import SentenceTransformer   # type: ignore
from dotenv import load_dotenv # type: ignore
import os
from utils.summarize_chat_bot_conversation import summarize
import pymongo
from datetime import datetime

load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="insurance_vectordb/")
login_collection_db = client.get_collection(name="login_knowlage_base")
enrollment_collection_db = client.get_collection(name="enrollement_knowlage_base")
#print(collection.count())

mongo_url = os.getenv("MONGO_URL")
client = pymongo.MongoClient(mongo_url)
db = client.insurance_chat_history
login_collection = db.login_chat_history
enrollment_collection = db.enrollment_chat_history

def chatbot(question, category, oldest_timestamp):
    """Takes in user question and returns answer."""
    
    if category == "Login":
      history_collection = login_collection
      response_function = run_chat_login
      vector_collection = login_collection_db
      prompt_function = get_prompt_login
    elif category == "Enrollment":
        history_collection = enrollment_collection
        response_function = run_enrollment_chat
        vector_collection = enrollment_collection_db
        prompt_function = get_prompt_enrollment
        
    else:
        return "Error: Invalid category. Please provide a valid category."

    print("History collection used: ", history_collection)
    print("Vector collection used: ", vector_collection)

    print("response function used: ", response_function)
    
    latest_chat = history_collection.find_one({"created_at": {"$gt": oldest_timestamp}},  sort=[("created_at", -1)])
    print(f"Latest chat: {latest_chat}")
    
    latest_chat_question = latest_chat['question'] if latest_chat else ""
    latest_chat_answer = latest_chat['answer'] if latest_chat else ""
    latest_chat_formatted = f"User: {latest_chat_question} AI: {latest_chat_answer}" if latest_chat else ""
    print(f"Latest chat formatted: {latest_chat_formatted}")
  
    question_history = f"{question} {latest_chat_formatted}"
    print("Question history: ", question_history)
    
    question_embedding = model.encode(question_history)
  
    #get context
    context = vector_collection.query(
        query_embeddings=question_embedding,
        n_results=3,
    )
    print(f"Retrieved context: {context}")
      
    latest_documents = list(
    history_collection.find({"created_at": {"$gt": oldest_timestamp}})
    .sort("created_at", -1) 
    .limit(3)  
)
    print("Latest documents: ", latest_documents)

    history_summary = summarize(latest_documents)
    print(f"Chat History Summary: {history_summary}\n")
    prompt = get_prompt_login(context['documents'], history_summary,history_collection.find_one(
    {"created_at": {"$gt": oldest_timestamp}},  
    sort=[("created_at", -1)]  ), question)
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

# print(chatbot("how to login as an agent?", "Login"))
# print(chatbot("And as a user?", "login"))