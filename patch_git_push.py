import os

agent_path = "nexus_core.py"
with open(agent_path, "r", encoding="utf-8") as f:
    code = f.read()

old_git_func = '''def git_commit_changes(message="Auto-commit by Nexus Core"):
    os.makedirs(PROJECT_DIR, exist_ok=True)
    subprocess.run(f"cd {PROJECT_DIR} && git init", shell=True, capture_output=True)
    subprocess.run(f"cd {PROJECT_DIR} && git add .", shell=True, capture_output=True)
    res = subprocess.run(f'cd {PROJECT_DIR} && git commit -m "{message}"', shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        return f"Git committed successfully: '{message}'"
    return "Git commit note: No new changes to commit."'''

new_git_func = '''def git_commit_and_push(message="Checkpoint commit by Nexus Core", remote_branch="main"):
    os.makedirs(PROJECT_DIR, exist_ok=True)
    subprocess.run(f"cd {PROJECT_DIR} && git init", shell=True, capture_output=True)
    subprocess.run(f"cd {PROJECT_DIR} && git add .", shell=True, capture_output=True)
    res = subprocess.run(f'cd {PROJECT_DIR} && git commit -m "{message}"', shell=True, capture_output=True, text=True)
    
    # Try pushing to remote
    push_res = subprocess.run(f"cd {PROJECT_DIR} && git push origin {remote_branch}", shell=True, capture_output=True, text=True)
    
    status_msg = []
    if res.returncode == 0:
        status_msg.append(f"Committed: '{message}'")
    else:
        status_msg.append("No new local changes to commit.")
        
    if push_res.returncode == 0:
        status_msg.append(f"Successfully pushed to GitHub ({remote_branch})!")
    else:
        status_msg.append(f"Git Push Note: Check remote repository configuration. ({push_res.stderr.strip()})")
        
    return " | ".join(status_msg)'''

if old_git_func in code:
    code = code.replace(old_git_func, new_git_func)
    # Also update the handler in main loop
    code = code.replace('[GIT_COMMIT:', '[GIT_PUSH:') if '[GIT_COMMIT:' in code else code
    with open(agent_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully added GitHub push hand to Nexus Core!")
else:
    print("Could not locate exact git function block. Patching manually.")
