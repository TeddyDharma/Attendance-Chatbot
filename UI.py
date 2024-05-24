# documentation : https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/
import streamlit as st
from main import * 
# App title
st.set_page_config(page_title="🤗💬 Sanata Chat")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hai selamat datang di Sanata Chat"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input):
    #
    model, tokenizer = load_model_and_tokenizer("./bot_model.h5")
    pred = predict_class(str(prompt_input), tokenizer, model)

    return pred

# User-provided prompt
if prompt := st.chat_input("ketik pesan mu disini ya!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)