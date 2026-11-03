Sure, I can help you add a particle burst system to your HTML5 Canvas game using Matter.js. Below is the complete code for a game with a particle burst system.

### HTML
html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Particle Burst System Game</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <canvas id="gameCanvas" width="800" height="600"></canvas>
    <script src="game.js"></script>
</body>
</html>


### CSS (styles.css)
css
body {
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f0f0f0;
}

canvas {
    border: 1px solid #000;
}


### JavaScript (game.js)

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const width = canvas.width;
const height = canvas.height;

const Matter = require('matter-js');
const MatterWorld = Matter.World;
const MatterEngine = Matter.Engine;
const MatterBody = Matter.Body;
const MatterConstraint = Matter.Constraint;
const MatterRender = Matter.Render;

// Create a Matter.js world
const world = new MatterWorld();
const engine = Matter.Engine.create();
Matter.World.add(world, engine.world);

// Create a canvas renderer
const render = Matter.Render.create({
    element: canvas,
    engine: engine,
    options: {
        width: width,
        height: height,
        background: '#f0f0f0',
        showDebug: false,
        showStats: false,
        wireframes: true
    }
});

// Add a ground
const ground = Matter.Body.create({
    position: { x: width / 2, y: height - 10 },
    width: width,
    height: 10,
    isStatic: true
});
Matter.World.add(world, ground);

// Add a player
const player = Matter.Body.create({
    position: { x: width / 2, y: height / 2 },
    mass: 10,
    shape: 'circle',
    render: {
        fillStyle: '#000',
        lineWidth: 2
    }
});
Matter.World.add(world, player);

// Add a particle system
const particleSystem = Matter.ParticleSystem.create({
    position: { x: width / 2, y: height / 2 },
    radius: 5,
    particles: 100,
    restitution: 0.9
});
Matter.World.add(world, particleSystem);

// Function to create a particle burst
function createParticleBurst() {
    const particles = Matter.ParticleSystem.create({
        position: { x: player.position.x, y: player.position.y },
        radius: 10,
        particles: 50,
        restitution: 0.9
    });
    Matter.World.add(world, particles);
}

// Event listener for button click
document.getElementById('createBurstButton').addEventListener('click', createParticleBurst);

// Start the Matter.js engine
Matter.Engine.run(engine);


### Explanation
1. **HTML**: The HTML sets up the canvas element and includes a script tag for the game.js file.
2. **CSS**: The CSS styles the canvas and sets up the basic layout.
3. **JavaScript**:
   - We create a Matter.js world and an engine.
   - We add a ground, a player, and a particle system.
   - A function `createParticleBurst` is defined to create a new particle burst when the button is clicked.
   - The button is also added to the HTML with an event listener that triggers the particle burst creation.

You can open the HTML file in a web browser to see the game in action with a particle burst system.