import os
from PIL import Image, ImageDraw, ImageFont
import uuid


def make_image(text):
    os.makedirs("static/images", exist_ok=True)

    filename = f"static/images/{uuid.uuid4().hex}.jpg"
    img = Image.new("RGB", (700, 700), (20, 20, 20))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    draw.text((20, 300), text, fill=(255, 255, 255), font=font)

    img.save(filename, "JPEG")
    return filename


def compose_drafts(trends):
    drafts = []
    for t in trends[:4]:
        img_path = make_image(t)
        drafts.append({
            "text": t,
            "image_path": img_path
        })
    return drafts
