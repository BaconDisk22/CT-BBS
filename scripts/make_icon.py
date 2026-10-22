"""Package the approved reference-style artwork; never replace it with a placeholder."""
from pathlib import Path
from PIL import Image

source = Path(__file__).resolve().parents[1] / 'assets' / 'ct-icon.png'
with Image.open(source) as artwork:
    icon = artwork.convert('RGBA').resize((1024, 1024), Image.Resampling.LANCZOS)
Path('build').mkdir(exist_ok=True)
icon.save('build/packy-icon.png')
Path('docs/images').mkdir(parents=True, exist_ok=True)
icon.save('docs/images/app-icon.png')
