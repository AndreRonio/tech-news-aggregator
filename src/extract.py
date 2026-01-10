import time
import requests
from typing import Optional, Dict, List, Any

BASE = "https://hacker-news.firebaseio.com/v0"
session = requests.Session()

def fetch_item(item_id: int) -> Optional[Dict[str, Any]]:
    r = session.get(f"{BASE}/item/{item_id}.json", timeout=30)
    r.raise_for_status()
    return r.json()

def fetch_top_ids() -> List[int]:
    r = session.get(f"{BASE}/topstories.json", timeout=30)
    r.raise_for_status()
    return r.json()

def top_stories_only(limit: int = 20, pause: float = 0.05) -> List[Dict[str, Any]]:
    top_ids = fetch_top_ids()  # up to 500
    stories: List[Dict[str, Any]] = []

    for item_id in top_ids:
        data = fetch_item(item_id)
        time.sleep(pause)

        if not data:
            continue

        if data.get("type") != "story":
            continue

        if data.get("deleted") or data.get("dead"):
            continue

        stories.append(data)

        if len(stories) == limit:
            break

    return stories
