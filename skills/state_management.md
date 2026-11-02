---
tags: [save, load, state, json, localstorage, persistence, rpg, inventory]
---
# RPG State Management & Persistence Guidelines
- Store all core game variables (player stats, inventory items, unlocked spells, quest progress) in a clean JSON state object.
- Implement robust `saveGame()` and `loadGame()` functions using `localStorage` so player progress persists across browser refreshes or app closures.
- Validate saved data structures on load to prevent crashes from corrupted or outdated save files.
