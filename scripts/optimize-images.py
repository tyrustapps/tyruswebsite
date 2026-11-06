"""Regenerate web assets from the approved original; requires Pillow (authoring only)."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'dist' / 'assets'
OUTPUT.mkdir(parents=True, exist_ok=True)
image = Image.open(ROOT / 'assets/source/coastal-ai-sunset.png').convert('RGB')
for width in [768, 1200, 1672]:
    resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
    resized.save(OUTPUT / f'coastal-ai-{width}.webp', quality=82, method=6)
image.save(OUTPUT / 'coastal-ai-fallback.jpg', quality=82, optimize=True, progressive=True)
image.resize((1200, 675), Image.Resampling.LANCZOS).save(OUTPUT / 'tyrus-social.jpg', quality=80, optimize=True)
