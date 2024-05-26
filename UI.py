import streamlit as st
from main import * 
import random 
import datetime 

st.set_page_config(page_title="🤗💬 Sanata Chat")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hai selamat datang di Sanata Chat"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

data  = read_json() 
# Function for generating LLM response
def generate_response(prompt_input):
    respons = "maaf saya tidak mengerti perintah anda"
    model, tokenizer = load_model_and_tokenizer("./bot_model.h5")
    pred = predict_class(str(prompt_input), tokenizer, model)
    classes = ['general', 'goodbye', 'greeting', 'izin', 'sakit']
   
    for i in range(len(data['intents'])):
        if data['intents'][i]['tag'] == classes[pred]: 
            index_res = random.randint(0, 2)
            respons = data['intents'][i]['responses'][index_res]  
    attendance_type = classes[pred]
    return respons, attendance_type




# User-provided prompt
if prompt := st.chat_input("ketik pesan mu disini ya, pastikan di pesan yang anda ketik berisikan nama anda"):
    pegawai_name = ""

    data_pegawai = get_data_pegawai()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    split_data = str(prompt).lower().split(" ")
    
    for word in split_data[:-1]: 
        for id,  name in  zip(data_pegawai.loc[:,'id'], data_pegawai.loc[:, 'name']): 
            if word in str(name).lower(): 
                print(f'naame : {name} dan word : {word}')
                pegawai_name = name
                id_pegawai  = id 
            
    


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response, attendance_type = generate_response(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
    

    for prompt_word in str(prompt).split(" ")[:-1]:
        if prompt_word not in [x.lower() for x in data['intents'][0]['input'] ]:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            insert_absensi(id_pegawai, date, pegawai_name, prompt, attendance_type) 
            break

