import streamlit as st

from app import chat


def main():
    st.title('QA Chatbot')
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask your question..."):
        with st.chat_message("user"):
            st.write(prompt)
    
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = chat(prompt)
        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
