import streamlit as st
import requests
import os

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode and chat bubbles
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #2B313E;
        margin-left: 20%;
        border-left: 3px solid #4CAF50;
    }
    .assistant-message {
        background-color: #1E2530;
        margin-right: 20%;
        border-left: 3px solid #2196F3;
    }
    .message-content {
        color: #FAFAFA;
        font-size: 1rem;
        line-height: 1.5;
    }
    .message-label {
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .user-label {
        color: #4CAF50;
    }
    .assistant-label {
        color: #2196F3;
    }
    div[data-testid="stExpander"] {
        background-color: #1E2530;
        border: 1px solid #2B313E;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🤖 RAG Chatbot")
    st.markdown("""
    ### About
    This is an AI-powered chatbot using:
    - **Groq LLM** for natural language understanding
    - **FastAPI** backend for processing
    - **Streamlit** for the user interface
    
    Ask any question and get informed answers with sources!
    """)
    
    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Powered by Groq & FastAPI")

# Main chat interface
st.title("💬 Chat with AI Assistant")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-label user-label">👤 You</div>
            <div class="message-content">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <div class="message-label assistant-label">🤖 Assistant</div>
            <div class="message-content">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show sources if available
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources / References"):
                for idx, source in enumerate(message["sources"], 1):
                    st.markdown(f"**{idx}.** {source['document']} (Page {source['page']})")

# Chat input (fixed at bottom)
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message immediately
    st.markdown(f"""
    <div class="chat-message user-message">
        <div class="message-label user-label">👤 You</div>
        <div class="message-content">{user_input}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show loading spinner
    with st.spinner("🤔 Thinking..."):
        try:
            # Send request to backend
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"question": user_input},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No response received.")
                sources = data.get("sources", [])
                
                # Add assistant message to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                
                # Rerun to display the new message
                st.rerun()
            else:
                st.error(f"Error: Backend returned status code {response.status_code}")
                st.error(f"Details: {response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Please make sure the FastAPI server is running on port 8000.")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
