import streamlit as st  # type: ignore
from chat_bot import chatbot

def main():
    """
    Main function contains all the UI parts of the application
    """
    st.set_page_config(page_title="Chat", layout="wide")
    st.title("💬 Chat")

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Login"

    category = st.selectbox("Select a category:", ["Login", "Enrollment"], index=["Login", "Enrollment"].index(st.session_state.selected_category))

    if "messages" not in st.session_state:
        st.session_state.messages = {"Login": [], "Enrollment": []}

    if category != st.session_state.selected_category:
        st.session_state.selected_category = category

    for message in st.session_state.messages[category]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages[category].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        bot_response = chatbot(user_input, category)

        st.session_state.messages[category].append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.write(bot_response)

if __name__ == "__main__":
    main()
