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
let movementInput = { x: 0, y: 0 };
const moveSpeed = 1.2;

let coins = [
    { x: canvas.width / 2 + 60, y: canvas.height / 2 - 40, radius: 8, collected: false },
    { x: canvas.width / 2 - 80, y: canvas.height / 2 + 60, radius: 8, collected: false }
];

let enemy = { x: canvas.width / 2 + 120, y: canvas.height / 2 + 120, radius: 14, speed: 0.6 };

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

    let edx = playerBody.position.x - enemy.x;
    let edy = playerBody.position.y - enemy.y;
    let edist = Math.sqrt(edx * edx + edy * edy);
    if (edist > 5) {
        enemy.x += (edx / edist) * enemy.speed;
        enemy.y += (edy / edist) * enemy.speed;
    }

}

function render() {
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    coins.forEach(coin => {
        if (!coin.collected) {
            ctx.fillStyle = '#f1c40f';
            ctx.beginPath();
            ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
            ctx.fill();
        }
    });

    ctx.fillStyle = '#e74c3c';
    ctx.beginPath();
    ctx.arc(enemy.x, enemy.y, enemy.radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#4a90e2';
    ctx.beginPath();
    ctx.arc(playerBody.position.x, playerBody.position.y, 16, 0, Math.PI * 2);
    ctx.fill();

}

function gameLoop() { update(); render(); requestAnimationFrame(gameLoop); }
gameLoop();
console.log("Nexus Autonomous Build Active.");
