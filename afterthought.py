import pandas as pd
import streamlit as st
from transformers import pipeline

# Load sentiment transformation model
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="t5-small")

model = load_model()

# Function to transform message tone
def transform_message(message, tone):
    prompt = f"Rewrite this message in a {tone} tone: {message}"
    result = model(prompt, max_length=50, num_return_sequences=1)
    return result[0]["generated_text"]

# App UI
st.title("Afterthought: Memory, Emotion, and Shifting Chats")

# Upload CSV
uploaded_file = st.file_uploader("Upload your chat history (CSV format)", type="csv")

if uploaded_file:
    # Load messages
    df = pd.read_csv(uploaded_file)
    st.write("Chat history loaded:")
    st.dataframe(df.head())

    # Select tone
    tone = st.selectbox("Set the emotional tone for your messages:", ["cheerful", "angry", "sad", "neutral", "nostalgic"])

    # Navigation through messages
    current_index = st.session_state.get("current_index", 0)
    if st.button("Next Message"):
        current_index += 1
        if current_index >= len(df):
            current_index = 0  # Loop back to the beginning
        st.session_state["current_index"] = current_index

    # Display current message
    if "current_index" in st.session_state:
        row = df.iloc[current_index]
        original_message = row["message"]
        transformed_message = transform_message(original_message, tone)

        st.write(f"**Sender:** {row['sender']}")
        st.write(f"**Timestamp:** {row['timestamp']}")
        st.write("### Original Message")
        st.write(original_message)
        st.write("### Transformed Message")
        st.write(transformed_message)
