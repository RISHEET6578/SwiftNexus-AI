import streamlit as st
import requests

# 1. Page Configuration & Styling
st.set_page_config(page_title="SwiftDelivery AI Support", page_icon="🤖", layout="centered")

st.title("🤖 SwiftDelivery Customer Support")
st.markdown("---")

# 2. Initialize Chat History in Session State
# This keeps the chat on the screen even when the app re-runs
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle New User Input
if user_query := st.chat_input("How can I help you with your delivery today?"):
    
    # Display user message instantly in the UI
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Display a loading spinner while the multi-agent crew works
    with st.chat_message("assistant"):
        with st.spinner("🤖 System is analyzing policy and verifying response..."):
            try:
                # 1. Define the base URL accurately
                FASTAPI_URL = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")
                
                # 2. Append the exact route your FastAPI uses (e.g., /api/chat)
                full_url = f"{FASTAPI_URL.strip('/')}/api/chat"
                
                payload = {"customer_query": user_query}
                
                # 3. Use the corrected variable name here!
                response = requests.post(full_url, json=payload)
                
                if response.status_code == 200:
                    # Extract the final answer from the JSON response
                    api_data = response.json()
                    final_answer = api_data.get("response", "No response received.")
                    
                    # Render the answer in the UI
                    st.markdown(final_answer)
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                else:
                    st.error(f"Backend Error: Received status code {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend API. Is your FastAPI server running?")
