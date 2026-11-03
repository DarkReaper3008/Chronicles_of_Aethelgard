// Game setup
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 600;

// Matter.js setup
const engine = Matter.Engine.create();
const world = engine.world;

// Canvas boundaries
const boundary = Matter.Bodies.rectangle(canvas.width / 2, canvas.height / 2, canvas.width, canvas.height, { isStatic: true });
world.add(boundary);

// Kaelen the elemental character
const kaelen = Matter.Bodies.circle(canvas.width / 2, canvas.height / 2, 50, { mass: 10, friction: 0.5, restitution: 0.7 });
world.add(kaelen);

// Kaelen's sprite
const kaelenSprite = document.createElement('img');
kaelenSprite.src = 'kaelen.png';
kaelenSprite.style.position = 'absolute';
kaelenSprite.style.left = `${canvas.width / 2 - kaelenSprite.width / 2}px`;
kaelenSprite.style.top = `${canvas.height / 2 - kaelenSprite.height / 2}px`;
kaelenSprite.style.zIndex = 100;
document.body.appendChild(kaelenSprite);

// Kaelen's ponytail physics
const ponytail = Matter.Bodies.rectangle(canvas.width / 2, canvas.height / 2, 100, 20, { isStatic: true });
world.add(ponytail);

// Kaelen's animation frames
const kaelenFrames = [
  { src: 'kaelen1.png', x: 0, y: 0, width: 50, height: 50 },
  { src: 'kaelen2.png', x: 50, y: 0, width: 50, height: 50 },
  { src: 'kaelen3.png', x: 100, y: 0, width: 50, height: 50 },
  { src: 'kaelen4.png', x: 150, y: 0, width: 50, height: 50 }
];

let kaelenFrameIndex = 0;
let kaelenFrameTimer = 0;

// Kaelen's sprite animation
function animateKaelen() {
  kaelenFrameTimer++;
  if (kaelenFrameTimer >= 10) {
    kaelenFrameTimer = 0;
    kaelenFrameIndex = (kaelenFrameIndex + 1) % kaelenFrames.length;
  }
  const frame = kaelenFrames[kaelenFrameIndex];
  kaelenSprite.style.transform = `translate(${kaelenSprite.offsetLeft + frame.x}px, ${kaelenSprite.offsetTop + frame.y}px)`;
}
setInterval(animateKaelen, 100);

// Kaelen's movement
let kaelenVelocity = { x: 0, y: 0 };
document.addEventListener('touchstart', (e) => {
  const touch = e.touches[0];
  kaelenVelocity.x = touch.clientX - canvas.width / 2;
  kaelenVelocity.y = touch.clientY - canvas.height / 2;
});
document.addEventListener('touchmove', (e) => {
  const touch = e.touches[0];
  kaelenVelocity.x = touch.clientX - canvas.width / 2;
  kaelenVelocity.y = touch.clientY - canvas.height / 2;
});
document.addEventListener('touchend', () => {
  kaelenVelocity.x = 0;
  kaelenVelocity.y = 0;
});

// Kaelen's electrostatic spark animation
const sparkFrames = [
  { src: 'spark1.png', x: 0, y: 0, width: 10, height: 10 },
  { src: 'spark2.png', x: 10, y: 0, width: 10, height: 10 },
  { src: 'spark3.png', x: 20, y: 0, width: 10, height: 10 },
  { src: 'spark4.png', x: 30, y: 0, width: 10, height: 10 }
];

let sparkFrameIndex = 0;
let sparkFrameTimer = 0;

// Kaelen's sprite animation
function animateSpark() {
  sparkFrameTimer++;
  if (sparkFrameTimer >= 10) {
    sparkFrameTimer = 0;
    sparkFrameIndex = (sparkFrameIndex + 1) % sparkFrames.length;
  }
  const frame = sparkFrames[sparkFrameIndex];
  sparkSprite.style.transform = `translate(${sparkSprite.offsetLeft + frame.x}px, ${sparkSprite.offsetTop + frame.y}px)`;
}
setInterval(animateSpark, 100);

// Kaelen's sprite animation
function animateKaelen() {
  kaelenFrameTimer++;
  if (kaelenFrameTimer >= 10) {
    kaelenFrameTimer = 0;
    kaelenFrameIndex = (kaelenFrameIndex + 1) % kaelenFrames.length;
  }
  const frame = kaelenFrames[kaelenFrameIndex];
  kaelenSprite.style.transform = `translate(${kaelenSprite.offsetLeft + frame.x}px, ${kaelenSprite.offsetTop + frame.y}px)`;
}
setInterval(animateKaelen, 100);

// Game loop
function gameLoop() {
  Matter.Engine.update(engine);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  Matter.Body.render(engine, ctx);
  requestAnimationFrame(gameLoop);
}
gameLoop();