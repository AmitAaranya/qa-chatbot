import streamlit as st

from app import Chat
from dotenv import load_dotenv

load_dotenv()


def main():
    st.title('QA Chatbot')
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_client" not in st.session_state:
        st.session_state.chat_client = Chat()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask your question..."):
        with st.chat_message("user"):
            st.write(prompt)
    
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Create a placeholder for the assistant's response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for response_chunk in st.session_state.chat_client(user_message=prompt):
                full_response += response_chunk
                # Update the placeholder with the accumulated response
                response_placeholder.markdown(full_response + "▌")
            
            # Final update without the cursor
            response_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
