---
tags: [matter, physics, 2d, engine, collisions, gravity, javascript, spells]
---
# Matter.js Physics & Spell Mechanics Guidelines
- Include Matter.js via CDN (`<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>`) in your HTML files.
- Use `Matter.Engine`, `Matter.Render`, and `Matter.Runner` to set up the 2D world loop.
- For elemental spells (like fireballs or ice shards), create dynamic bodies with custom velocities and collision filters (`category` and `mask`) to handle damage interactions cleanly.
