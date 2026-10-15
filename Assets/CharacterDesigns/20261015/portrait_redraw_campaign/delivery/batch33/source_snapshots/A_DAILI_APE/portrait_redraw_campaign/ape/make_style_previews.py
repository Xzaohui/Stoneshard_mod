from pathlib import Path
from PIL import Image
W=Path(__file__).resolve().parent
for name in ["mara","iwo","leiya","tore"]:
    image=Image.open(W/f"sources/{name}_style_reference.png")
    image.resize((image.width*8,image.height*8),Image.Resampling.NEAREST).save(W/f"sources/{name}_style_reference_8x.png")
