import os
import dotenv  # type: ignore
import httpx
from mistralai import Mistral
from langchain_groq import ChatGroq  # type: ignore

dotenv.load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
model_mistral = "ministral-3b-latest"

llm_enrollment = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_retries=3,
)

llm_others = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_retries=3,
)

def llm_login(prompt):
    """Handles login-related chat using Mistral-3B."""
    try:
        client_mistral = Mistral(api_key=api_key)
        response = client_mistral.chat.complete(
            model=model_mistral,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except httpx.HTTPStatusError as e:
        return handle_http_error(e)

    except Exception as e:
        return f"Error: {str(e)}"


def run_chat_groq(prompt, llm_instance):
    """Handles chat using Groq models (for enrollment and others)."""
    try:
        response = llm_instance.invoke(prompt)
        if hasattr(response, 'content'):
            return response.content  
        
        return "Error: Unexpected response format. Response did not contain 'content'."

    except httpx.HTTPStatusError as e:
        return handle_http_error(e)

    except Exception as e:
        return f"Error: {str(e)}"


def handle_http_error(e):
    """Handles HTTP errors and provides user-friendly messages."""
    try:
        error_json = e.response.json()  
        error_message = error_json.get("message", "Unknown error")

        if e.response.status_code == 429:
            return "Error: Requests rate limit exceeded. Please try again later."

        if "too large for model" in error_message:
            return "Error: Input too large. Please break down your request."

        return f"Error: {e.response.status_code} - {error_message}"

    except Exception:
        return f"Error: {e.response.status_code} - {e.response.text}"


def run_chat_login(prompt):
    return run_chat_groq(prompt, llm_enrollment)   # Uses Mistral-3B

def run_enrollment_chat(prompt):
    return run_chat_groq(prompt, llm_enrollment) 

def run_chat_others(prompt):
    return run_chat_groq(prompt, llm_others)  # Uses Llama-3.1-8B

