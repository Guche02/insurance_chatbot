from chromadb import PersistentClient  # type: ignore
from utils.prompt import get_prompt, get_validation_prompt, get_query_category
from utils.llm import run_chat_login, run_chat_others
from sentence_transformers import SentenceTransformer   # type: ignore
from dotenv import load_dotenv
import os
from utils.summarize_chat_bot_conversation import summarize

load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="new_vector_db/")
collection = client.get_collection(name="login_related_chunks")

print(collection.count())

import pymongo

mongo_url = os.getenv("MONGO_URL")
client = pymongo.MongoClient(mongo_url)
db = client.insurance_chat_history
mongo_collection = db.chat_history

from datetime import datetime

from datetime import datetime

def chatbot(question):

    """Takes in user question and returns answer."""
    #encode question
    question_embedding = model.encode(question)

    #get context from vector db
    context = collection.query(
    query_embeddings=question_embedding,
    n_results=3
      
    print(f"Retrived context: {context}")
      
    prompt_for_type = get_query_category(question)
   
    # print(f"Retrived context: {context}\n")

    #get histroy
    latest_documents = mongo_collection.find().sort("created_at", -1).limit(10)
    print(latest_documents)

    #get history
    history_summary = summarize(latest_documents)
    # print(f"Chat History Summary: {history_summary}\n")

    #get answer
    prompt = get_prompt(context['documents'], history_summary, mongo_collection.find_one(sort=[("created_at", -1)]),question)
      
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
    # print(f"Initial Response: {response}\n")

    #push conversation to history in mongodb
    mongo_collection.insert_one({
    "question": question,
    "answer": response,
    "created_at": datetime.utcnow()
    })


    return response

# print(chatbot("How do I purchase an insurance?")) 
# print(chatbot("I forgot my password, how do I reset it?"))