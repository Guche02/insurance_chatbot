from utils.prompt import get_validation_prompt, get_query_category, get_prompt_enrollment, get_format_text_prompt,query_reformulation_prompt, get_formatting_and_validation_prompt
from utils.llm import run_chat_login, run_chat_others, run_enrollment_chat, llm_others, llm_login,llm_enrollment
from dotenv import load_dotenv 
from datetime import datetime
from utils.mongodb import  add_collection
from langchain.memory import ConversationTokenBufferMemory
from langchain.vectorstores import Chroma
import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain, LLMChain,StuffDocumentsChain

load_dotenv()
    
memory = ConversationTokenBufferMemory(
llm=llm_others,  
memory_key="chat_history",
return_messages=True,
max_token_limit=500 
)
    
embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="/app/insurance_new")
login_collection_db = Chroma(client=client, collection_name="knowledge_base", embedding_function=embedding_function)
enrollment_collection_db = Chroma(client=client, collection_name="knowledge_base", embedding_function=embedding_function)
#print(collection.count())

def chatbot(question):
    """Takes in user question and returns answer."""
    
    category = run_chat_others(get_query_category(question))

    if category == "login":
      response_function = run_chat_login
      vector_collection = login_collection_db
      llm_function = llm_login
      prompt_function = get_prompt_enrollment()
      
    elif category == "enrollment":
        response_function = run_enrollment_chat
        vector_collection = enrollment_collection_db
        llm_function = llm_enrollment
        prompt_function = get_prompt_enrollment()
        
    else:
        return "Error: Invalid category. Please provide a valid category."

    #chain
    
    #chain that takes the user question and main prompt function
    llm_chain = LLMChain(llm=llm_function, prompt=prompt_function)
    
    # StuffDocumentsChain to process the retrieved documents and the user question
    combine_docs_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context"  
    )
        
    question_generator_chain = LLMChain(llm=llm_function, prompt=query_reformulation_prompt())

    retriever = vector_collection.as_retriever(search_kwargs={"k": 3})
    
    # ConversationalRetrievalChain, combining everything
    chain = ConversationalRetrievalChain(
        combine_docs_chain=combine_docs_chain,
        retriever=retriever,
        question_generator=question_generator_chain,
        memory=memory  
    )
    
    memory_output = memory.load_memory_variables({})
    print("\n🔹 Memory Output:")
    print(memory_output)
    
    chat_list = []

    # Ensure there are at least two messages in chat history
    if len(memory_output['chat_history']) >= 2:
       human_message = memory_output['chat_history'][-2].content
       ai_message = memory_output['chat_history'][-1].content
    
       chat_list = [{
            'human': human_message,
            'ai': ai_message
        }]
    else:
        chat_list = []  # Handle case where there are fewer than two messages

    # Debug print the resulting list
    print("Last Two Chat Messages:", chat_list)

    generated_question = question_generator_chain.run({"question": question, "chat_history": chat_list})
    print("\n🔹 Generated Question:")
    print(generated_question)
    
    retrieved_docs = retriever.get_relevant_documents(generated_question)
    print("\n🔹 Retrieved Documents:")
    
    formatted_prompt = prompt_function.format(question=generated_question, context=retrieved_docs)
    response = response_function(formatted_prompt)

    
    print("Response:",response)

    # validation_prompt = get_validation_prompt(response, generated_question)
    # validation_result = run_chat_others(validation_prompt)
    # print("Validation result:",validation_result.strip(),"end")
    
    formatting_prompt = get_format_text_prompt(question,response)
    formatted_result = run_chat_others(formatting_prompt)
    print("Formatted result:",formatted_result.strip())
    
    # #check is user is enrolled
    # enrollment_status = run_chat_others(get_user_enrollment_status(question))

    # print("Enrollment status: ", enrollment_status)
    # if "I don't have enough information" in validation_result and enrollment_status == "new user":
    #    pass 
    # elif enrollment_status == "new user" :
    #     validation_result = validation_result.strip('"') + "\nGo to the website https://qa-enroll.corenroll.com/ to enroll in a plan."
    
    final_formatted = get_formatting_and_validation_prompt(formatted_result, generated_question)
    final = run_chat_others(final_formatted)
    print("Final result:",final.strip())
    
    memory.save_context({"input": question},{"output": final})
    
        #save chat history 
    add_collection(category,{
        "question": question,
        "answer": final,
        "created_at": datetime.utcnow()}
    )
    
    return final 

# print(chatbot("how to login as an agent?", "Login"))
# print(chatbot("And as a user?", "login"))