---
tags: [save, load, checkpoint, inventory, currency, persistence, json, localstorage]
---
# Save, Load & Checkpoint Guidelines
- Serialize the entire game state (player position, health, mana, coins, inventory array, equipped weapon/armor rank, and active checkpoint ID) into a single JSON object.
- Automatically trigger `localStorage.setItem('rpg_save', JSON.stringify(gameState))` upon reaching checkpoints or purchasing items.
- On game boot, check for existing save data, validate its structure, and restore the player seamlessly.
