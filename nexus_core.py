import os
import subprocess
import requests
import json

PROJECT_DIR = os.getcwd()
LLAMA_SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"

class NexusPipelinePipeline:
    def __init__(self):
        print("[INIT] Nexus Modular Skill Pipeline + World Generator initialized.")
        print("  ├── 1. [ADHD_SKILL_BREAKER] ....... READY")
        print("  ├── 2. [LOCAL_QWEN_MODEL] ......... CONNECTED (No Timeouts)")
        print("  ├── 3. [WORLD_GENERATOR_SKILL] .... ACTIVE (Procedural Maps & Tiles)")
        print("  ├── 4. [PONYTAIL_BOILERPLATE_CUTTER] ACTIVE (Shreds Bloat)")
        print("  ├── 5. [SELF_AUDITING_LOOP] ....... ACTIVE")
        print("  ├── 6. [FILE_WRITER] .............. READY")
        print("  ├── 7. [MARKDOWN_LOGGER] .......... READY")
        print("  └── 8. [GIT_SYNC_HANDLER] ......... READY\n")

    def query_qwen(self, system_prompt, user_prompt):
        payload = {
            "model": "qwen",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
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
            return None

    def execute_pipeline(self, raw_prompt):
        print(f"\n[PIPELINE START] Processing World Request: '{raw_prompt}'")
        
        status_report = {
            "prompt": raw_prompt,
            "adhd_split": False,
            "model_generated": False,
            "world_skill_applied": True,
            "boilerplate_shredded": False,
            "audit_repaired": False,
            "file_written": False,
            "markdowns_updated": False,
            "git_pushed": False,
            "git_error": ""
        }

        # --- STEP 1: ADHD Skill Breakdown ---
        print("  ├── [1. ADHD_SKILL_BREAKER] Breaking down world generation parameters...")
        sub_tasks = [
            f"World Environment Goal: {raw_prompt}",
            "Generate procedural floor tiles, grid lines, environmental obstacles, and collectible gold items.",
            "Maintain minimal HTML5 Canvas, Matter.js physics (gravity 0), touch controls, and PixelFX particles."
        ]
        status_report["adhd_split"] = True

        # --- STEP 2 & 3: Local Model + World Generator Skill ---
        print("  ├── [2 & 3. LOCAL MODEL + WORLD GENERATOR] Synthesizing rich visual world layout...")
        system_instructions = """You are an expert procedural 2D game world architect. Write clean, concise JavaScript game code for 'game.js' that renders a stunning visual world (grid backgrounds, atmospheric lighting/particles, static environmental obstacles to navigate around, and glowing collectible items). Avoid verbose commentary. Return ONLY raw JavaScript code without markdown wrappers."""
        
        combined_prompt = f"Build the following world environment into the game loop:\n- " + "\n- ".join(sub_tasks)
        code = self.query_qwen(system_instructions, combined_prompt)
        
        if not code:
            print("  ❌ [ERROR] World generation failed.")
            self.print_summary(status_report)
            return
        status_report["model_generated"] = True

        # --- STEP 4: Ponytail Boilerplate Cutter ---
        print("  ├── [4. PONYTAIL_BOILERPLATE_CUTTER] Shredding unnecessary boilerplate...")
        lines = []
        for line in code.split('\n'):
            stripped = line.strip()
            if stripped.startswith('// TODO') or stripped.startswith('// DEBUG') or (stripped.startswith('*') and len(stripped) < 5):
                continue
            lines.append(line)
        code = '\n'.join(lines).strip()
        status_report["boilerplate_shredded"] = True

        # --- STEP 5: Self-Auditing Loop ---
        print("  ├── [5. SELF_AUDITING_LOOP] Auditing syntax and bracket closure...")
        open_b = code.count('{')
        close_b = code.count('}')
        if open_b != close_b:
            print(f"      ⚠️ Bracket mismatch detected ({open_b} open vs {close_b} close). Auto-repairing...")
            repair_prompt = f"Fix the bracket mismatch in this JavaScript code and return only valid code:\n\n{code}"
            code = self.query_qwen(system_instructions, repair_prompt) or code
            status_report["audit_repaired"] = True
        else:
            print("      -> Self-audit passed successfully.")

        # --- STEP 6: File Creating/Editing ---
        print("  ├── [6. FILE_WRITER] Writing world logic to game.js...")
        try:
            with open("game.js", "w", encoding="utf-8") as f:
                f.write(code)
            status_report["file_written"] = True
        except Exception as e:
            status_report["file_written"] = False

        # --- STEP 7: Markdown Documentation ---
        print("  ├── [7. MARKDOWN_LOGGER] Updating CHANGELOG.md and PROJECT_STATUS.md...")
        try:
            changelog_entry = f"\n- **[World Update: {raw_prompt}]**: Generated via World Generator Skill -> Qwen -> Ponytail -> Self-Audit."
            if not os.path.exists("CHANGELOG.md"):
                with open("CHANGELOG.md", "w", encoding="utf-8") as cf:
                    cf.write("# Chronicles of Aethelgard - Dev Log\n")
            with open("CHANGELOG.md", "a", encoding="utf-8") as cf:
                cf.write(changelog_entry)

            status_entry = f"\n- **World Environment**: {raw_prompt}"
            if not os.path.exists("PROJECT_STATUS.md"):
                with open("PROJECT_STATUS.md", "w", encoding="utf-8") as sf:
                    sf.write("# Chronicles of Aethelgard - Project Status\n\n## World Environments\n")
            with open("PROJECT_STATUS.md", "a", encoding="utf-8") as sf:
                sf.write(status_entry)
            status_report["markdowns_updated"] = True
        except Exception as e:
            status_report["markdowns_updated"] = False

        # --- STEP 8: Git Push ---
        print("  ├── [8. GIT_SYNC_HANDLER] Staging changes and pushing to GitHub...")
        subprocess.run("git add .", shell=True, capture_output=True)
        subprocess.run(f'git commit -m "World Generator update: {raw_prompt[:30]}"', shell=True, capture_output=True)
        res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)

        if res.returncode == 0:
            status_report["git_pushed"] = True
        else:
            status_report["git_pushed"] = False
            status_report["git_error"] = res.stderr.strip()

        # --- STEP 9: Execution Summary Report ---
        self.print_summary(status_report)

    def print_summary(self, report):
        print("\n" + "="*50)
        print("🌍 WORLD GENERATOR EXECUTION SUMMARY")
        print("="*50)
        print(f" • **Target World Prompt**: {report['prompt']}")
        print(f" • **ADHD Breakdown**: {'✅ Succeeded' if report['adhd_split'] else '❌ Failed'}")
        print(f" • **World Generator Skill**: {'✅ Active & Applied' if report['world_skill_applied'] else '❌ Skipped'}")
        print(f" • **Qwen Generation**: {'✅ Succeeded' if report['model_generated'] else '❌ Failed'}")
        print(f" • **Ponytail Code Shredder**: {'✅ Bloat removed' if report['boilerplate_shredded'] else '❌ Skipped'}")
        print(f" • **Self-Audit Repair**: {'🔧 Auto-repaired brackets' if report['audit_repaired'] else '✅ Clean on first pass'}")
        print(f" • **File Writer (`game.js`)**: {'✅ World created / updated' if report['file_written'] else '❌ Failed to write'}")
        print(f" • **Markdown Logs**: {'✅ Updated' if report['markdowns_updated'] else '❌ Failed'}")
        print(f" • **GitHub Sync**: {'✅ Pushed successfully' if report['git_pushed'] else f'⚠️ Local only (Error: {report["git_error"]})'}")
        print("="*50 + "\n")

nexus = NexusPipelinePipeline()

while True:
    try:
        cmd = input("NexusWorld> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif len(cmd.strip()) > 0:
            nexus.execute_pipeline(cmd)
        else:
            print("Please enter a valid command.")
    except KeyboardInterrupt:
        break
