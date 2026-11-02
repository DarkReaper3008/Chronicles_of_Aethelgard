import os
import subprocess

PROJECT_DIR = os.getcwd()

def git_commit_and_push(message="Checkpoint commit by Nexus Core", remote_branch="main"):
    os.makedirs(PROJECT_DIR, exist_ok=True)
    subprocess.run(f"cd {PROJECT_DIR} && git init", shell=True, capture_output=True)
    subprocess.run(f"cd {PROJECT_DIR} && git add .", shell=True, capture_output=True)
    res = subprocess.run(f'cd {PROJECT_DIR} && git commit -m "{message}"', shell=True, capture_output=True, text=True)
    
    push_res = subprocess.run(f"cd {PROJECT_DIR} && git push origin {remote_branch}", shell=True, capture_output=True, text=True)
    
    status_msg = []
    if res.returncode == 0:
        status_msg.append(f"Committed: '{message}'")
    else:
        status_msg.append("No new local changes to commit.")
        
    if push_res.returncode == 0:
        status_msg.append(f"Successfully pushed to GitHub ({remote_branch})!")
    else:
        status_msg.append(f"Git Push Note: Check remote repository configuration.")
        
    return " | ".join(status_msg)

print("Nexus Core initialized in Chronicles of Aethelgard environment.")
print("Type 'exit' to quit.")

while True:
    try:
        cmd = input("NexusCore> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif cmd.startswith("[GIT_PUSH]"):
            print(git_commit_and_push())
        else:
            print(f"Executing/Acknowledged: {cmd}")
    except KeyboardInterrupt:
        break
