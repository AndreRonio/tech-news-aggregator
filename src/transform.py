from urllib.parse import urlparse
from typing import Any, Dict, List

import pandas as pd


def extract_domain(url: Any) -> str | None:
    if not isinstance(url, str) or url.strip() == "":
        return None

    u = url.strip()
    p = urlparse(u)

    host = p.netloc.lower()

    # handle urls without scheme
    if host == "" and "://" not in u:
        host = urlparse("https://" + u).netloc.lower()

    if host.startswith("www."):
        host = host[4:]

    return host or None


def transform_stories_to_df(stories: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Takes raw HN story dicts and returns a cleaned dataframe ready for loading.
    """
    df = pd.DataFrame(stories)

    # keep only relevant cols (some may be missing)
    cols = ["id", "title", "url", "by", "time", "score", "descendants"]
    df = df.reindex(columns=cols)

    # unix -> datetime (UTC)
    df["published_at_utc"] = pd.to_datetime(df["time"], unit="s", utc=True)

    # domain from url (null-safe)
    df["domain"] = df["url"].apply(extract_domain)

    # rename for postgres
    df = df.rename(columns={
        "id": "story_id",
        "by": "author",
        "descendants": "comment_count",
    })

    # final order
    df = df.reindex(columns=[
        "story_id",
        "title",
        "url",
        "domain",
        "author",
        "published_at_utc",
        "score",
        "comment_count",
    ])

    return df
