// Chronicles of Aethelgard - Phase 1 Core Engine
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
