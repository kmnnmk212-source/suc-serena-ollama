import requests
from sseclient import SSEClient
import subprocess
import json

# --- CONFIG ---
SERENA_SSE_URL = "http://127.0.0.1:9121/sse"
OLLAMA_MODEL = "llama3.2:3b" # تأكد من استخدام اسم النموذج الصحيح لديك

# --- FUNCTION TO QUERY SERENA ---
def query_serena_sse():
    print("Connecting to Serena SSE...")
    try:
        session = requests.Session()
        response = session.get(SERENA_SSE_URL, stream=True)
        response.encoding = 'utf-8'
        messages = SSEClient(response)
        
        for msg in messages.events():
            if msg.data:
                try:
                    data = json.loads(msg.data)
                except json.JSONDecodeError:
                    data = msg.data
                print(f"Serena: {data}")
                yield data
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Serena SSE: {e}")
        return

# --- FUNCTION TO CALL OLLAMA (Modified for older versions) ---
def query_ollama(prompt: str):
    print("Calling Ollama...")
    try:
        #
        # --== التعديل هنا لاستخدام "run" بدلاً من "chat" ==--
        #
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error calling Ollama: {e.stderr}")
        return None

# --- MAIN ---
if __name__ == "__main__":
    query = "list all Python files in the project"
    print(f"Querying Serena: {query}\n")

    for serena_response in query_serena_sse():
        # تحويل الاستجابة إلى نص بسيط قبل إرسالها إلى Ollama
        prompt_for_ollama = f"Based on the following tool output, list the python file names. Output: {serena_response}"
        ollama_response = query_ollama(prompt_for_ollama)
        if ollama_response:
            print(f"Ollama response:\n{ollama_response}")
        break