---
tags: [enemy, guards, boss, summons, familiar, combat, hitboxes, AI]
---
# Entity Combat & AI Guidelines
- Implement a unified base `Entity` class for the player, enemies, guards, and bosses, handling position, velocity, health bars, and render states.
- Give bosses distinct phase states and check for specific "boss-killing weapon" flags during collision calculation to handle special damage modifiers.
- Use simple Euclidean distance checks for enemy and guard aggro ranges relative to the player's canvas coordinates.
