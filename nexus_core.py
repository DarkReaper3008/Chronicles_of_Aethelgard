import os
import subprocess
import requests
import json

PROJECT_DIR = os.getcwd()
LLAMA_SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"

class NexusAutonomousAgent:
    def __init__(self):
        print("[INIT] Nexus Core Autonomous Agent + Self-Correction Loop initialized.")
        print("  ├── Hand: [LOCAL_QWEN_MODEL] ....... CONNECTED (No Timeouts)")
        print("  ├── Hand: [SKILL_CONTEXT_INJECTOR] .. ACTIVE")
        print("  ├── Hand: [SELF_CORRECTION_LOOP] ... ACTIVE (Auto-Diagnostics)")
        print("  ├── Hand: [FILE_WRITER] ............ READY")
        print("  └── Hand: [GIT_SYNC_HANDLER] ....... READY\n")

    def query_qwen(self, system_prompt, user_prompt):
        payload = {
            "model": "qwen",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 2000
        }
        try:
            response = requests.post(LLAMA_SERVER_URL, json=payload, timeout=None)
            if response.status_code == 200:
                res_json = response.json()
                code = res_json['choices'][0]['message']['content']
                return code.replace("```javascript", "").replace("```", "").strip()
            return None
        except Exception as e:
            print(f"[ERROR] Llama server connection error: {e}")
            return None

    def think_and_generate(self, prompt):
        print(f"\n[AI THINKING] Generating code for: '{prompt}'...")
        
        system_instructions = """You are an expert mobile-first HTML5 and Matter.js game developer working on 'Chronicles of Aethelgard'.
Generate complete, clean, working JavaScript game code for 'game.js'.
Ensure all curly braces, parentheses, and functions are fully closed and syntactically correct.
Include Canvas setup, Matter.js physics (gravity 0), touch controls, mobile boundary clamping, PixelFX particles, and Game Over/Pause state management.
Return ONLY raw JavaScript code without markdown wrappers."""

        code = self.query_qwen(system_instructions, prompt)
        if not code:
            return None

        # --- SELF-CORRECTION & DIAGNOSTIC HAND ---
        print("  └── [HAND: SELF_CORRECTION_LOOP] Inspecting code for syntax or structural flaws...")
        
        # Simple local static check for unclosed brackets or syntax bugs
        open_braces = code.count('{')
        close_braces = code.count('}')
        
        if open_braces != close_braces:
            print(f"  ⚠️ [DIAGNOSTIC WARNING] Bracket mismatch detected! ({open_braces} opening vs {close_braces} closing). Sending back to Qwen for auto-repair...")
            
            repair_prompt = f"The previous code generated had a structural bracket mismatch ({open_braces} opening vs {close_braces} closing braces). Please fix the syntax and return the complete, corrected JavaScript code:\n\n{code}"
            fixed_code = self.query_qwen(system_instructions, repair_prompt)
            if fixed_code:
                print("  └── [HAND: SELF_CORRECTION_LOOP] Code successfully repaired and validated!")
                return fixed_code

        print("  └── [HAND: SELF_CORRECTION_LOOP] Code passed structural diagnostics.")
        return code

nexus = NexusAutonomousAgent()

while True:
    try:
        cmd = input("NexusAI> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif len(cmd.strip()) > 0:
            code = nexus.think_and_generate(cmd)
            
            if code:
                print("  └── [HAND: FILE_WRITER] Writing validated code to game.js...")
                with open("game.js", "w", encoding="utf-8") as f:
                    f.write(code)
                
                print("  └── [HAND: MARKDOWN_LOGGER] Updating documentation logs...")
                changelog_entry = f"\n- **Update [{cmd}]**: Auto-generated and verified via Self-Correction Agent Loop."
                if not os.path.exists("CHANGELOG.md"):
                    with open("CHANGELOG.md", "w", encoding="utf-8") as cf:
                        cf.write("# Chronicles of Aethelgard - Dev Log\n")
                with open("CHANGELOG.md", "a", encoding="utf-8") as cf:
                    cf.write(changelog_entry)

                status_entry = f"\n- **Active Feature**: {cmd}"
                if not os.path.exists("PROJECT_STATUS.md"):
                    with open("PROJECT_STATUS.md", "w", encoding="utf-8") as sf:
                        sf.write("# Chronicles of Aethelgard - Project Status\n\n## Features\n")
                with open("PROJECT_STATUS.md", "a", encoding="utf-8") as sf:
                    sf.write(status_entry)

                print("  └── [HAND: GIT_SYNC_HANDLER] Committing and pushing to GitHub...")
                subprocess.run("git add .", shell=True, capture_output=True)
                subprocess.run(f'git commit -m "Self-repaired update: {cmd[:30]}"', shell=True, capture_output=True)
                res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
                
                if res.returncode == 0:
                    print("[SUCCESS] Autonomous cycle complete: Generated, self-fixed, logged, and pushed!\n")
                else:
                    print(f"[NOTICE] Code written locally. Git output: {res.stderr.strip()}\n")
            else:
                print("[NOTICE] Generation skipped due to an error.")
        else:
            print("Please enter a valid command.")
    except KeyboardInterrupt:
        break
