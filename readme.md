# 🖨️ Print Weekly Surprise

Print a random **comic**, **image**, and **quote** once per week through your CUPS printer. Keeping **inkjet printer heads from drying or clogging** when it isn’t used regularly for once a week "printer exercise".

---

## 💡 Why Use This?

Inkjet printers that sit idle for long periods often suffer from **dried print heads** and **ink flow problems**. This container suddenly prints a small page each week without warning, combining:

- 🎨 Random photo background
- 🧠 XKCD comic
- 💬 Short sometimes inspirational quote
- 💧 CMYK patch

---

## 🖨️ Tips for Inkjet Owners

- If your prints are too vivid or use too much ink, lower the background saturation by setting `BG_SATURATION=0.5` (or even `0.3`) to mute the image while keeping the comic and text clear.

---

## ⚙️ Recommended Settings for your NAS

When creating the container:

1. **Network Mode** → select **Host** (local CUPS communication works reliably)
2. **Restart Policy** → select **Always** (survive NAS reboots)
3. Mount a shared folder to `/data` to keep print history.

---

## 📁 Data Persistence

Each generated print is saved in `/data/history/` inside the container.
To keep your archive between restarts, mount a host folder:

```bash
-v /volume1/print-weekly-surprise:/data
````

---

## 🕒 Scheduling

The print job runs via **cron**.
By default it’s set to **Mondays at 09:30 (UTC)**.
You can change this with the `CRON` variable, using standard cron syntax:

```
-e CRON="0 12 * * FRI"  # Fridays at 12:00 UTC
```

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

---

## 🧩 Environment Variables

| Variable        | Default         | Description                        |
| --------------- | --------------- | ---------------------------------- |
| `TZ`            | `Etc/UTC`       | Timezone for cron scheduling       |
| `CRON`          | `30 9 * * MON`  | Schedule (cron syntax)             |
| `PRINT`         | `1`             | Set to `0` for preview-only mode   |
| `PAPER`         | `A4`            | Paper size (`A4` or `LETTER`)      |
| `CUPS_HOST`     | `127.0.0.1:631` | Your CUPS server address           |
| `QUEUE`         | `epson-et1810`  | CUPS printer queue name            |
| `BG_SATURATION` | `0.7`           | 0–1 multiplier to reduce ink usage |

---

**Maintainer:** [kequc](https://hub.docker.com/u/kequc)
**Source:** [github.com/kequtech/print-weekly-surprise](https://github.com/kequtech/print-weekly-surprise)

```
