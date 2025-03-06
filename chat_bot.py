from chromadb import PersistentClient  # type: ignore
from utils.prompt import get_prompt_login, get_validation_prompt, get_query_category, get_prompt_enrollment,get_format_text_prompt
from utils.llm import run_chat_login, run_chat_others, run_enrollment_chat
from sentence_transformers import SentenceTransformer   # type: ignore
from dotenv import load_dotenv # type: ignore
import os
from utils.summarize_chat_bot_conversation import summarize
import pymongo
from datetime import datetime

load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="insurance_vectordb/")
login_collection_db = client.get_collection(name="enrollement_knowlage_base")
enrollment_collection_db = client.get_collection(name="enrollement_knowlage_base")
#print(collection.count())

mongo_url = os.getenv("MONGO_URL")
client = pymongo.MongoClient(mongo_url)
db = client.insurance_chat_history
login_collection = db.login_chat_history
enrollment_collection = db.enrollment_chat_history

def chatbot(question, oldest_timestamp):
    """Takes in user question and returns answer."""
    
    #categorize the question
    category = run_chat_others(get_query_category(question))

    
    if category == "login":
      history_collection = login_collection
      response_function = run_chat_login
      vector_collection = login_collection_db
      prompt_function = get_prompt_enrollment
      
    elif category == "enrollment":
        history_collection = enrollment_collection
        response_function = run_enrollment_chat
        vector_collection = enrollment_collection_db
        prompt_function = get_prompt_enrollment
        
    else:
        return "Error: Invalid category. Please provide a valid category."

    #get latest chat
    latest_chat = history_collection.find_one({"created_at": {"$gt": oldest_timestamp}},  sort=[("created_at", -1)])
    print(f"Latest chat: {latest_chat}")
    
    latest_chat_question = latest_chat['question'] if latest_chat else ""
    latest_chat_answer = latest_chat['answer'] if latest_chat else ""
    latest_chat_formatted = f"User: {latest_chat_question} AI: {latest_chat_answer}" if latest_chat else ""
    print(f"Latest chat formatted: {latest_chat_formatted}")
  
    #combine lates chat and question for context retrival
    question_history = f"{question} {latest_chat_formatted}"
    print("Question history: ", question_history)
    
    #get question embedding
    question_embedding = model.encode(question_history)
  
    #get context
    context = vector_collection.query(
        query_embeddings=question_embedding,
        n_results=3)

    #format context
    documents = context.get('documents', [])
    flattened_doc=[item for sublist in documents for item in sublist]
    context = list(set(flattened_doc))
    
    #get 3 latest document to create hstory summary
    latest_documents = list(
    history_collection.find({"created_at": {"$gt": oldest_timestamp}})
    .sort("created_at", -1) 
    .limit(3)  )
    
    #create history summary
    history_summary = summarize(latest_documents)
    
    #create prompt
    prompt = prompt_function(context, history_summary,history_collection.find_one(
    {"created_at": {"$gt": oldest_timestamp}},  
    sort=[("created_at", -1)]  ), question)
    print(f"Final Prompt: {prompt}")
      
    #get response
    response = response_function(prompt)
    
    formatted_response = run_chat_others(get_format_text_prompt(response))
    
    #validate response
    validation_prompt = get_validation_prompt(response, question)
    validation_result = run_chat_others(validation_prompt)


    #save chat history
    history_collection.insert_one({
        "question": question,
        "answer": response,
        "created_at": datetime.utcnow()
    })
    
    
    
    #return validated prompt
    return validation_result

# print(chatbot("how to login as an agent?", "Login"))
# print(chatbot("And as a user?", "login"))
