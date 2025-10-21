# 🖨️ Print Weekly Surprise

Automatically prints a random **comic**, **image**, and **quote** once per week through your CUPS printer. For keeping your **inkjet printer heads from drying or clogging** when it isn’t used regularly. A self-contained “printer exercise” container that surprises you every week.

---

## 💡 Why Use This?

Inkjet printers that sit unused for long periods often suffer from **dried print heads** and **ink flow problems**. It suddenly and surprisingly prints something once a week. Combining an XKCD comic, a random photo, and a short motivational quote so your printer stays happy.

---

## 🖨️ Tips for Inkjet Owners”:

If your prints are too vivid or use too much ink, set BG_SATURATION=0.5 (or even 0.3) to lighten the background colors while keeping the comic and text sharp.

---

### 📁 Data Persistence

This container saves every printed page to `/data/history/`.
If you want to keep your print history between container restarts, mount a host folder to `/data`:

---

## 🚀 Quick Start

```bash
docker run -d \
  --name print-weekly-surprise \
  --network host \
  -v /volume1/print-weekly-surprise:/data \
  -e TZ=Etc/UTC \
  -e CRON="30 9 * * MON" \
  -e PRINT=1 \
  -e PAPER=A4 \
  -e QUEUE=epson-et1810 \
  -e CUPS_HOST=127.0.0.1:631 \
  -e BG_SATURATION=0.7 \
  --restart unless-stopped \
  kequc/print-weekly-surprise:latest
```
