from chromadb import PersistentClient  # type: ignore
from utils.prompt import get_prompt, get_validation_prompt, get_query_category
from utils.llm import run_chat_login, run_chat_others
from sentence_transformers import SentenceTransformer   # type: ignore
from dotenv import load_dotenv # type: ignore
import os
from utils.summarize_chat_bot_conversation import summarize

load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="new_vector_db/")
collection = client.get_collection(name="login_related_chunks")

#print(collection.count())

import pymongo

mongo_url = os.getenv("MONGO_URL")
client = pymongo.MongoClient(mongo_url)
db = client.insurance_chat_history
mongo_collection = db.chat_history

from datetime import datetime

def chatbot(question, category):

    """Takes in user question and returns answer."""
    #get the latest chat
    latest_chat = mongo_collection.find_one(sort=[("created_at", -1)])
    #print(f"Latest chat: {latest_chat}")
    
    #format latest chat
    latest_chat_question= latest_chat['question']
    latest_chat_answer = latest_chat['answer']
    latest_chat_formatted = f"User: {latest_chat_question} AI: {latest_chat_answer}"
    #print(f"Latest chat formatted: {latest_chat_formatted}")
  
    #combine question and latest chat
    question_history = f"{question} {latest_chat_formatted}"
    #print("Question history: ", question_history)
    
    #encode question/latestchat
    question_embedding = model.encode(question_history)
  
    #get context
    context = collection.query(
    query_embeddings=question_embedding,
    n_results=3
    )
    print(f"Retrived context: {context}")
      
    prompt_for_type = get_query_category(question)
   
    latest_documents = list(mongo_collection.find().sort("created_at", -1).limit(10))
    #print("latest documents: ", latest_documents)

    history_summary = summarize(latest_documents)
    #print(f"Chat History Summary: {history_summary}\n")
    prompt = get_prompt(context['documents'], history_summary, mongo_collection.find_one(sort=[("created_at", -1)]),question)
    print(f"Final Prompt: {prompt}")
      
    prompt_type = run_chat_login(prompt_for_type)
    #print(f"Prompt type: {prompt_type}")
    if prompt_type == "login":
        response = run_chat_login(prompt)
    else:
        response = run_chat_others(prompt)

    #print(f"Initial Response: {response}")
    validation_prompt = get_validation_prompt(response, question)
    #print(f"Validation prompt: {validation_prompt}")
    validation_result = run_chat_others(validation_prompt)
    #print(f"Final result: {validation_result}")

    #push conversation to history in mongodb
    mongo_collection.insert_one({
    "question": question,
    "answer": response,
    "created_at": datetime.utcnow()
    })

    return response

print(f"Answer: {chatbot("how to login as an agent?", "login")}")
print(f"Answer: {chatbot("And as a user?", "login")}")