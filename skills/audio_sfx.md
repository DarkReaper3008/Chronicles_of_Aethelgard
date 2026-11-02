---
tags: [audio, sound, sfx, music, webaudio, synth, combat, spells]
---
# Audio & Procedural Sound FX Guidelines
- Use the native browser `AudioContext` API to generate retro sound effects programmatically (e.g., oscillator frequency sweeps for sword swings, spell casts, and coin pickups) to avoid missing asset crashes.
- Maintain separate volume controls for background ambient medieval music and active combat sound effects.
