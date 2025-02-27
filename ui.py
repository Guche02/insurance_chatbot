import streamlit as st
from chat_bot import chatbot

def main():

    """
    Main function contains all the UI parts of the application
    """
    st.set_page_config(page_title="Chat", layout="wide")
    st.title("💬Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message, str):
                st.write(message)
                
    user_input = st.chat_input("Type your message...")

    # Process user input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show the message in display
        with st.chat_message("user"):
            st.write(user_input)

        # Concatenate DataFrame if necessary
        input_data = user_input

        # Get output through pipeline
        bot_response = chatbot(input_data)

        # Append the output message of bot in the message history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # show bot output
        with st.chat_message("assistant"):
            if isinstance(bot_response, str):
                st.write(bot_response)

if __name__ == "__main__":
    main()
