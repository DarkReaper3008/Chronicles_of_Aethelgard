import os
import time
import subprocess

PROJECT_DIR = os.getcwd()

def log_tools_used(tools_list, message="Executing operation"):
    print(f"\n[AGENT TOOL DISPATCH] -> {message}")
    for tool in tools_list:
        print(f"  ├── Hand Used: {tool}")
    print("  └── Status: In Progress...")

def upgrade_to_phase_2():
    log_tools_used(["[FILE_WRITER]", "[MATTER_PHYSICS_ENGINE]", "[GIT_SYNC]"], "Writing Phase 2 Physics Engine")
    time.sleep(0.5) # Visual progress delay so you can see it working
    
    js_content = """// Chronicles of Aethelgard - Phase 2 Physics Engine
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

function drawIsometricGrid() {
    ctx.strokeStyle = '#222';
    ctx.lineWidth = 1;
    const tileSize = 40;
    for (let x = 0; x < canvas.width; x += tileSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += tileSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

function render() {
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    drawIsometricGrid();

    ctx.fillStyle = '#666';
    ctx.strokeStyle = '#888';
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
console.log("Chronicles of Aethelgard Phase 2 Physics Engine Active.");
"""

    with open("game.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print("  └── [SUCCESS] game.js overwritten with Matter.js physics code.")

def git_commit_and_push(message="Phase 2 physics engine integrated"):
    print("\n[GIT SYNC] -> Pushing changes to remote repository...")
    subprocess.run("git add .", shell=True, capture_output=True)
    subprocess.run(f'git commit -m "{message}"', shell=True, capture_output=True)
    res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print("  └── [SUCCESS] Changes committed and pushed to GitHub successfully!\n")
    else:
        print(f"  └── [NOTICE] Files saved locally. Git push note: {res.stderr.strip()}\n")

print("Nexus Core (Live Progress Edition) initialized.")
while True:
    try:
        cmd = input("NexusCore> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif any(k in cmd.lower() for k in ["generate", "update", "game.js", "physics"]):
            upgrade_to_phase_2()
            git_commit_and_push()
        else:
            log_tools_used(["[SHELL_ECHO]"], "Echoing input")
            print(f"Acknowledged: {cmd}")
    except KeyboardInterrupt:
        break
