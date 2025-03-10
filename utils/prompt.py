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
        input_variables=["context", "query"],
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
        {query} 
        """
    )
    
    # formatted_prompt = prompt_template.format(
    #     contexts=contexts, latest_chat=latest_chat, query=query
    # )
    return prompt_template

def query_reformulation_prompt() :

    query_reformulation_prompt = PromptTemplate(
    input_variables=["memory", "question"],
    template="""
    You are an intelligent assistant that refines user queries to make them clear, coherent, and contextually relevant.
    
    **Instructions:**
    - Carefully analyze the previous conversation history.
    - Understand the intent behind the current query.
    - Reformulate the query in one sentence to make it more precise, removing ambiguities.
    - Ensure the reformulated query maintains the original meaning while making it clearer.
    - Don't generate any additional explanations other than the reformulated query.
    
    **Conversation History:**
    {memory}
    
    **User's Current Query:**
    {question}
    
    **Reformulated Query:**
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

def get_format_text_prompt(query: str, response:str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query","response"],
        template=
        """
          - You are an AI responsible for formatting text AI reponses following below guidelines also consider user's question when necessary:
          
          1. Make the reponse generalized without asumming the user's situation.
          2. If the user asks questions related to plan enrollment, return "\nGo to the website https://qa-enroll.corenroll.com/ to enroll in a plan.".
          3. If question want to report a issue or has a issue return "\nGo to the website https://qa-tickets.purenroll.com/ to report any issue.".
          4. Remove/Don't include extra text, such as “feel free to ask more questions”.
          5. Do not request additional information.
          6. Ensure responses feel natural and directly address the user's query.
          7. Do not offer explanations or generate additional content. ()
          
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

def get_formatting_prompt(response: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["response"],
        template=
        """
        Please revise the response and return a more professional and straignt to the point version. 
        - Ensure that the text size is normal and consistent.

        
        - Don't generate any additional explanations.
        
        {response}      
        """
    )
    formatted_prompt = prompt_template.format(response=response)
    return formatted_prompt

