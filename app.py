import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

st.title("Groq Chatbot with LLaMA 3")

# User input
user_input = st.text_input("Ask something:", placeholder="e.g. Explain the importance of fast language models")

# Submit button
if st.button("Submit") and user_input:
    with st.spinner("Generating response..."):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )

            response = chat_completion.choices[0].message.content
            st.success("Response:")
            st.markdown(response)

        except Exception as e:
            st.error(f"Error: {str(e)}")
