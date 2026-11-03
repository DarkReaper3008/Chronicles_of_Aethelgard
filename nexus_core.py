import os
import subprocess

PROJECT_DIR = os.getcwd()

def think_and_generate_code(prompt):
    p = prompt.lower()
    print(f"\n[AGENT THOUGHT PROCESS] Analyzing request: '{prompt}'")
    
    base_setup = """const canvas = document.getElementById('gameCanvas');
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
    frictionAir: 0.1, restitution: 0.2, render: { fillStyle: '#4a90e2' }
});
Composite.add(engine.world, [playerBody]);

const runner = Runner.create();
Runner.run(runner, engine);

let goldCount = 0;
let movementInput = { x: 0, y: 0 };
const moveSpeed = 1.2;
"""

    features = ""
    
    if "coin" in p or "gold" in p:
        print("  ├── [DECISION] Adding Gold Coin collection and inventory logic.")
        features += """
let coins = [
    { x: canvas.width / 2 + 60, y: canvas.height / 2 - 40, radius: 8, collected: false },
    { x: canvas.width / 2 - 80, y: canvas.height / 2 + 60, radius: 8, collected: false }
];
"""

    if "attack" in p or "sword" in p:
        print("  ├── [DECISION] Adding Melee Attack Hitbox logic.")
        features += """
let isAttacking = false;
let attackCooldown = 0;
document.getElementById('btn-attack').addEventListener('touchstart', (e) => {
    e.preventDefault();
    if (attackCooldown <= 0) { isAttacking = true; attackCooldown = 25; }
});
"""

    if "enemy" in p or "goblin" in p:
        print("  ├── [DECISION] Adding Enemy AI chasing logic.")
        features += """
let enemy = { x: canvas.width / 2 + 120, y: canvas.height / 2 + 120, radius: 14, speed: 0.6 };
"""

    loop_code = """
document.getElementById('btn-up').addEventListener('touchstart', () => movementInput.y = -moveSpeed);
document.getElementById('btn-up').addEventListener('touchend', () => movementInput.y = 0);
document.getElementById('btn-down').addEventListener('touchstart', () => movementInput.y = moveSpeed);
document.getElementById('btn-down').addEventListener('touchend', () => movementInput.y = 0);
document.getElementById('btn-left').addEventListener('touchstart', () => movementInput.x = -moveSpeed);
document.getElementById('btn-left').addEventListener('touchend', () => movementInput.x = 0);
document.getElementById('btn-right').addEventListener('touchstart', () => movementInput.x = moveSpeed);
document.getElementById('btn-right').addEventListener('touchend', () => movementInput.x = 0);

function update() {
    Body.setVelocity(playerBody, { x: movementInput.x * 3, y: movementInput.y * 3 });
"""

    if "coin" in p or "gold" in p:
        loop_code += """
    coins.forEach(coin => {
        if (!coin.collected) {
            const dx = playerBody.position.x - coin.x;
            const dy = playerBody.position.y - coin.y;
            if (Math.sqrt(dx * dx + dy * dy) < 24) {
                coin.collected = true;
                goldCount += 10;
                document.getElementById('hud').innerText = `HP: 100 | Gold: ${goldCount}`;
            }
        }
    });
"""

    if "attack" in p or "sword" in p:
        loop_code += """
    if (attackCooldown > 0) { attackCooldown--; if (attackCooldown === 0) isAttacking = false; }
"""

    if "enemy" in p or "goblin" in p:
        loop_code += """
    let edx = playerBody.position.x - enemy.x;
    let edy = playerBody.position.y - enemy.y;
    let edist = Math.sqrt(edx * edx + edy * edy);
    if (edist > 5) {
        enemy.x += (edx / edist) * enemy.speed;
        enemy.y += (edy / edist) * enemy.speed;
    }
"""

    loop_code += """
}

function render() {
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
"""

    if "coin" in p or "gold" in p:
        loop_code += """
    coins.forEach(coin => {
        if (!coin.collected) {
            ctx.fillStyle = '#f1c40f';
            ctx.beginPath();
            ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
            ctx.fill();
        }
    });
"""

    if "enemy" in p or "goblin" in p:
        loop_code += """
    ctx.fillStyle = '#e74c3c';
    ctx.beginPath();
    ctx.arc(enemy.x, enemy.y, enemy.radius, 0, Math.PI * 2);
    ctx.fill();
"""

    loop_code += """
    ctx.fillStyle = '#4a90e2';
    ctx.beginPath();
    ctx.arc(playerBody.position.x, playerBody.position.y, 16, 0, Math.PI * 2);
    ctx.fill();
"""

    if "attack" in p or "sword" in p:
        loop_code += """
    if (isAttacking) {
        ctx.strokeStyle = '#e74c3c';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(playerBody.position.x, playerBody.position.y, 32, 0, Math.PI * 2);
        ctx.stroke();
    }
"""

    loop_code += """
}

function gameLoop() { update(); render(); requestAnimationFrame(gameLoop); }
gameLoop();
console.log("Nexus Autonomous Build Active.");
"""

    return base_setup + features + loop_code

print("Nexus Core (Autonomous + Sequential Git Sync) initialized.")
while True:
    try:
        cmd = input("NexusCore> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif len(cmd.strip()) > 0:
            # Step 1: Reason and write code locally
            generated_code = think_and_generate_code(cmd)
            with open("game.js", "w", encoding="utf-8") as f:
                f.write(generated_code)
            print("[SUCCESS] game.js written locally.")
            
            # Step 2: Sequential Git Sync and Push
            print("[WORKING] Committing changes to git...")
            subprocess.run("git add .", shell=True, capture_output=True)
            subprocess.run(f'git commit -m "Autonomous update: {cmd[:30]}"', shell=True, capture_output=True)
            
            print("[WORKING] Pushing to GitHub repository...")
            res = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
            
            if res.returncode == 0:
                print("[SUCCESS] Successfully pushed to GitHub!\n")
            else:
                print(f"[NOTICE] Code updated locally (Git sync note: {res.stderr.strip()})\n")
        else:
            print("Please enter a valid command.")
    except KeyboardInterrupt:
        break
