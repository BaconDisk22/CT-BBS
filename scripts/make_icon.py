"""Package the approved reference-style artwork; never replace it with a placeholder."""
from pathlib import Path
from PIL import Image

source = Path(__file__).resolve().parents[1] / 'assets' / 'jersey-icon.png'
with Image.open(source) as artwork:
    icon = artwork.convert('RGBA').resize((1024, 1024), Image.Resampling.LANCZOS)
Path('build').mkdir(exist_ok=True)
icon.save('build/sitdown-icon.png')
Path('docs/images').mkdir(parents=True, exist_ok=True)
icon.save('docs/images/app-icon.png')
