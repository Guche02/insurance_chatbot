from utils.prompt import get_validation_prompt, get_query_category, get_prompt_enrollment, get_user_enrollment_status,query_reformulation_prompt, get_formatting_prompt
from utils.llm import run_chat_login, run_chat_others, run_enrollment_chat
from dotenv import load_dotenv 
from datetime import datetime
from utils.mongodb import  add_collection
from langchain.memory import ConversationTokenBufferMemory
from langchain.vectorstores import Chroma
import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain, LLMChain,StuffDocumentsChain

load_dotenv()


embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="insurance_vectordb/")
login_collection_db = Chroma(client=client, collection_name="enrollement_knowlage_base", embedding_function=embedding_function)
enrollment_collection_db = Chroma(client=client, collection_name="enrollement_knowlage_base", embedding_function=embedding_function)
#print(collection.count())


def chatbot(question):
    """Takes in user question and returns answer."""
    
    #categorize the question
    category = run_chat_others(get_query_category(question))

    if category == "login":
      response_function = run_chat_login()
      vector_collection = login_collection_db
      prompt_function = get_prompt_enrollment()
      
    elif category == "enrollment":
        response_function = run_enrollment_chat()
        vector_collection = enrollment_collection_db
        prompt_function = get_prompt_enrollment()
        
    else:
        return "Error: Invalid category. Please provide a valid category."

    #chain
    
    #chain that takes the user question and main prompt function
    llm_chain = LLMChain(llm=response_function, prompt=prompt_function)
    
    # StuffDocumentsChain to process the retrieved documents and the user question
    combine_docs_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context"  
    )
        
    question_generator_chain = LLMChain(llm=response_function, prompt=query_reformulation_prompt())
    
    memory = ConversationTokenBufferMemory(
    llm=response_function,  
    memory_key="chat_history",
    return_messages=True,
    max_token_limit=500 
    )
    
    retriever = vector_collection.as_retriever()
    
    # ConversationalRetrievalChain, combining everything
    chain = ConversationalRetrievalChain(
        combine_docs_chain=combine_docs_chain,
        retriever=retriever,
        question_generator=question_generator_chain,
        memory=memory  
    )
    
    response = chain.invoke({ 
	"question": question
    }) 

    #validate response
    validation_prompt = get_validation_prompt(response, question)
    validation_result = run_chat_others(validation_prompt)
    
    print("Validation result:",validation_result.strip(),"end")

    #check is user is enrolled
    enrollment_status = run_chat_others(get_user_enrollment_status(question))

    print("Enrollment status: ", enrollment_status)
    if "I don't have enough information" in validation_result and enrollment_status == "new user":
       pass 
    elif enrollment_status == "new user" :
        validation_result = validation_result.strip('"') + "\nGo to the website https://qa-enroll.corenroll.com/ to enroll in a plan."
    #save chat history 
    add_collection(category,{
        "question": question,
        "answer": validation_result,
        "created_at": datetime.utcnow()}
    )
    
    formatted_prompt = get_formatting_prompt(validation_result)
    formatted_result = run_chat_others(formatted_prompt)
    
    return formatted_result 

# print(chatbot("how to login as an agent?", "Login"))
# print(chatbot("And as a user?", "login"))
