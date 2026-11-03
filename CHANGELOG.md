# Chronicles of Aethelgard - Development Changelog

## Phase 2: Physics and Collisions (Current)
* **Matter.js Integration:** Replaced basic coordinate movement with rigid-body physics bodies and zeroed-out vertical gravity for top-down isometric view.
* **Castle Wall Obstacles:** Added static rectangular body barriers for the player to collide against.
* **Mobile Touch Optimization:** Added `touch-action: manipulation` and disabled default text selection callouts (`user-select: none`) to prevent the browser's "Copy / Select all" popup menu from overlapping virtual D-pad buttons.

## Phase 1: Core Engine
* Initialized HTML5 Canvas and responsive viewport scaling.
* Created virtual touch D-pad and action button layout.
* Set up local Python server testing environment on port 8081.

- **Update**: `atmospheric fantasy background` (Synced with Background & PixelFX Pipeline)
- **Update**: `Add a Game Over overlay screen when playerHp reaches 0 with a restart button, and polish the HUD styling` (Synced with Background & PixelFX Pipeline)
- **Update**: `Add a Pause button to the top UI HUD that pauses the game loop and physics engine when clicked, and show a Pause menu overlay` (Synced with Background & PixelFX Pipeline)