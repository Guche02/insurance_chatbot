from langchain_groq import ChatGroq  # type: ignore
import httpx
import os
from dotenv import load_dotenv  # type: ignore
import google.generativeai as genai

genai.configure(api_key="AIzaSyBjKMLKyAyP-YPZttNPvgt1rooXpC4fQY8")
model = genai.GenerativeModel("gemini-1.5-flash")

load_dotenv()

def gemi(prompt):

  response = model.generate_content(prompt)
  return response.text

llm_login = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_retries=3,
)

llm_others = ChatGroq(
    model="llama-3.1-3b-preview",
    temperature=0.3,
    max_retries=3,
)

def run_chat_login(prompt):
    try:
        response = llm_login.invoke(prompt)
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
   
def run_enrollment_chat(prompt):
    try:
        response = gemi(prompt)
        # if hasattr(response, 'content'):
        #     return response.content  
        
        # return f"Error: Unexpected response format. Response did not contain 'content'."
        return response
        
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
    
     
    
def run_chat_others(prompt):
    try:
        response = gemi(prompt)
        # if hasattr(response, 'content'):
        #     return response.content  
        
        # return f"Error: Unexpected response format. Response did not contain 'content'."
        return response
        
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
    
    