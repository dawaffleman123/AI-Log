import ollama
import subprocess

# Settings

version = "v0.2.0"
isCPU = True

if isCPU:
    model = "gemma2:2b"
else:
    model = "gemma2"

print(f"AI Log Summarizer {version}\nModel name: {model}")

cmd=['sudo', 'dmesg']

try:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=isinstance(cmd, str))
    log = result.stdout
    
except subprocess.CalledProcessError as e:
    print(f"Error: {e.stderr}")
    
    exit()


# Pass the log into ollama
stream = ollama.chat(
    model=model,
    messages=[{'role': 'user', 'content': f'The following is a snippet from the dmesg log on linux. Find any errors or probable errors that could occur. Also give a brief summary of what happens and try to explain it in simple and easy to understand terms. At the end give suggjestions on how to improve system performance and to fix certain errors Here is the log file, {log}'}],
    stream=True,
    )
   

# Print the response
try:


    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True) 

except ollama._types.ResponseError as cheese:
    print(cheese)
    print(f"{model} is not found, Attempting to pull")
    ollama.pull(model)
    print("pull complete!")
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True) 

print("\n\n\n")
