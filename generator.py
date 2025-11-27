import datetime
from PIL import Image, ImageDraw, ImageFont
import uuid
import os
from moderation import passes_checks

TEMPLATE_PATH = "templates/default.jpg"
FONT_PATH = "fonts/DejaVuSans-Bold.ttf"   # embedded font


def get_text_size(draw, text, font):
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def load_font(h):
    """
    Always load the embedded font in /fonts/.
    No reliance on system fonts.
    """
    if not os.path.exists(FONT_PATH):
        raise RuntimeError(f"Embedded font not found: {FONT_PATH}")

    return ImageFont.truetype(FONT_PATH, size=int(h * 0.06))


def make_meme(text):
    out = f"static/generated_{uuid.uuid4().hex}.jpg"

    img = Image.open(TEMPLATE_PATH).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # load guaranteed embedded font
    font = load_font(h)

    words = text.split()
    lines = []
    line = ""
    max_width = int(w * 0.85)

    for word in words:
        test_line = (line + " " + word).strip()
        tw, th = get_text_size(draw, test_line, font)

        if tw <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)

    y = int(h * 0.6)

    for l in lines:
        tw, th = get_text_size(draw, l, font)
        x = (w - tw) // 2
        draw.text((x, y), l, font=font, fill="white")
        y += th + 10

    img.save(out, quality=85)
    return out


def compose_drafts(trends):
    drafts = []

    for t in trends[:4]:
        text = f"{t['title']} — {t.get('tagline','')} #trending"

        if not passes_checks(text):
            continue

        img = make_meme(t["title"])

        drafts.append({
            "text": text,
            "image_path": img,
            "created_at": datetime.datetime.utcnow().isoformat()
        })

    return drafts
