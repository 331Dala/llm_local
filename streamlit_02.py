from openai import OpenAI

# The app framework, Streamlit, is used to create the web app
import streamlit as st

# Create a client instance
client = OpenAI(
	api_key='asdasd123', 
	base_url='http://localhost:8000/v1'
)

st.title('👽GPT Server App')
prompt = st.chat_input('Pass prompt here')

if prompt:
    st.chat_message('user').markdown(prompt) # 'user' for avatar
    # Create a chat completion
    response = client.chat.completions.create(
        # which model to use
        model = 'D:\ml_workspace\llm_local\models\mistral-7b-instruct-v0.1.Q4_0.gguf',
        # messages to send to the model aka prompt
        messages = [{'role': 'user', 'content': prompt}], 
        # Add a stream
        stream=True
    )
    with st.chat_message('ai'): # 'ai' for avatar
        complete_message = ""
        message = st.empty()
        # Streaming the response out
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                # Print the content of the chunk
                # flush=True will force the output to be printed immediately
                # end='' will prevent a new line after each print
                complete_message += chunk.choices[0].delta.content
                message.markdown(complete_message)

# run this file open a PS terminal and run the command: python -m llama_cpp.server --model models/mistral-7b-instruct-v0.1.Q4_0.gguf
# then run streamlit app in another PS terminal with: streamlit run streamlit_02.py
# this will start a local server and run the model on the server

# 502 Error - Bad Gateway solution see README.md
# try command: $env:NO_PROXY = "localhost,127.0.0.1" 
# may caused by the proxy settings in the system, if you are using a proxy server, you may need to configure your proxy settings to allow access to the local server.