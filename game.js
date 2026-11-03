// Chronicles of Aethelgard - Phase 4 Gold Coins & Inventory Active
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
const wall2 = Bodies.rectangle(canvas.width / 2 - 100, canvas.height / 2 + 50, 20, 150, { isStatic: true });

Composite.add(engine.world, [playerBody, wall1, wall2]);

const runner = Runner.create();
Runner.run(runner, engine);

let goldCount = 0;
let coins = [
    { x: canvas.width / 2 + 60, y: canvas.height / 2 - 40, radius: 8, collected: false },
    { x: canvas.width / 2 - 80, y: canvas.height / 2 + 60, radius: 8, collected: false },
    { x: canvas.width / 2 + 90, y: canvas.height / 2 + 80, radius: 8, collected: false }
];

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

    coins.forEach(coin => {
        if (!coin.collected) {
            const dx = playerBody.position.x - coin.x;
            const dy = playerBody.position.y - coin.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < 24) {
                coin.collected = true;
                goldCount += 10;
                document.getElementById('hud').innerText = `HP: 100 | Gold: ${goldCount}`;
            }
        }
    });
}

function drawIsometricTilemap() {
    const tileWidth = 64;
    const tileHeight = 32;
    const cols = 12;
    const rows = 12;
    const startX = canvas.width / 2;
    const startY = canvas.height / 4;

    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
            const x = startX + (col - row) * (tileWidth / 2);
            const y = startY + (col + row) * (tileHeight / 2);

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

    coins.forEach(coin => {
        if (!coin.collected) {
            ctx.fillStyle = '#f1c40f';
            ctx.beginPath();
            ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.lineWidth = 1.5;
            ctx.strokeStyle = '#d4ac0d';
            ctx.stroke();
        }
    });

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
console.log("Chronicles of Aethelgard Gold Coins Active.");
