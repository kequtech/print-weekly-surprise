#!/usr/bin/env python3
import os, io, json, random, datetime, subprocess, ssl, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# -------------- CONFIG --------------
DPI = 300
PAPER = os.getenv("PAPER", "A4").upper()
BG_SATURATION = float(os.getenv("BG_SATURATION", "0.7"))

if PAPER == "LETTER":
    W, H = int(8.5 * DPI), int(11 * DPI)
else:
    W, H = round(210 / 25.4 * DPI), round(297 / 25.4 * DPI)

MARGIN, GAP = int(15 / 25.4 * DPI), int(6 / 25.4 * DPI)
CUPS_HOST = os.getenv("CUPS_HOST", "127.0.0.1:631")
QUEUE = os.getenv("QUEUE", "epson-et1810")
PRINT = os.getenv("PRINT", "1") != "0"
OUT_DIR = "/data/history"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def make_archive_path():
    date_part = datetime.datetime.now().strftime("%Y-%m-%d")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    while True:
        suffix = "".join(random.choice(alphabet) for _ in range(4))
        path = os.path.join(OUT_DIR, f"{date_part}-{suffix}.jpg")
        if not os.path.exists(path):
            return path

OUT_PATH = make_archive_path()
ssl_ctx = ssl._create_unverified_context()

# -------------- HELPERS --------------
def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20, context=ssl_ctx) as r:
            return r.read()
    except Exception as e:
        print(f"[printbot] WARN: {url} failed: {e}")
        return b""

def load_font(pt):
    try: return ImageFont.truetype(FONT_PATH, pt)
    except: return ImageFont.load_default()

def fit_cover(img, w, h):
    iw, ih = img.size
    s = max(w/iw, h/ih)
    img = img.resize((int(iw*s), int(ih*s)), Image.LANCZOS)
    x, y = (img.width-w)//2, (img.height-h)//2
    return img.crop((x, y, x+w, y+h))

def fit_within(img, mw, mh):
    iw, ih = img.size
    s = min(mw/iw, mh/ih)
    return img.resize((int(iw*s), int(ih*s)), Image.LANCZOS)

# -------------- FETCH CONTENT --------------
def random_photo():
    img = Image.open(io.BytesIO(get("https://picsum.photos/2200/3300.jpg"))).convert("RGB")
    if BG_SATURATION < 1.0:
        img = ImageEnhance.Color(img).enhance(BG_SATURATION)
    return img

def random_xkcd():
    latest = json.loads(get("https://xkcd.com/info.0.json") or b'{"num":2500}')["num"]
    n = random.randint(1, latest)
    info = json.loads(get(f"https://xkcd.com/{n}/info.0.json") or b'{}')
    img = Image.open(io.BytesIO(get(info.get("img","")) or get("https://imgs.xkcd.com/comics/standards.png"))).convert("RGB")
    return img, info.get("safe_title", "xkcd")

def random_quote_parts():
    q = json.loads(get("https://api.quotable.io/random?maxLength=200") or b'{"content":"Be kind whenever possible.","author":"Dalai Lama"}')
    return q["content"], q["author"]

# -------------- MAIN --------------
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    bg = fit_cover(random_photo(), W, H)
    d  = ImageDraw.Draw(bg)

    # Header date
    date = datetime.date.today().strftime("%A, %d %B %Y")
    f_date = load_font(40)
    tw, th = d.textbbox((0,0), date, font=f_date)[2:]
    chip = Image.new("RGBA", (tw+24, th+12), (255,255,255,200))
    bg.paste(chip, (W - tw - 24 - MARGIN, MARGIN), chip)
    d.text((W - tw - 12 - MARGIN, MARGIN + 6), date, fill=(0,0,0), font=f_date)

    # Comic
    comic, _ = random_xkcd()
    top_y = MARGIN + int(20 / 25.4 * DPI)
    max_w = int(W * 0.74)
    max_h = int(H * 0.55)
    comic = fit_within(comic, max_w, max_h)
    cx = (W - comic.width) // 2
    cy = top_y
    bg.paste(comic, (cx, cy))

    # Quote
    quote_text, author = random_quote_parts()
    qx, qy = cx, cy + comic.height + GAP
    avail_w = comic.width - 40
    avail_h = H - MARGIN - qy
    size = 72
    min_size = 28

    while size >= min_size:
        f_q = load_font(size)
        f_a = load_font(max(min_size, int(size * 0.78)))
        lines, line = [], ""
        for word in quote_text.split():
            test = (line + " " + word).strip()
            if d.textlength(test, font=f_q) > avail_w:
                if line: lines.append(line)
                line = word
            else:
                line = test
        if line: lines.append(line)
        line_h = size + 12
        author_h = int(f_a.size + 10)
        total_h = len(lines) * line_h + author_h + 48
        if total_h <= avail_h:
            overlay = Image.new("RGBA", (comic.width, total_h), (255,255,255,190))
            bg.paste(overlay, (qx, qy), overlay)
            y = qy + 20
            for ln in lines:
                tw_ln = d.textlength(ln, font=f_q)
                x = qx + (comic.width - tw_ln)//2
                d.text((x, y), ln, fill=(0,0,0), font=f_q)
                y += line_h
            author_line = f"— {author}"
            tw_a = d.textlength(author_line, font=f_a)
            ax = qx + (comic.width - tw_a)//2
            d.text((ax, y + 8), author_line, fill=(0,0,0), font=f_a)
            break
        size -= 4

    # CMYK patch
    s, pad = int(12 / 25.4 * DPI), int(10 / 25.4 * DPI)
    x0, y0 = W - pad - s*4 - 9, H - pad - s
    for i, c in enumerate([(0,255,255),(255,0,255),(255,255,0),(0,0,0)]):
        x = x0 + i*(s+3)
        d.rectangle((x, y0, x+s, y0+s), fill=c, outline=(40,40,40))

    # Save + print
    bg.save(OUT_PATH, quality=95)
    print(f"[printbot] archived {OUT_PATH}")
    if PRINT:
        subprocess.run(["lp", "-h", CUPS_HOST, "-d", QUEUE, "-o", f"media={PAPER}", "-o", "fit-to-page", OUT_PATH])
        print("[printbot] sent to printer")
    else:
        print("[printbot] preview mode (PRINT=0)")

if __name__ == "__main__":
    main()
