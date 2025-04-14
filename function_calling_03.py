from openai import OpenAI

# The app framework, Streamlit, is used to create the web app
import streamlit as st

# model function calling framework
# instructor library allows us build a response model effectively extract the values we need from prompts.
import instructor
# Bring in the Base model class
from pydantic import BaseModel
# Bring in the stock price function
from stock_data import get_stock_prices

# Create a client
client = OpenAI(api_key = 'asdasd123', base_url = 'http://localhost:8000/v1')
# Create a patched client
client = instructor.patch(client=client)

# Structure what want extracted from the prompt
class ResponseModel(BaseModel):
    ticker: str
    days: int


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
        # stream=True
        response_model=ResponseModel,
    )

    st.chat_message('ai').markdown(response)

    try:
        prices = get_stock_prices(response.ticker, response.days)
        st.chat_message('ai').markdown(prices)
    except Exception as e:
        st.chat_message('ai').markdown('Something went wrong😣')

# summarise the stock price movements for AAPL for the last 7 days
    
# this will start a local server with chat format 'functionary' or chatml and run the model on the server
# run this file open a PS terminal and run the command: 
# python -m llama_cpp.server --model models/mistral-7b-instruct-v0.1.Q4_0.gguf --chat functionary
# then run streamlit app in another PS terminal with: streamlit run function_calling_03.py

# 502 Error - Bad Gateway solution see README.md
# try command: $env:NO_PROXY = "localhost,127.0.0.1" 
# may caused by the proxy settings in the system, if you are using a proxy server
# , you may need to configure your proxy settings to allow access to the local server.