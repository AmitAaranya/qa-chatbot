import streamlit as st

from app import Chat
from dotenv import load_dotenv

load_dotenv()

def handle_csv_file(files, chat_client):
    for file in files:
        result = chat_client.process_file(file)
        st.session_state.messages.append({"role": "assistant", "content": result})
    st.rerun()


def main():
    st.title('QA Chatbot')
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_client" not in st.session_state:
        st.session_state.chat_client = Chat()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask your question...", accept_file=True, file_type=["csv"]):
        if isinstance(prompt, str):
            prompt_text = prompt
        else:
            prompt_text = prompt.get("text", None)
            prompt_files = prompt.get("files", None)

            if len(prompt_files) > 0:
                with st.status("Processing files..."):
                    handle_csv_file(files=prompt_files, chat_client=st.session_state.chat_client)
        with st.chat_message("user"):
            st.write(prompt_text)
    
        st.session_state.messages.append({"role": "user", "content": prompt_text})
        
        # Create a placeholder for the assistant's response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for response_chunk in st.session_state.chat_client(user_message=prompt_text):
                full_response += response_chunk
                # Update the placeholder with the accumulated response
                response_placeholder.markdown(full_response + "▌")
            
            # Final update without the cursor
            response_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
