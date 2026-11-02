import os
from PIL import Image, ImageDraw

def generate_tile(filename="tile.png", color=(70, 130, 180)):
    os.makedirs("/storage/emulated/0/Download/MyGameScripts/assets", exist_ok=True)
    path = f"/storage/emulated/0/Download/MyGameScripts/assets/{filename}"
    
    # Create a 32x32 pixel art canvas
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a styled block with a border
    draw.rectangle([2, 2, 29, 29], fill=color, outline=(20, 20, 20), width=2)
    draw.rectangle([5, 5, 10, 10], fill=(255, 255, 255, 100)) # Highlight
    
    img.save(path)
    print(f"[+] Generated 2D Sprite: {path}")

if __name__ == "__main__":
    generate_tile("platform_block.png", (46, 139, 87))
    generate_tile("coin_icon.png", (255, 215, 0))
