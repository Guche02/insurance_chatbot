from datetime import datetime
import streamlit as st   # type: ignore
from chat_bot import chatbot

def main():
    """
    Main function contains all the UI parts of the application
    """
    st.set_page_config(page_title="Chat", layout="wide")
    st.title("💬 Chat")

    #chat toggle
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            st.caption(f'{message["timestamp"].strftime("%Y-%m-%d %H:%M:%S")}')

    #get user input
    user_input = st.chat_input("Type your message...")

    if user_input:
        timestamp = datetime.utcnow()

        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })

        with st.chat_message("user"):
            st.write(user_input)
            st.caption(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}')
            
        if st.session_state.messages:
            oldest_timestamp = st.session_state.messages[0]["timestamp"]
        else:
            oldest_timestamp = datetime.utcnow() 

        bot_response = chatbot(user_input,oldest_timestamp)

        timestamp = datetime.utcnow()

        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response,
            "timestamp": timestamp
        })  

        with st.chat_message("assistant"):
            st.write(bot_response)
            st.caption(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}')

if __name__ == "__main__":
    main()
