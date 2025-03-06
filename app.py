import streamlit as st
from PIL import Image
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.markdown(f"**🧑‍💻 User:** {message.content}")
        else:
            st.markdown(f"**🤖 Reply:** {message.content}")

def main():
    st.set_page_config(page_title="RetrieveX", page_icon="💀", layout="wide")
    
    # Custom CSS for styling
    st.markdown(
        """
        <style>
            .stTextInput, .stButton, .stFileUploader {
                text-align: center;
                border-radius: 10px;
            }
            .stTextInput > div > div > input {
                font-size: 16px;
                padding: 10px;
            }
            .stButton > button {
                background-color: #4CAF50 !important;
                color: white !important;
                font-weight: bold;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Header Section
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>RetrieveX 💀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:18px;'>Ask questions from your uploaded files!</p>", unsafe_allow_html=True)
    
    # User Question Input
    user_question = st.text_input("📌 Ask a Question", placeholder="Type your question here...")
    
    # Session State Initialization
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    if user_question:
        user_input(user_question)
    
    # Sidebar Menu
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📂 Menu</h2>", unsafe_allow_html=True)
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        
        if st.button("📥 Submit & Process"):
            with st.spinner("🚀 Processing your files..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success("✅ Done! You can now ask questions.")
    
    # Footer
    st.markdown("""
    <hr>
    <p style='text-align: center; font-size:14px;'>Built with ❤️ </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
