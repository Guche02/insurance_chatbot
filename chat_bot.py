from chromadb import PersistentClient 
from utils.prompt import get_prompt_login, get_validation_prompt, get_query_category, get_prompt_enrollment, get_user_enrollment_status
from utils.llm import run_chat_login, run_chat_others, run_enrollment_chat
from sentence_transformers import SentenceTransformer  
from dotenv import load_dotenv 
from utils.summarize_chat_bot_conversation import summarize
from datetime import datetime
from utils.mongodb import get_latest_chat, get_chat_history, add_collection

load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="insurance_vectordb/")
login_collection_db = client.get_collection(name="enrollement_knowlage_base")
enrollment_collection_db = client.get_collection(name="enrollement_knowlage_base")
#print(collection.count())


def chatbot(question, oldest_timestamp):
    """Takes in user question and returns answer."""
    
    #categorize the question
    category = run_chat_others(get_query_category(question))

    if category == "login":
      response_function = run_chat_login
      vector_collection = login_collection_db
      prompt_function = get_prompt_enrollment
      
    elif category == "enrollment":
        response_function = run_enrollment_chat
        vector_collection = enrollment_collection_db
        prompt_function = get_prompt_enrollment
        
    else:
        return "Error: Invalid category. Please provide a valid category."

    #get history
    history = get_chat_history(category, oldest_timestamp)
    latest_chat = get_latest_chat(category, oldest_timestamp)

    #combine lates chat and question for context retrival
    question_history = f"{question} {latest_chat}"
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
    
    #create history summary
    history_summary = summarize(history)
    
    #create prompt
    prompt = prompt_function(context, history_summary,latest_chat, question)
    print(f"Final Prompt: {prompt}")
      
    #get response
    response = response_function(prompt)
    
    #validate response
    validation_prompt = get_validation_prompt(response, question)
    validation_result = run_chat_others(validation_prompt)
    
    print("Validation result: ", validation_result)
    
    #check is user is enrolled
    enrollment_status = run_chat_others(get_user_enrollment_status(question))
    print("Enrollment status: ", enrollment_status)
    if enrollment_status == "new user":
        validation_result = validation_result + "\nGo to the website https://qa-enroll.corenroll.com/ to enroll in a plan."

    #save chat history 
    add_collection(category,{
        "question": question,
        "answer": validation_result,
        "created_at": datetime.utcnow()}
    )
    
    return validation_result 

# print(chatbot("how to login as an agent?", "Login"))
# print(chatbot("And as a user?", "login"))
