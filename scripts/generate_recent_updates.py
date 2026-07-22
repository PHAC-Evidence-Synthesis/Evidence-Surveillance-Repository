from pathlib import Path
import csv
import hashlib
import json
import urllib.request
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

SOURCES_FILE = ROOT / "data" / "google-sheet-sources.csv"
STATE_FILE = ROOT / "data" / "sheet-update-state.json"
OUTPUT_FILE = ROOT / "_recent-updates.md"


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def fetch_csv_hash(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()

    return hashlib.sha256(data).hexdigest()


def load_sources():
    if not SOURCES_FILE.exists():
        return []

    with SOURCES_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_recent_updates(state):
    updates = []

    for slug, item in state.items():
        if item.get("updated"):
            updates.append({
                "slug": slug,
                "title": item.get("title", slug.replace("-", " ").title()),
                "updated": item["updated"]
            })

    updates = sorted(updates, key=lambda x: x["updated"], reverse=True)[:5]

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write("## Recently updated\n\n")
        f.write("This section is generated automatically from linked Google Sheet data sources.\n\n")

        if not updates:
            f.write("No linked datasets have been checked yet.\n")
            return

        f.write("::: {.card-grid}\n\n")

        for update in updates:
            f.write("::: {.info-card}\n")
            f.write(f"### {update['title']}\n\n")
            f.write(f"**Updated:** {update['updated']}\n\n")
            f.write(f"[View table](outbreaks/{update['slug']}/)\n")
            f.write(":::\n\n")

        f.write(":::\n")


def main():
    state = load_state()
    sources = load_sources()

    for source in sources:
        slug = source.get("slug", "").strip()
        title = source.get("title", "").strip()
        url = source.get("url", "").strip()

        if not slug or not url:
            continue

        try:
            current_hash = fetch_csv_hash(url)
        except Exception as e:
            print(f"Could not check {slug}: {e}")
            continue

        previous = state.get(slug, {})
        previous_hash = previous.get("hash")

        if previous_hash != current_hash:
            state[slug] = {
                "title": title or previous.get("title", slug.replace("-", " ").title()),
                "url": url,
                "hash": current_hash,
                "updated": today()
            }
        else:
            state[slug] = {
                **previous,
                "title": title or previous.get("title", slug.replace("-", " ").title()),
                "url": url,
                "hash": current_hash
            }

    save_state(state)
    write_recent_updates(state)


if __name__ == "__main__":
    main()
