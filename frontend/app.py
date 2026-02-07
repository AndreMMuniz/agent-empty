import streamlit as st
import uuid
import time
from api_client import APIClient

# Page Configuration
st.set_page_config(
    page_title="RAG Agent Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #f0f2f6;
        align-items: flex-end;
    }
    .chat-message.assistant {
        background-color: #e6f3ff;
        align-items: flex-start;
    }
    .source-doc {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
        padding: 0.5rem;
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()

# Sidebar
with st.sidebar:
    st.title("🤖 Agent Controls")
    
    # Connection Status
    if st.session_state.api_client.check_health():
        st.success("API Connected ✅")
    else:
        st.error("API Disconnected ❌")
        st.info("Make sure the backend is running on http://localhost:8000")
    
    st.divider()
    
    st.caption(f"Session ID: {st.session_state.thread_id}")
    
    if st.button("New Chat / Clear History"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# Main Chat Interface
st.title("📚 Knowledge Base Assistant")
st.markdown("Ask questions about your documents and get answers with citations.")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get Assistant Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Call API
            api_response = st.session_state.api_client.send_message(
                message=prompt,
                thread_id=st.session_state.thread_id
            )
            
            if "error" in api_response:
                response_text = f"❌ Error: {api_response.get('error')}"
            else:
                response_text = api_response.get("response", "No response received.")
                
            # Simulate streaming effect (optional polish)
            message_placeholder.markdown(response_text)
            
            # Store Assistant Message
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            message_placeholder.markdown(f"An error occurred: {str(e)}")
