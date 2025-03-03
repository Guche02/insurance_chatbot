import streamlit as st  # type: ignore
from chat_bot import chatbot

def main():
    """
    Main function contains all the UI parts of the application
    """
    st.set_page_config(page_title="Chat", layout="wide")
    st.title("💬 Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    category = st.selectbox("Select a category:", ["Login", "Enrollment"])
    
    user_input = st.chat_input("Type your message...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": f"[{category}] {user_input}"})
        
        with st.chat_message("user"):
            st.write(f"[{category}] {user_input}")
        
        bot_response = chatbot(user_input, category)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        with st.chat_message("assistant"):
            st.write(bot_response)

if __name__ == "__main__":
    main()
