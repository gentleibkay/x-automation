import datetime
from PIL import Image, ImageDraw, ImageFont
import uuid
import os
from moderation import passes_checks

TEMPLATE_PATH = "templates/default.jpg"


def get_text_size(draw, text, font):
    """
    Pillow 10+ replacement for deprecated textsize().
    Uses textbbox() instead.
    """
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def load_font(h):
    """
    Safe cross-platform font loader.
    Render (Linux) includes DejaVuSans by default.
    macOS fallback included for local development.
    """

    # Linux-safe built-in font
    linux_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    # Fallbacks for safety (macOS paths included)
    fallback_fonts = [
        linux_font,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]

    font_path = None
    for f in fallback_fonts:
        if os.path.exists(f):
            font_path = f
            break

    if font_path is None:
        raise RuntimeError("No usable system font found")

    return ImageFont.truetype(font_path, size=int(h * 0.06))


def make_meme(text):
    """
    Creates meme-style image by overlaying wrapped text on template.
    Saves output inside /static so Flask can serve it.
    """
    # Output path inside static/
    out = f"static/generated_{uuid.uuid4().hex}.jpg"

    # Load template
    img = Image.open(TEMPLATE_PATH).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # Load safe font
    font = load_font(h)

    # -------- TEXT WRAPPING -------- #
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

    # -------- DRAW TEXT -------- #
    y = int(h * 0.6)

    for l in lines:
        tw, th = get_text_size(draw, l, font)
        x = (w - tw) // 2

        # Draw text with light white color
        draw.text((x, y), l, font=font, fill="white")
        y += th + 10

    # -------- SAVE OUTPUT -------- #
    img.save(out, quality=85)
    return out


def compose_drafts(trends):
    """
    Generates up to 4 draft posts with meme images.
    Returns list of dictionaries saved into DB.
    """

    drafts = []

    for t in trends[:4]:
        text = f"{t['title']} — {t.get('tagline','')} #trending"

        if not passes_checks(text):
            continue

        # Generate meme image
        img = make_meme(t["title"])

        drafts.append({
            "text": text,
            "image_path": img,
            "created_at": datetime.datetime.utcnow().isoformat()
        })

    return drafts
