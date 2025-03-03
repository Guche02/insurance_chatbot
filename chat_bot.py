from chromadb import PersistentClient  # type: ignore
from utils.prompt import get_prompt, get_validation_prompt
from utils.llm import run_chat
from sentence_transformers import SentenceTransformer   # type: ignore
from dotenv import load_dotenv
import os
from utils.summarize_chat_bot_conversation import summarize

load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="vectordb/")
collection = client.get_collection(name="knowlage_base")

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
    )
    # print(f"Retrived context: {context}\n")

    #get histroy
    latest_documents = mongo_collection.find().sort("created_at", -1).limit(10)
    print(latest_documents)

    #get history
    history_summary = summarize(latest_documents)
    # print(f"Chat History Summary: {history_summary}\n")

    #get answer
    prompt = get_prompt(context['documents'], history_summary, mongo_collection.find_one(sort=[("created_at", -1)]),question)
    response = run_chat(prompt)
    # print(f"Initial Response: {response}\n")

    #push conversation to history in mongodb
    mongo_collection.insert_one({
    "question": question,
    "answer": response,
    "created_at": datetime.utcnow()
    })

    return response

print(chatbot("How do I change my name on my policy ?")) 
# print(chatbot("How does an agent sell their plans?")) 