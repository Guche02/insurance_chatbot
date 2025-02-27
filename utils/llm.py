from langchain_groq import ChatGroq
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.0,
    max_retries=2,
)


def run_chat(prompt):
    try:
        response = llm.invoke(prompt)
        
        if hasattr(response, 'content'):
            return response.content  
        
        return f"Error: Unexpected response format. Response did not contain 'content'."
        
    except httpx.HTTPStatusError as e:
        try:
            error_json = e.response.json()  
            error_message = error_json.get("message", "Unknown error")

            if e.response.status_code == 429:
                return "Error: Requests rate limit exceeded. Please try again later."

            if "too large for model" in error_message:
                return "Error: Requests rate limit exceeded. Please try again later, break down the input."

            return f"Error: {e.response.status_code} - {error_message}"

        except Exception:
            return f"Error: {e.response.status_code} - {e.response.text}"

    
    except Exception as e:
        return f"Error: {str(e)}"
