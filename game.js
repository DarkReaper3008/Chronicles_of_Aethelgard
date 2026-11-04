// Game.js

// Initialize Matter.js world
const Engine = Matter.Engine;
const World = Matter.World;
const Bodies = Matter.Bodies;
const Constraint = Matter.Constraint;

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const engine = Engine.create();
const world = World.create();

// Set up the canvas
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Define the floor tile size
const tileWidth = 50;
const tileHeight = 50;

// Generate procedural floor tiles
function generateFloor() {
  for (let x = 0; x < canvas.width; x += tileWidth) {
    for (let y = 0; y < canvas.height; y += tileHeight) {
      const tile = Bodies.rectangle(x, y, tileWidth, tileHeight, { isStatic: true, render: { fillStyle: '#333' } });
      World.add(world, tile);
    }
  }
}

// Generate grid lines
function generateGridLines() {
  for (let x = 0; x < canvas.width; x += tileWidth) {
    const line = Bodies.rectangle(x, 0, 1, canvas.height, { isStatic: true, render: { fillStyle: '#333' } });
    World.add(world, line);
  }
  for (let y = 0; y < canvas.height; y += tileHeight) {
    const line = Bodies.rectangle(0, y, canvas.width, 1, { isStatic: true, render: { fillStyle: '#333' } });
    World.add(world, line);
  }
}

// Generate stone pillars
function generateStonePillars() {
  for (let i = 0; i < 10; i++) {
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    const pillar = Bodies.rectangle(x, y, 50, 50, { isStatic: true, render: { fillStyle: '#666' } });
    World.add(world, pillar);
  }
}

// Generate floating gold shards
function generateGoldShards() {
  for (let i = 0; i < 5; i++) {
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    const shard = Bodies.circle(x, y, 10, { isStatic: false, render: { fillStyle: '#FFD700' } });
    World.add(world, shard);
  }
}

// Update the game loop
function update() {
  Engine.update(engine);
  requestAnimationFrame(update);
}

// Start the game loop
update();

// Generate the floor, grid lines, stone pillars, and gold shards
generateFloor();
generateGridLines();
generateStonePillars();
generateGoldShards();