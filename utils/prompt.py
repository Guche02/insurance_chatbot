
from langchain.prompts import PromptTemplate

def get_prompt(contexts: str, query: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["query", "contexts"],
        template=
        
        """
        You are a knowledgeable assistant specialized in an insurance system, providing detailed and accurate answers based on the given context.
        - Use **all** the provided context to answer the user's question **without being repetative**. Ensure you reference relevant parts of the context.
        - If the question cannot be answered using the given information, respond with: **"I don't have that information."**
        - Provide a comprehensive answer that includes all necessary details to fully address the user's question.

        **Context:**  
        {contexts}  

        **User Question:**  
        {query}  

        """
    )
    formatted_prompt = prompt_template.format(query=query, contexts=contexts)
    print(f"Formatted Prompt: {formatted_prompt}")
    return formatted_prompt
    