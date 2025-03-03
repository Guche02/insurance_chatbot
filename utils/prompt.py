from langchain.prompts import PromptTemplate  # type: ignore

def get_prompt(contexts: str, query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query", "contexts"],
        template=
        """"
    You are an insurance assistant. Answer based on the given sample responses and knowledge.).  

   - If the context exactly matches the question, provide a precise answer.  
   - If the context is too specific, give a general answer.  

    **Knowledge**  
    {contexts}  

    **User Question:**  
    {query}  
       """
    )

    formatted_prompt = prompt_template.format(query=query, contexts=contexts)
    print(f"Formatted Prompt: {formatted_prompt}")
    return formatted_prompt

def get_validation_prompt(response: str, query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["response", "query"],
        template=
        """  
        You are an AI assistant validating an insurance response that exactly follows the below instructions.

        - Check if the response is extremely irrelavant to the user query. Return **"Please contact the office or provide more details"**.
        - If the response is relevant, return the response provided itsel.
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
