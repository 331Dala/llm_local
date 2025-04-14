from openai import OpenAI
import streamlit as st
import urllib.request

# Create a client
client = OpenAI(api_key='asdasd123', base_url='http://localhost:8000/v1')

st.title('👽GPT Server App')
prompt = st.chat_input('Pass prompt here')
image_url = st.text_input('Enter image URL here').strip()

# Function to load image with headers
def load_image_with_headers(image_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://png.pngtree.com/'
    }
    req = urllib.request.Request(image_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

if prompt:
    # Display user input
    st.chat_message('user').markdown(prompt)  # 'user' for avatar

    # Create a chat completion
    response = client.chat.completions.create(
        model='mistral-function-calling',
        messages=[{'role': 'user', 'content': [{'type': 'image_url', 'image_url': image_url}, {'type': 'text', 'text': prompt}]}],
        stream=True
    )

    # Display AI response
    with st.chat_message('ai'):  # 'ai' for avatar
        complete_message = ""
        message = st.empty()
        for chunk in response:
            if chunk.choices[0].delta.content:  # Ensure content is not None
                complete_message += chunk.choices[0].delta.content
                message.markdown(complete_message)

# Optional: Test image loading
if image_url:
    image_data = load_image_with_headers(image_url)
    if image_data:
        st.image(image_data, caption="Loaded Image")
        
#search below
# https://png.pngtree.com/png-vector/20221228/ourlarge/pngtree-trading-candlestick-pattern-in-red-and-green-colors-png-image_6536057.png
# describe the image provided

# this will start a local server with chat format 'functionary' or 'chatml' or '...' and run the model on the server
# run this file open a PS terminal and run the command: 
# python -m llama_cpp.server --model models\llava-v1.5-7b-Q4_K.gguf --clip_model_path .\models\llava-v1.5-7b-mmproj-Q4_0.gguf --chat llava-1-5
# then run streamlit app in another PS terminal with: streamlit run multimodal_llava_05.py

# 502 Error - Bad Gateway solution see README.md
# try command: $env:NO_PROXY = "localhost,127.0.0.1" 
# may caused by the proxy settings in the system, if you are using a proxy server
# , you may need to configure your proxy settings to allow access to the local server.




# Code original**********************************

# from openai import OpenAI

# # The app framework, Streamlit, is used to create the web app
# import streamlit as st

# # Create a client
# client = OpenAI(api_key = 'asdasd123', base_url = 'http://localhost:8000/v1')


# st.title('👽GPT Server App')
# prompt = st.chat_input('Pass prompt here')

# image_url = st.text_input('Enter image URL here')

# # Function calling LLM call
# if prompt:
#     st.chat_message('user').markdown(prompt) # 'user' for avatar
#     # Create a chat completion
#     response = client.chat.completions.create(
#         # which model to use
#         model = 'mistral-function-calling',
#         # messages to send to the model aka prompt
#         messages = [{'role': 'user', 'content': [{'type': 'image_url', 'image_url': image_url}, {'type': 'text', 'text': prompt}]}], 
#         # Add a stream
#         stream=True
#     )

#     st.chat_message('ai').markdown(response)

#     with st.chat_message('ai'): # 'ai' for avatar
#         complete_message = ""
#         message = st.empty()
#         # Streaming the response out
#         for chunk in response:
#             if chunk.choices[0].delta.content is not None:
#                 # Print the content of the chunk
#                 # flush=True will force the output to be printed immediately
#                 # end='' will prevent a new line after each print
#                 complete_message += chunk.choices[0].delta.content
#                 message.markdown(complete_message)


