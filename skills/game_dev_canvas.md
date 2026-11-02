---
tags: [game, canvas, physics, sprites, touch, mobile, render, loop]
---
# Game Development & Canvas Guidelines
- Use a dedicated `requestAnimationFrame` loop with delta time (dt) calculations for smooth, frame-rate independent movement.
- Implement responsive mobile touch controls (virtual D-pad or swipe handlers) so games work seamlessly on Android.
- Keep game state isolated in a clean JSON object or class structure before rendering updates to the HTML5 canvas.
