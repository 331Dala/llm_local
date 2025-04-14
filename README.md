# llm_local

Run LLM apps hyper fast on a local machine.

- **Operating System**: Windows 10  (system else [here](https://github.com/ggml-org/llama.cpp/blob/master/README.md))
- **Hardware**: CPU  
- **Python Version**: 3.10  

This project leverages **llama.cpp** as its backbone. You can find the official documentation [here](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md).

---

## Project File Description

This project contains five independent scripts. Each script is standalone and cannot be used simultaneously. Below is a brief description of each file:

1. **`openaiTest_01.py`**
2. **`streamlit_02.py`**
3. **`function_calling_03.py`**
4. **`dual_model_04.py`**
5. **`multimodal_llava_05.py`**

Each script includes instructions on how to run it at the end of the file.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ggerganov/llama.cpp
```

### 2. Build llama.cpp

Follow the official documentation for building llama.cpp on Windows. Below are the summarized steps:

1. Download the latest Fortran version of [w64devkit](https://github.com/skeeto/w64devkit/releases).  
2. Install [Visual Studio 2022](https://visualstudio.microsoft.com/zh-hans/vs/community/) and [CMake](https://cmake.org/download/).  
3. Extract `w64devkit` on your PC and run `w64devkit.exe`.  
4. Use the `cd` command to navigate to the `llama.cpp` folder.  
5. Optionally, download [ccache](https://ccache.dev/) to speed up CPU compilation.  
6. Run the following commands to build:
   ```bash
   cmake -B build
   cmake --build build --config Release -j 8
   ```
7. If you encounter errors related to CUDA or CURL, try:
   ```bash
   cmake -B build -DLLAMA_CURL=OFF
   ```

### 3. Install Python Dependencies
```bash
pip install openai 'llama-cpp-python[server]' pydantic instructor streamlit
```

### 4. Start the Server

Follow these commands to start the server based on your use case:

- **Single Model Chat**  
  ```bash
  python -m llama_cpp.server --model models/mistral-7b-instruct-v0.1.Q4_0.gguf
  ```

- **Single Model Chat with GPU Offload**  
  ```bash
  python -m llama_cpp.server --model models/mistral-7b-instruct-v0.1.Q4_0.gguf --n_gpu -1
  ```

- **Single Model Function Calling with GPU Offload**  
  ```bash
  python -m llama_cpp.server --model models/mistral-7b-instruct-v0.1.Q4_0.gguf --n_gpu -1 --chat functionary
  ```

- **Multiple Model Load with Config File**  
  ```bash
  python -m llama_cpp.server --config_file config.json
  ```

- **Multi-Modal Models**  
  ```bash
  python -m llama_cpp.server --model models/llava-v1.5-7b-Q4_K.gguf --clip_model_path models/llava-v1.5-7b-mmproj-Q4_0.gguf --n_gpu -1 --chat llava-1-5
  ```

### 5. Run the Script
```bash
streamlit run app.py
```

---

## Known Issues and Solutions

### 502 Error Caused by Enabling Proxy

When running the `app.py` script with the proxy enabled, you may encounter the error:
```
openai.InternalServerError: Error code: 502
```
This error is due to the proxy interfering with the communication between the client (Python script) and the local server (local LLM server).

#### **Solution**

To resolve this issue, you can set up a proxy whitelist so that requests sent to the local server bypass the proxy. Follow these steps:

1. Open a PowerShell terminal.
2. Execute the following command to set the proxy whitelist:
   ```powershell
   $env:NO_PROXY = "localhost,127.0.0.1"
   ```

---

## Troubleshooting: HTTP Error 403 and Model Response Issues

### Problem 1: HTTP Error 403: Forbidden

#### Description
When attempting to load an image from a URL, the application encountered an `HTTP Error 403: Forbidden`. This error indicates that the server rejected the request, likely due to missing or incorrect HTTP headers.

#### Solutions Attempted

1. **Added Custom HTTP Headers**  
   - **Action**: Added `User-Agent` and `Referer` headers to mimic a browser request.  
   - **Code**:
     ```python
     headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
         'Referer': 'https://png.pngtree.com/'
     }
     req = urllib.request.Request(image_url, headers=headers)
     ```
   - **Result**: The image loaded successfully, resolving the HTTP Error 403.

2. **Validated Image URL**  
   - **Action**: Ensured the URL was properly formatted and stripped of extra spaces or newlines.
     ```python
     image_url = st.text_input('Enter image URL here').strip()
     ```
   - **Result**: The URL was confirmed to be valid, but this step alone did not resolve the issue.

3. **Tested Image Loading Independently**  
   - **Action**: Tested the image loading logic in a standalone script to isolate the issue.
   - **Result**: The image loaded successfully in the standalone script, confirming that the issue was not with the URL or headers.

4. **Used `requests` Library Instead of `urllib`**  
   - **Action**: Replaced `urllib` with the `requests` library for more robust HTTP handling.
     ```python
     import requests
     response = requests.get(image_url, headers=headers, timeout=10)
     ```
   - **Result**: The image loaded successfully, though this change was not necessary after adding headers to `urllib`.

---

### Problem 2: Model Fails to Respond to Prompts

#### Description
After resolving the image loading issue, the model failed to provide a proper response to prompts. The server logs showed an exception in the ASGI application, specifically related to the model's internal image loading logic.

#### Solutions Attempted

1. **Modified Model's Internal Image Loading Logic**  
   - **Action**: Ensured the model's internal `_load_image` function used the same headers as the custom image loader.
     ```python
     def _load_image(image_url):
         headers = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
             'Referer': 'https://png.pngtree.com/'
         }
         req = urllib.request.Request(image_url, headers=headers)
         with urllib.request.urlopen(req) as response:
             return response.read()
     ```
   - **Result**: The error persisted, indicating the issue might not be solely related to image loading logic.

2. **Simplified Model Input**  
   - **Action**: Simplified the messages parameter sent to the model to include only text (excluding the image URL).
     ```python
     messages = [{'role': 'user', 'content': prompt}]
     ```
   - **Result**: The model responded correctly to text-only prompts, suggesting the issue lies in handling multimodal inputs.

3. **Tested Local Fallback for Images**  
   - **Action**: Provided a fallback mechanism to load a local image if the URL failed.
     ```python
     local_image_path = "fallback_image.png"
     try:
         with open(local_image_path, "rb") as f:
             image_data = f.read()
     except Exception as e:
         st.error(f"Error loading fallback image: {e}")
     ```
   - **Result**: The fallback mechanism worked, but the model still failed to process prompts with image URLs.

4. **Checked Proxy Settings**  
   - **Action**: Ensured the local server was excluded from proxy settings by setting the `NO_PROXY` environment variable.
     ```powershell
     $env:NO_PROXY = "localhost,127.0.0.1"
     ```
   - **Result**: No change in behavior; the error persisted.

---

### Current Status
- **Image Loading**: Resolved. Images can be loaded successfully using the custom image loader.
- **Model Response**: Unresolved. The model fails to process prompts containing image URLs, throwing an exception in the ASGI application.

---

### Next Steps
1. Investigate the model's handling of multimodal inputs (text + image).  
2. Debug the ASGI application to identify the root cause of the exception.  
3. Consult the documentation or support for the `llama_cpp` library to ensure proper usage of multimodal inputs.

---

### Conclusion
While the image loading issue has been resolved, the model's inability to process prompts with image URLs remains a challenge. Further debugging and investigation are required to address this issue.

---

## Models Used
- **Mistral**: [Mistral-7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)
- **Mixtral**: [Mixtral-8x7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF)
- **LLaVa**: [LLaVa-v1.5-7B-GGUF](https://huggingface.co/jartine/llava-v1.5-7B-GGUF/tree/main)

---

## Known Compatibility Issues

- **Mixtral Model**:  
  The model `Mixtral-8x7B-Instruct-v0.1.Q2_K.gguf` is incompatible with the latest version of `llama.cpp` due to changes in how MoE tensors are handled.  
  **Solution**: Download an older version of the model from [here](https://huggingface.co/mradermacher/Mixtral-8x7B-Instruct-v0.1-GGUF?show_file_info=Mixtral-8x7B-Instruct-v0.1.Q2_K.gguf)