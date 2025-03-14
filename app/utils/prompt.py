from langchain.prompts import PromptTemplate  # type: ignore

def get_prompt_login() : 
    """
    The function returns a formatted prompt to generate a polite and human-like response.
    :param contexts: str
    :param history: str
    :param latest_chat: str
    :param query: str
    :return: str
    """
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=
        """
        You are a friendly and knowledgeable expert in login systems. You communicate **politely, like a helpful human**, ensuring clarity and warmth in your responses.

        **Guidelines for Your Response:**
        - Provide a **clear and general answer** using the **Context (Knowledge Base)** as the primary source.
        - If the **User Query** cannot be fully answered using **Context**, refer to **past conversations** for additional details.
        - If needed, use **Latest Chat** to provide further clarification.
        - Keep responses **concise, helpful, and human-like** while maintaining accuracy.
        - End with a polite closing (e.g., "Let me know if you need more help!").

        **Context (Knowledge Base - Primary Source):**
        {context}


        **User Query:**
        {question} 
        """
    )
    
    # formatted_prompt = prompt_template.format(
    #     contexts=contexts, latest_chat=latest_chat, query=query
    # )
    return prompt_template

def query_reformulation_prompt(): 

    query_reformulation_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""
    You are an intelligent assistant that refines user queries only when necessary to make them clearer and contextually relevant.
    
    **Instructions:**
    - Carefully analyze the previous conversation history.
    - Maintain the original wording of the user's query.
    - Add only a few words if necessary to clarify meaning based on context.
    - If the original query is already clear, leave it unchanged.
    - Do not alter the intent or structure of the original question.
    - Provide only the final query without additional explanations.

    **Examples:**
    - If the user asks: "How to login?" → Keep it as "How to login?"
    - If the user asks: "How to reset my password?" → Keep it as "How to reset my password?"
    - If the latest chat history is: "How to reset my password?" and the next query is: "As an agent?" → Reformulate it as "How to reset my password as an agent?"
    - If the previous chat history is: "How to reset my password?" and the next query is: "As an  group agent?" → Reformulate it as "How to reset my password as a group agent?"
    - If the lastest chat history is: "How to login?" and the next query is: "As an agent?" → Reformulate it as "How to login as an agent?"
    - If the previous chat history is: "How to reset my username?" and the next query is: "As an  agent?" → Reformulate it as "How to reset my username as an agent?"
    - If the previous chat history is: "How to reset my username?" and the next query is: "what about my password?" → Reformulate it as "How to reset my password?"

    **Conversation History:**
    {chat_history}
    
    **User's Current Query:**
    {question}
    
    **Final Query:**
    """
)
    return query_reformulation_prompt

def get_prompt_enrollment() :
    """
    Generates a structured prompt to ensure the model provides a natural, context-aware response 
    without directly referencing source material.
    :param contexts: str - Primary knowledge base information.
    :param history: str - Summary of past interactions.
    :param latest_chat: str - Most recent user interaction.
    :param query: str - User's current query.
    :return: str - Formatted prompt for generating a response.
    """
    prompt_template = PromptTemplate(
        input_variables=["context",  "question"],
        template=
        """
            ### SYSTEM MESSAGE  
            You are an  part of insurance company working as an **insurance enrollment expert**, and your task is to **answer the user's query in USER QUERY heading** in a **clear and natural manner**. 

            **IMPORTANT:**
            - **Do NOT** reference the source text (Context, History, or Latest Chat) directly in your response.
            - **Do NOT quote or copy-paste** content from the provided information.
            - **DO NOT say "Based on the Context" or similar phrases**.
            - Integrate the relevant information into a **natural, fluent response** without explicitly calling out where it came from.
            - Ensure that your response **does not repeat verbatim** the language in the source material.
            - **USE LATEST CHAT OR HISTORY ONLY IF USER QUERY IS UNCLEAR**.
            - Don't generate any additional explanations other than the response.

            BACKGROUND INFORMATION (Use this to answer the USER QUERY):
            {context}

            USER QUERY:
            {question}

            RESPONSE:
            (Provide a concise, clear response. Integrate information without repeating source text or referring to the context explicitly.)
        """
    )

    return prompt_template

def get_validation_prompt(response: str, query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["response", "question"],
        template=
    """  
        You are an AI assistant responsible for validating and formatting an insurance response according to the following instructions:

        1. If the response is completely irrelevant to the user’s query, return: "I don't have enough information on that. Please contact the office or provide more details."
        2. Strictly don't generate any extra texs.

        **User Question:**  
        {question}

        **Response Provided:**  
        {response}
 
    """
    )

    formatted_prompt = prompt_template.format(question=query, response=response)
    print(f"Formatted Prompt: {formatted_prompt}")
    return formatted_prompt

def get_query_category(query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query"],
        template=
        """
        You are an AI assistant categorizing user queries related to login and user accounts.
        
        - If the query is related to login, username, password, or account access, return **"login"**.
        - For all other queries, return **"enrollment"**.
        - Don't generate any additional explanations.

        **User Query:**  
        {query}  
        """
    )
    
    formatted_prompt = prompt_template.format(query=query)
    print(f"Formatted Prompt: {formatted_prompt}")
    return formatted_prompt

def get_summarize_prompt(data):
    
    """Takes in conversation history data and returns a formatted prompt."""

    prompt_template = PromptTemplate(
        input_variables=["data"],
        template="""
        You are an AI assistant that **summarizes** the given **conversation data**.
        Optimize the summary so that it provides sufficient context for an LLM about the chat history.
        Limit the summary to 1000 characters to ensure it is concise and informative.
        If **Conversation Data** is **Empty** return "History Empty".

        **Conversation Data:**
        {data}
        """
    )

    formatted_prompt = prompt_template
    return formatted_prompt

def get_format_text_prompt(query: str, response: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query", "response"],
        template=
        """
        - You are an AI responsible for formatting text AI responses following the guidelines below. Also, consider the user's question when necessary:

        1. Make the response generalized without assuming the user's situation.  
        2. If the user asks questions related to plan enrollment, return:  
           "\nGo to the website https://qa-enroll.corenroll.com/ to enroll in a plan.".  
        3. If the user wants to report an issue or has an issue, return:  
           "\nGo to the website https://qa-tickets.purenroll.com/ to report any issue.".  
        4. Remove/Don't include extra text, such as “feel free to ask more questions.”  
        5. Do not request additional information.  
        6. Ensure responses feel natural and directly address the user's query.  
        7. Do not offer explanations or generate additional content. 
        8. If the user wants to login or view the dashboard, without specifying the type of user, returns all the dashboard ***links***.
        9. If the user specifies a particular dashboard or login, return ONLY the relevant dashboard ***links***.

        ***Links***: 
           - **Member Dashboard**: "\nGo to the website https://qa-dashboard.purenroll.com to log in to your account."  
           - **Group/Employer Dashboard**: "\nGo to the website https://group.corenroll.com to log in to your account."  
           - **Representative Dashboard**: "\nGo to the website https://reps.purenroll.com/ to log in to your representative account."  

        ***Examples***:

        - If the user asks: "How do I log in?" Return:  
          "\nGo to the website https://qa-dashboard.purenroll.com to log in to into your member account."  
          "\nGo to the website https://group.corenroll.com to log in to your group account."  
          "\nGo to the website https://reps.purenroll.com/ to log in to your representative account."  

        - If the user asks: "How do I log in as a representative?" Return:  
          "\nGo to the website https://reps.purenroll.com/ to log in to your representative account."

        - If the user asks: "How do I log in as a group/employer?" Return:  
          "\nGo to the website https://group.corenroll.com to log in to your group/employer account."

        **User Query:**  
        {query}  

        **AI Response:**  
        {response}  
        """
    )

    formatted_prompt = prompt_template.format(query=query, response=response)
    return formatted_prompt

def get_user_enrollment_status(query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query"],
        template=
        """
        You are an AI assistant determining whether a user is enrolled in an insurance plan based on their query.
        Classify the user into one of the following categories:
        
        - **enrolled** → If the query suggests the user already has an insurance plan.
        - **new user** → If the query suggests the user is not yet enrolled or is seeking enrollment information.

        Respond only with **"enrolled"** or **"new user"** without any additional explanation.

        **Examples:**
        - "How do I change my password?" → **enrolled**
        - "How do I enroll?" → **new user**
        - "How do I change my plan?" → **enrolled**
        - "What plans are available?" → **new user**
        - "How do I cancel my plan?" → **enrolled**
        - "What different enrollment plans are available?" → **new user**

        **User Query:** {query}  
        **Response:** 
        """
    )
    formatted_prompt = prompt_template.format(query=query)
    return formatted_prompt

def get_formatting_and_validation_prompt(response: str, query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["response", "query"],
        template=
        """
        Please revise the response and return a more professional version.
        - Ensure that the answer is relevant to the question.
        - If the answer is relevant, return the SAME response.
        - Otherwise, generate a more relevant response using the given query and response.
        - If you don't have enough information return "I don't have enough information on that. Please contact the office or provide more details."

        - STRICTLY ***Don't generate any additional explanations.***

        {query}
        
        {response}      
        """
    )
    formatted_prompt = prompt_template.format(response=response, query=query)
    return formatted_prompt