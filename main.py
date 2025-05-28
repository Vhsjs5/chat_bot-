import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load environment variables
load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Set page config
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.assistant {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 AI Chatbot")
st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user">
                    <strong>You:</strong><br>{message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant">
                    <strong>Assistant:</strong><br>{message["content"]}
                </div>
            """, unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Type your message here...", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": m["role"], "content": m["content"]} 
            for m in st.session_state.messages
        ],
        model="llama-3.3-70b-versatile",
    )
    
    # Add assistant response to chat history
    assistant_response = chat_completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Rerun to update the chat display
    st.rerun()