import requests
from sseclient import SSEClient
import subprocess
import json
import time

# --- CONFIG ---
SERENA_SSE_URL = "http://127.0.0.1:9121/sse"
OLLAMA_MODEL = "llama3.2:3b" # تأكد من أن هذا النموذج موجود لديك

# --- FUNCTION TO QUERY SERENA ---
def query_serena_sse():
    """
    يتصل بنقطة نهاية SSE الخاصة بـ Serena للاستماع إلى الرسائل.
    """
    print("Connecting to Serena SSE...")
    try:
        session = requests.Session()
        response = session.get(SERENA_SSE_URL, stream=True)
        response.encoding = 'utf-8'
        messages = SSEClient(response)
        
        for msg in messages.events():
            yield msg.data
            
    except requests.exceptions.RequestException as e:
        print(f"\nError: Could not connect to Serena SSE. Is the Serena server running? Details: {e}")
        return

# --- FUNCTION TO CALL OLLAMA ---
def query_ollama(prompt: str):
    """
    يستدعي نموذج Ollama مع الموجه المحدد باستخدام الأمر run الصحيح.
    """
    print("\nCalling Ollama with the result from Serena...")
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8' # تحديد الترميز لتجنب مشاكل ويندوز
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: 'ollama' command not found. Make sure Ollama is installed and in your system's PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error calling Ollama: {e.stderr}")
        return None

# --- MAIN ---
if __name__ == "__main__":
    query = "list all Python files in the project"
    print(f"Querying Serena: {query}")

    # استدعاء أداة Serena ثم الحصول على استجابة من Ollama
    for serena_response in query_serena_sse():
        # --== التعديل هنا: تجاهل رسالة معرف الجلسة الأولية ==--
        if "session_id" in serena_response:
            print(f"Serena session started: {serena_response}")
            continue # انتقل إلى الرسالة التالية

        print(f"Serena responded with file data: {serena_response}")

        # إنشاء موجه واضح لـ Ollama
        prompt_for_ollama = f"From the following JSON output, list only the file names mentioned in the 'files' list. Output must be only the file names, one per line. JSON: {serena_response}"
        
        ollama_response = query_ollama(prompt_for_ollama)
        
        if ollama_response:
            print("\n--- Ollama Final Response ---")
            print(ollama_response)
        
     