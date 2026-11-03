import os
import subprocess
import requests
import json

PROJECT_DIR = os.getcwd()
LLAMA_SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"

class NexusAIBridge:
    def __init__(self):
        print("[INIT] Nexus Core AI Bridge (Infinite Timeout Edition) initialized.")
        print("  ├── Hand: [LOCAL_QWEN_MODEL] ... CONNECTED (No Timeouts)")
        print("  ├── Hand: [FILE_WRITER] ........ READY")
        print("  └── Hand: [GIT_SYNC_HANDLER] ... READY\n")

    def think_and_generate_code(self, prompt):
        print(f"\n[AI THINKING] Querying local Qwen model for: '{prompt}' (Please wait, no timeout)...")
        
        payload = {
            "model": "qwen",
            "messages": [
                {"role": "system", "content": "You are an expert JavaScript game developer. Write ONLY valid, complete JavaScript game code for HTML5 Canvas and Matter.js based on the user's request. Do not include markdown blocks like ```javascript, just output raw code."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }

        try:
            # timeout=None ensures we wait as long as it takes for Qwen to finish writing on mobile
            response = requests.post(LLAMA_SERVER_URL, json=payload, timeout=None)
            if response.status_code == 200:
                res_json = response.json()
                generated_code = res_json['choices'][0]['message']['content']
                # Clean any markdown wrappers if the model accidentally adds them
                generated_code = generated_code.replace("```javascript", "").replace("```", "").strip()
                return generated_code
            else:
                print(f"[ERROR] Server returned status {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"[ERROR] Connection to local llama-server failed: {e}")
            return None

nexus = NexusAIBridge()

while True:
    try:
        cmd = input("NexusAI> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif len(cmd.strip()) > 0:
            code = nexus.think_and_generate_code(cmd)
            
            if code:
                print("  └── [HAND: FILE_WRITER] Writing Qwen-generated code to game.js...")
                with open("game.js", "w", encoding="utf-8") as f:
                    f.write(code)
                
                print("  └── [HAND: GIT_SYNC_HANDLER] Committing and pushing updates...")
                subprocess.run("git add .", shell=True, capture_output=True)
                subprocess.run(f'git commit -m "Qwen AI update: {cmd[:30]}"', shell=True, capture_output=True)
                res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
                
                if res.returncode == 0:
                    print("[SUCCESS] Qwen generated, wrote, and pushed changes successfully!\n")
                else:
                    print(f"[NOTICE] Code written locally. Git output: {res.stderr.strip()}\n")
            else:
                print("[NOTICE] Generation skipped due to an error.")
        else:
            print("Please enter a valid command.")
    except KeyboardInterrupt:
        break
