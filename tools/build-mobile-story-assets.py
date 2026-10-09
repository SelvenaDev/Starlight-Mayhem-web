from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'assets/images/menucharacters'
SCALE = 0.5
for png in sorted(BASE.glob('*.png')):
    out = png.with_name(png.stem + '-mobile.png')
    with Image.open(png) as im:
        im.convert('RGBA').resize((max(1,round(im.width*SCALE)), max(1,round(im.height*SCALE))), Image.Resampling.LANCZOS).save(out, optimize=True)
    xml = png.with_suffix('.xml')
    if xml.exists():
        tree = ET.parse(xml); root = tree.getroot()
        for e in root.iter():
            if e.tag.lower().endswith('subtexture'):
                for k in ('x','y','width','height','frameX','frameY','frameWidth','frameHeight'):
                    if k in e.attrib: e.attrib[k] = str(round(float(e.attrib[k])*SCALE))
        root.set('imagePath', out.name)
        ET.indent(tree, space='  ')
        tree.write(out.with_suffix('.xml'), encoding='utf-8', xml_declaration=True)
print('generated mobile MenuCharacter assets')
