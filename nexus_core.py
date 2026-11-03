import os
import time
import subprocess
import urllib.request
import json

PROJECT_DIR = os.getcwd()
LOCAL_LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"

def query_local_qwen(prompt):
    print(f"\n[AI AGENT] -> Querying local Qwen model (extended timeout)...")
    payload = {
        "model": "qwen",
        "messages": [
            {"role": "system", "content": "You are a concise game dev AI. Output ONLY raw executable JavaScript code inside standard tags, no long explanations."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 1500
    }
    
    req = urllib.request.Request(
        LOCAL_LLM_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        # Increased timeout to 120 seconds for mobile GGUF processing
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            code_content = res_data['choices'][0]['message']['content']
            if "```javascript" in code_content:
                code_content = code_content.split("```javascript")[1].split("```")[0]
            elif "```js" in code_content:
                code_content = code_content.split("```js")[1].split("```")[0]
            elif "```" in code_content:
                code_content = code_content.split("```")[1].split("```")[0]
            return code_content.strip()
    except Exception as e:
        print(f"  └── [ERROR] LLM request failed or timed out: {e}")
        return None

print("Nexus Core (Extended Timeout Edition) initialized.")
while True:
    try:
        cmd = input("NexusCore> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif len(cmd.strip()) > 0:
            print(f"\n[AGENT TOOL DISPATCH] -> Processing: '{cmd.strip()}'")
            generated_code = query_local_qwen(cmd)
            
            if generated_code:
                with open("game.js", "w", encoding="utf-8") as f:
                    f.write(generated_code)
                print("  └── [SUCCESS] Qwen generated and wrote code to game.js!")
                
                print("[GIT SYNC] -> Committing and pushing changes...")
                subprocess.run("git add .", shell=True, capture_output=True)
                subprocess.run(f'git commit -m "Qwen update: {cmd[:30]}"', shell=True, capture_output=True)
                res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
                if res.returncode == 0:
                    print("  └── [SUCCESS] Pushed to GitHub successfully!\n")
                else:
                    print(f"  └── [NOTICE] Saved locally. Push note: {res.stderr.strip()}\n")
            else:
                print("  └── [FAILED] Could not write file due to generation error.")
        else:
            print("Please enter a valid command.")
    except KeyboardInterrupt:
        break
