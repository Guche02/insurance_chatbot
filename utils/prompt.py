from langchain.prompts import PromptTemplate  # type: ignore

def get_prompt_login(contexts: str, history: str, latest_chat: str, query: str) -> str:
    """
    The function returns formatted prompt to get answer to the user query.
    :param contexts: str
    :param history: str
    :param latest_chat: str
    :param query: str
    :return: str
    """
    prompt_template = PromptTemplate(
        input_variables=["contexts", "history", "latest_chat", "query"],
        template="""
        You are an expert in login systems, providing ***accurate and detailed*** answers based on the available information.

        Strictly follow these guidelines:
        - Use **Context (Knowledge Base)** as the primary source to answer **User Query**.
        - If the **User Query** cannot be answered using **Context**, refer to **History Summary**.
        - If the answer is still unclear, consider **Latest Chat** for additional context.
        - Do not use **History Summary** or **Latest Chat** if **Context** provides a complete answer. (!!!THIS IS IMPORTANT!!!)

        - provide a detailed and accurate asnwer based on above guidelines.
        - Do not generate any additional explanation.

        **Context (Knowledge Base - Primary Source):**
        {contexts}

        **History Summary (Secondary Source - Past Conversations Overview):**
        {history}

        **Latest Chat (Tertiary Source - Most Recent User Interaction):**
        {latest_chat}

        **User Query (Answer This Based on the Given Sources):**
        {query} 
        """
    )
    
    formatted_prompt = prompt_template.format(
        contexts=contexts, history=history, latest_chat=latest_chat, query=query
    )
    return formatted_prompt

def get_validation_prompt(response: str, query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["response", "query"],
        template=
        """  
        You are an AI assistant validating an insurance response that exactly follows the below instructions.

        - Check if the response is extremely irrelavant to the user query. Return **"Please contact the office or provide more details"**.
        - If the response is relevant, return the response provided itself.
        - Don't generate any additional explanations.
        
        **User Question:**  
        {query}  

        **Response Provided:**  
        {response}  
        """
    )

    formatted_prompt = prompt_template.format(query=query, response=response)
    print(f"Formatted Prompt: {formatted_prompt}")
    return prompt_template.format(response=response, query=query)


def get_query_category(query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query"],
        template=
        """
        You are an AI assistant categorizing user queries related to login and user accounts.
        
        - If the query is related to login, username, password, or account access, return **"login"**.
        - For all other queries, return **"others"**.
        - Don't generate any additional explanations.

        **User Query:**  
        {query}  
        """
    )
    
    formatted_prompt = prompt_template.format(query=query)
    print(f"Formatted Prompt: {formatted_prompt}")
    return prompt_template.format(query=query)

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

    formatted_prompt = prompt_template.format(data=data)

    return formatted_prompt