import streamlit as st
import torch
# print(torch.cuda.is_available())
from transformers import T5Tokenizer, T5ForConditionalGeneration




# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the model on the appropriate device (GPU or CPU)


# Set page config
st.set_page_config(page_title="Legal Advisor AI", layout="wide")

# Custom styles
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .block-container {
            max-width: 1000px;
            margin: auto;
        }
        .header {
            text-align: center;
            padding: 20px;
            background: primaryColor;
            color: white;
            border-radius: 10px;
        }
        .stButton > button {
            background-color: white !important;
            color: black !important;
            border: none;
            padding: 10px;
            border-radius: 50%;
            font-size: 16px;
            width: 40px;
            height: 40px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #f0f0f0 !important;
        }
        .chat-bubble {
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
            max-width: 80%;
            color: #121212;
        }
        .user-bubble {
                background-color: #555555; /* Grey background */
            color: white;              /* White text */
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            max-width: 75%; /* Adjust width based on content */
            align-self: flex-end; /* Align the bubble to the extreme right */
            word-wrap: break-word; /* Ensure text wraps correctly */
            display: inline-block;
        }
        .assistant-bubble {
            color : white;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'><h1>Legal Advisor AI</h1></div>", unsafe_allow_html=True)


#model load
def load_model():
    tokenizer = T5Tokenizer.from_pretrained('./model')
    model = T5ForConditionalGeneration.from_pretrained('./model')
    return tokenizer, model
device = torch.device('cpu')
t5_tokenizer, t5_model = load_model()

t5_model = t5_model.to(device)


def generate_t5_response(query):
    input_text = f"question: {query}"
    inputs = t5_tokenizer(input_text, return_tensors="pt", truncation=True, padding=True).to(device)
    outputs = t5_model.generate(
        inputs["input_ids"],
        max_length=150,
        num_beams=5,
        early_stopping=True,
        no_repeat_ngram_size=2,  # Prevent repetition
        temperature=1.0,  # Control randomness (set to 1 for no change)
        top_p=1.0,  # Controls nucleus sampling, if used
        top_k=50
    )
    return t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
# Conversation area
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input and button in the same row using columns
col1, col2 = st.columns([9, 1])  # Adjust column ratios for width

with col1:
    query = st.text_input(
        "",
        placeholder="Ask your legal question related to Indian Penal Code...",
        label_visibility="collapsed",
        key="query_input",
    )

with col2:
    submit_button = st.button("➤", help="Submit your query")

# Handle button click
if submit_button and query:
    # Store user query
    st.session_state.messages.append({"role": "user", "content": query})
    try:
        response = generate_t5_response(query)
    except Exception as e:
        response = f"An error occurred while generating the response: {str(e)}"
    
    # Store assistant's response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Example response (replace with model logic)
#     response = '''The punishment for theft under Section 378 of the Indian Penal Code (IPC) is specified in Section 379. It states:

# "Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with a fine, or with both."'''

# Display conversation
for msg in st.session_state.messages:
    role = msg["role"]
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    st.markdown(f"<div class='chat-bubble {bubble_class}'>{msg['content']}</div>", unsafe_allow_html=True)
