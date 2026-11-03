import os
import subprocess

PROJECT_DIR = os.getcwd()

def generate_game_files():
    os.makedirs(PROJECT_DIR, exist_ok=True)
    
    # 1. index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Chronicles of Aethelgard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas"></canvas>
        <div id="ui-overlay">
            <div id="hud">HP: 100 | Gold: 0</div>
            <div id="changelog-panel">Phase 1: Isometric Engine Active</div>
        </div>
        <div id="touch-controls">
            <div class="virtual-dpad">
                <button id="btn-up" class="dpad-btn">▲</button>
                <div class="dpad-row">
                    <button id="btn-left" class="dpad-btn">◀</button>
                    <button id="btn-right" class="dpad-btn">▶</button>
                </div>
                <button id="btn-down" class="dpad-btn">▼</button>
            </div>
            <div class="virtual-actions">
                <button id="btn-action" class="action-btn">⚔️</button>
            </div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
    <script src="game.js"></script>
</body>
</html>"""
    
    # 2. style.css
    css_content = """body, html {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #111;
    font-family: monospace;
    color: #fff;
}
#game-container {
    position: relative;
    width: 100%;
    height: 100%;
}
canvas {
    display: block;
    width: 100%;
    height: 100%;
}
#ui-overlay {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
    font-size: 14px;
    text-shadow: 1px 1px #000;
}
#changelog-panel {
    background: rgba(0,0,0,0.6);
    padding: 4px 8px;
    border: 1px solid #444;
}
#touch-controls {
    position: absolute;
    bottom: 20px;
    left: 20px;
    right: 20px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
}
.virtual-dpad {
    display: flex;
    flex-direction: column;
    align-items: center;
    pointer-events: auto;
}
.dpad-row {
    display: flex;
    gap: 40px;
}
.dpad-btn, .action-btn {
    width: 60px;
    height: 60px;
    background: rgba(255,255,255,0.2);
    border: 2px solid rgba(255,255,255,0.5);
    border-radius: 50%;
    color: white;
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    touch-action: manipulation;
}
.virtual-actions {
    display: flex;
    align-items: flex-end;
    pointer-events: auto;
}
.action-btn {
    background: rgba(180, 50, 50, 0.4);
    border-color: rgba(255, 100, 100, 0.8);
}"""

    # 3. game.js
    js_content = """// Chronicles of Aethelgard - Phase 1 Core Engine
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Player state in 2.5D isometric projection space
let player = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    vx: 0,
    vy: 0,
    speed: 3,
    radius: 16
};

// Input handling from virtual buttons
let keys = { up: false, down: false, left: false, right: false };

document.getElementById('btn-up').addEventListener('touchstart', () => keys.up = true);
document.getElementById('btn-up').addEventListener('touchend', () => keys.up = false);
document.getElementById('btn-down').addEventListener('touchstart', () => keys.down = true);
document.getElementById('btn-down').addEventListener('touchend', () => keys.down = false);
document.getElementById('btn-left').addEventListener('touchstart', () => keys.left = true);
document.getElementById('btn-left').addEventListener('touchend', () => keys.left = false);
document.getElementById('btn-right').addEventListener('touchstart', () => keys.right = true);
document.getElementById('btn-right').addEventListener('touchend', () => keys.right = false);

// Keyboard fallbacks for desktop testing
window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' || e.key === 'w') keys.up = true;
    if (e.key === 'ArrowDown' || e.key === 's') keys.down = true;
    if (e.key === 'ArrowLeft' || e.key === 'a') keys.left = true;
    if (e.key === 'ArrowRight' || e.key === 'd') keys.right = true;
});
window.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowUp' || e.key === 'w') keys.up = false;
    if (e.key === 'ArrowDown' || e.key === 's') keys.down = false;
    if (e.key === 'ArrowLeft' || e.key === 'a') keys.left = false;
    if (e.key === 'ArrowRight' || e.key === 'd') keys.right = false;
});

function update() {
    if (keys.up) player.y -= player.speed;
    if (keys.down) player.y += player.speed;
    if (keys.left) player.x -= player.speed;
    if (keys.right) player.x += player.speed;
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

    // Draw player placeholder (Hero character)
    ctx.fillStyle = '#4a90e2';
    ctx.beginPath();
    ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
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
console.log("Chronicles of Aethelgard engine initialized.");
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    with open("style.css", "w", encoding="utf-8") as f:
        f.write(css_content)
    with open("game.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    return "Successfully generated index.html, style.css, and game.js!"

def git_commit_and_push(message="Phase 1 core generated"):
    subprocess.run("git add .", shell=True, capture_output=True)
    subprocess.run(f'git commit -m "{message}"', shell=True, capture_output=True)
    res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        return "Committed and pushed Phase 1 files to GitHub!"
    return f"Files saved locally. Git push note: {res.stderr.strip()}"

print("Nexus Core (Builder Edition) active.")
while True:
    try:
        cmd = input("NexusCore> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif "generate" in cmd.lower() or "files" in cmd.lower():
            print(generate_game_files())
            print(git_commit_and_push())
        elif "[GIT_PUSH]" in cmd:
            print(git_commit_and_push())
        else:
            print(f"Acknowledged: {cmd}. Type your build command to generate files.")
    except KeyboardInterrupt:
        break
