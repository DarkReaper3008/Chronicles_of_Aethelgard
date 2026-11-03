import os
import subprocess
import requests
import json

PROJECT_DIR = os.getcwd()
LLAMA_SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"

class NexusAIBridge:
    def __init__(self):
        print("[INIT] Nexus Core AI Bridge + Skill Context initialized.")
        print("  ├── Hand: [LOCAL_QWEN_MODEL] ... CONNECTED (No Timeouts)")
        print("  ├── Hand: [SKILL_CONTEXT_INJECTOR] ... ACTIVE")
        print("  ├── Hand: [FILE_WRITER] ........ READY")
        print("  └── Hand: [GIT_SYNC_HANDLER] ... READY\n")

    def think_and_generate_code(self, prompt):
        print(f"\n[AI THINKING] Querying local Qwen model with full project skills for: '{prompt}'...")
        
        # Comprehensive system prompt embedding your established game architecture and skills
        system_instructions = """You are an expert mobile-first HTML5 and Matter.js game developer working on 'Chronicles of Aethelgard'.
You must generate complete, working JavaScript game code for 'game.js'.

Project Architectural Rules & Skills to Include:
1. Engine Setup: HTML5 Canvas resizing, Matter.js world gravity set to 0, player circle body with frictionAir and restitution.
2. Mobile UI & Controls: On-screen touch control event listeners (up, down, left, right, attack).
3. Boundary Clamping: Keep player and entities within safe mobile screen margins (no walking off-screen).
4. Asset & FX Integration: Support for PixelFX particle bursts (spawning sparks on coin pickup or damage) and background grid rendering.
5. Game State Management: Track gold count, player HP (default 100), pause states, and Game Over / restart overlays when HP reaches 0.
6. Output Format: Return ONLY raw, valid JavaScript code. Do not wrap code in markdown codeblocks like ```javascript."""

        payload = {
            "model": "qwen",
            "messages": [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 2000
        }

        try:
            response = requests.post(LLAMA_SERVER_URL, json=payload, timeout=None)
            if response.status_code == 200:
                res_json = response.json()
                generated_code = res_json['choices'][0]['message']['content']
                # Clean markdown wrappers if present
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
                print("  └── [HAND: FILE_WRITER] Writing skilled Qwen-generated code to game.js...")
                with open("game.js", "w", encoding="utf-8") as f:
                    f.write(code)
                
                print("  └── [HAND: GIT_SYNC_HANDLER] Committing and pushing updates...")
                subprocess.run("git add .", shell=True, capture_output=True)
                subprocess.run(f'git commit -m "Qwen Skill update: {cmd[:30]}"', shell=True, capture_output=True)
                res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
                
                if res.returncode == 0:
                    print("[SUCCESS] Code generated with project skills and pushed to GitHub!\n")
                else:
                    print(f"[NOTICE] Code written locally. Git output: {res.stderr.strip()}\n")
            else:
                print("[NOTICE] Generation skipped due to an error.")
        else:
            print("Please enter a valid command.")
    except KeyboardInterrupt:
        break
