// Chronicles of Aethelgard - Full Game Build with Background & FX
// Prompt: Add a Pause button to the top UI HUD that pauses the game loop and physics engine when clicked, and show a Pause menu overlay
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
    frictionAir: 0.1, restitution: 0.2, render: { fillStyle: '#4a90e2' }
});
Composite.add(engine.world, [playerBody]);

const runner = Runner.create();
Runner.run(runner, engine);

let goldCount = 0;
let playerHp = 100;
let movementInput = { x: 0, y: 0 };
const moveSpeed = 1.2;

let coins = [
    { x: canvas.width / 2 + 60, y: canvas.height / 2 - 40, radius: 8, collected: false },
    { x: canvas.width / 2 - 80, y: canvas.height / 2 + 60, radius: 8, collected: false }
];

let enemy = { x: canvas.width / 2 + 120, y: canvas.height / 2 + 120, radius: 14, speed: 0.5 };
let damageCooldown = 0;

let activeParticles = [];
function spawnPixelFX(x, y, color) {
    for (let i = 0; i < 12; i++) {
        activeParticles.push({
            x: x, y: y,
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4,
            alpha: 1.0,
            color: color
        });
    }
}
function updatePixelFX() {
    activeParticles.forEach(p => {
        p.x += p.vx; p.y += p.vy; p.alpha -= 0.03;
    });
    activeParticles = activeParticles.filter(p => p.alpha > 0);
}
function renderPixelFX() {
    activeParticles.forEach(p => {
        ctx.save();
        ctx.globalAlpha = p.alpha;
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, 4, 4);
        ctx.restore();
    });
}

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

    const margin = 30;
    if (playerBody.position.x < margin) Body.setPosition(playerBody, { x: margin, y: playerBody.position.y });
    if (playerBody.position.x > canvas.width - margin) Body.setPosition(playerBody, { x: canvas.width - margin, y: playerBody.position.y });
    if (playerBody.position.y < margin + 60) Body.setPosition(playerBody, { x: playerBody.position.x, y: margin + 60 });
    if (playerBody.position.y > canvas.height - margin) Body.setPosition(playerBody, { x: playerBody.position.x, y: canvas.height - margin });

    coins.forEach(coin => {
        if (!coin.collected) {
            const dx = playerBody.position.x - coin.x;
            const dy = playerBody.position.y - coin.y;
            if (Math.sqrt(dx * dx + dy * dy) < 24) {
                coin.collected = true;
                goldCount += 10;
                spawnPixelFX(coin.x, coin.y, '#f1c40f');
                document.getElementById('hud').innerText = `HP: ${playerHp} | Gold: ${goldCount}`;
            }
        }
    });

    let edx = playerBody.position.x - enemy.x;
    let edy = playerBody.position.y - enemy.y;
    let edist = Math.sqrt(edx * edx + edy * edy);
    if (edist > 2) {
        enemy.x += (edx / edist) * enemy.speed;
        enemy.y += (edy / edist) * enemy.speed;
    }

    if (damageCooldown > 0) damageCooldown--;
    if (edist < 26 && damageCooldown <= 0) {
        playerHp = Math.max(0, playerHp - 10);
        damageCooldown = 60;
        spawnPixelFX(playerBody.position.x, playerBody.position.y, '#e74c3c');
        document.getElementById('hud').innerText = `HP: ${playerHp} | Gold: ${goldCount}`;
    }

    updatePixelFX();
}

function render() {
    // 1. Render Fantasy Environment Background (Grid / Terrain Pattern)
    ctx.fillStyle = '#16192b'; // Deep fantasy night/dungeon tone
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#222742';
    ctx.lineWidth = 1;
    const gridSize = 40;
    for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }

    // 2. Render Coins
    coins.forEach(coin => {
        if (!coin.collected) {
            ctx.fillStyle = '#f1c40f';
            ctx.beginPath();
            ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
            ctx.fill();
        }
    });

    // 3. Render Enemy
    ctx.fillStyle = '#e74c3c';
    ctx.beginPath();
    ctx.arc(enemy.x, enemy.y, enemy.radius, 0, Math.PI * 2);
    ctx.fill();

    // 4. Render Player
    ctx.fillStyle = '#4a90e2';
    ctx.beginPath();
    ctx.arc(playerBody.position.x, playerBody.position.y, 16, 0, Math.PI * 2);
    ctx.fill();

    // 5. Render PixelFX Particle Overlays
    renderPixelFX();
}

function gameLoop() { update(); render(); requestAnimationFrame(gameLoop); }
gameLoop();
