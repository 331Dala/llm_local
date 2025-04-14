from openai import OpenAI

# Create a client instance
client = OpenAI(
	api_key='asdasd123', 
	base_url='http://localhost:8000/v1'
)

# Create a chat completion聊天补全
response = client.chat.completions.create(
    # which model to use
    model = 'D:\ml_workspace\llm_local\models\mistral-7b-instruct-v0.1.Q4_0.gguf',
    # messages to send to the model aka prompt
    messages = [{'role': 'user', 'content': 'What is ROI in reference to finance?'}], 
	# add stream output
    stream = True
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        # Print the content of the chunk
        # flush=True will force the output to be printed immediately
        # end='' will prevent a new line after each print
        print(chunk.choices[0].delta.content, end='', flush=True)

# write me a python function to get stock prices using yfinance

# run this file open a PS terminal and run the command: python -m llama_cpp.server --model models/mistral-7b-instruct-v0.1.Q4_0.gguf
# then run this file in another PS terminal with: python streamlit_02.py
# this will start a local server and run the model on the server

# InternalServerError: Error code: 502 - Bad Gateway solution see README.md
# try command: $env:NO_PROXY = "localhost,127.0.0.1" 
# may caused by the proxy settings in the system, if you are using a proxy server, you may need to configure your proxy settings to allow access to the local server.
