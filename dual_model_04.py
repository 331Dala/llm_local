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

# Function calling LLM call
if prompt:
    st.chat_message('user').markdown(prompt) # 'user' for avatar
    # Create a chat completion
    response = client.chat.completions.create(
        # which model to use
        model = 'mistral-function-calling',
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

        # Summary output prompt + prices
        fullresponse = client.chat.completions.create(
            # which model to use
            model = 'mixtral',
            # messages to send to the model aka prompt
            messages = [{'role': 'user', 'content': prompt +'\n' + str(prices)}], 
            # Add a stream
            stream=True
        )
        with st.chat_message('ai'): # 'ai' for avatar
            complete_message = ""
            message = st.empty()
            # Streaming the response out
            for chunk in fullresponse:
                if chunk.choices[0].delta.content is not None:
                    # Print the content of the chunk
                    # flush=True will force the output to be printed immediately
                    # end='' will prevent a new line after each print
                    complete_message += chunk.choices[0].delta.content
                    message.markdown(complete_message)
    except Exception as e:
        st.chat_message('ai').markdown('Something went wrong😣')

# summarise the stock price movements for AAPL for the last 7 days

# this will start a local server with chat format 'functionary' or 'chatml' or '...' and run the model on the server
# run this file open a PS terminal and run the command: 
# python -m llama_cpp.server --config_file config.json
# then run streamlit app in another PS terminal with: streamlit run dual_model_04.py


# 502 Error - Bad Gateway solution see README.md
# try command: $env:NO_PROXY = "localhost,127.0.0.1" 
# may caused by the proxy settings in the system, if you are using a proxy server
# , you may need to configure your proxy settings to allow access to the local server.
