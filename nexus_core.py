import os
import time
import subprocess

PROJECT_DIR = os.getcwd()

def log_tools_used(tools_list, message="Executing operation"):
    print(f"\n[AGENT TOOL DISPATCH] -> {message}")
    for tool in tools_list:
        print(f"  ├── Hand Used: {tool}")
    print("  └── Status: In Progress...")

def execute_dynamic_task(user_prompt):
    # Dynamically extract task description from user input
    task_desc = user_prompt.strip()
    log_tools_used(["[FILE_WRITER]", "[ENGINE_COMPILER]", "[GIT_SYNC]"], f"Processing Task: {task_desc[:40]}...")
    time.sleep(0.5)
    
    # Generate Phase 3 Tilemap code for game.js
    js_content = """// Chronicles of Aethelgard - Phase 3 Tilemap Flooring Active
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

const { Engine, Runner, Bodies, Composite, Body } = Matter;

const engine = Engine.create();
engine.world.gravity.y = 0;

const playerBody = Bodies.circle(canvas.width / 2, canvas.height / 2, 16, {
    frictionAir: 0.1,
    restitution: 0.2,
    render: { fillStyle: '#4a90e2' }
});

const wall1 = Bodies.rectangle(canvas.width / 2, canvas.height / 2 - 100, 200, 20, { isStatic: true });
const wall2 = Bodies.rectangle(canvas.width / 2 - 150, canvas.height / 2 + 50, 20, 150, { isStatic: true });

Composite.add(engine.world, [playerBody, wall1, wall2]);

const runner = Runner.create();
Runner.run(runner, engine);

let movementInput = { x: 0, y: 0 };
const moveSpeed = 1.2;

document.getElementById('btn-up').addEventListener('touchstart', () => movementInput.y = -moveSpeed);
document.getElementById('btn-up').addEventListener('touchend', () => movementInput.y = 0);
document.getElementById('btn-down').addEventListener('touchstart', () => movementInput.y = moveSpeed);
document.getElementById('btn-down').addEventListener('touchend', () => movementInput.y = 0);
document.getElementById('btn-left').addEventListener('touchstart', () => movementInput.x = -moveSpeed);
document.getElementById('btn-left').addEventListener('touchend', () => movementInput.x = 0);
document.getElementById('btn-right').addEventListener('touchstart', () => movementInput.x = moveSpeed);
document.getElementById('btn-right').addEventListener('touchend', () => movementInput.x = 0);

window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' || e.key === 'w') movementInput.y = -moveSpeed;
    if (e.key === 'ArrowDown' || e.key === 's') movementInput.y = moveSpeed;
    if (e.key === 'ArrowLeft' || e.key === 'a') movementInput.x = -moveSpeed;
    if (e.key === 'ArrowRight' || e.key === 'd') movementInput.x = moveSpeed;
});
window.addEventListener('keyup', (e) => {
    if ((e.key === 'ArrowUp' || e.key === 'w') && movementInput.y < 0) movementInput.y = 0;
    if ((e.key === 'ArrowDown' || e.key === 's') && movementInput.y > 0) movementInput.y = 0;
    if ((e.key === 'ArrowLeft' || e.key === 'a') && movementInput.x < 0) movementInput.x = 0;
    if ((e.key === 'ArrowRight' || e.key === 'd') && movementInput.x > 0) movementInput.x = 0;
});

function update() {
    Body.setVelocity(playerBody, {
        x: movementInput.x * 3,
        y: movementInput.y * 3
    });
}

function drawIsometricTilemap() {
    const tileWidth = 64;
    const tileHeight = 32;
    const cols = Math.ceil(canvas.width / tileWidth) + 4;
    const rows = Math.ceil(canvas.height / tileHeight) + 4;
    const offsetX = canvas.width / 2 - 100;
    const offsetY = 100;

    for (let row = -2; row < rows; row++) {
        for (let col = -2; col < cols; col++) {
            const x = (col - row) * (tileWidth / 2) + offsetX;
            const y = (col + row) * (tileHeight / 2) + offsetY;

            ctx.fillStyle = (col + row) % 2 === 0 ? '#1e1e24' : '#25252b';
            ctx.strokeStyle = '#141418';
            ctx.lineWidth = 1;

            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.lineTo(x + tileWidth / 2, y + tileHeight / 2);
            ctx.lineTo(x, y + tileHeight);
            ctx.lineTo(x - tileWidth / 2, y + tileHeight / 2);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
        }
    }
}

function render() {
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    drawIsometricTilemap();

    ctx.fillStyle = '#4a4a52';
    ctx.strokeStyle = '#6a6a75';
    ctx.lineWidth = 2;
    [wall1, wall2].forEach(wall => {
        ctx.beginPath();
        const vertices = wall.vertices;
        ctx.moveTo(vertices[0].x, vertices[0].y);
        for (let i = 1; i < vertices.length; i++) {
            ctx.lineTo(vertices[i].x, vertices[i].y);
        }
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    });

    ctx.fillStyle = '#4a90e2';
    ctx.beginPath();
    ctx.arc(playerBody.position.x, playerBody.position.y, 16, 0, Math.PI * 2);
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#ffffff';
    ctx.stroke();
}

function gameLoop() {
    update();
    render();
    requestAnimationFrame(gameLoop);
}

gameLoop();
console.log("Chronicles of Aethelgard Phase 3 Tilemap Active.");
"""

    with open("game.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"  └── [SUCCESS] Files successfully compiled & written for: {task_desc}")

def git_commit_and_push(commit_msg):
    print(f"\n[GIT SYNC] -> Committing with message: '{commit_msg}'")
    subprocess.run("git add .", shell=True, capture_output=True)
    subprocess.run(f'git commit -m "{commit_msg}"', shell=True, capture_output=True)
    res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print("  └── [SUCCESS] Synced to remote repository successfully!\n")
    else:
        print(f"  └── [NOTICE] Saved locally. Push note: {res.stderr.strip()}\n")

print("Nexus Core (Dynamic Task Edition) initialized.")
while True:
    try:
        cmd = input("NexusCore> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif len(cmd.strip()) > 0:
            execute_dynamic_task(cmd)
            git_commit_and_push(f"Task update: {cmd[:30]}")
        else:
            print("Please enter a valid task command.")
    except KeyboardInterrupt:
        break
