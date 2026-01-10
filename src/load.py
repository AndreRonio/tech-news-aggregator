import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch


def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "hn_db"),
        user=os.getenv("PGUSER", "hn_user"),
        password=os.getenv("PGPASSWORD", "hn_pass"),
    )


def create_table_if_not_exists(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS news_archive (
      story_id BIGINT PRIMARY KEY,
      title TEXT,
      url TEXT,
      domain TEXT,
      author TEXT,
      published_at_utc TIMESTAMPTZ,
      score INTEGER,
      comment_count INTEGER,
      first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def upsert_news_archive(conn, df: pd.DataFrame):
    upsert_sql = """
    INSERT INTO news_archive (
      story_id, title, url, domain, author, published_at_utc, score, comment_count,
      first_seen_at, last_seen_at
    )
    VALUES (
      %(story_id)s, %(title)s, %(url)s, %(domain)s, %(author)s, %(published_at_utc)s,
      %(score)s, %(comment_count)s,
      NOW(), NOW()
    )
    ON CONFLICT (story_id)
    DO UPDATE SET
      title = EXCLUDED.title,
      url = EXCLUDED.url,
      domain = EXCLUDED.domain,
      author = EXCLUDED.author,
      published_at_utc = EXCLUDED.published_at_utc,
      score = EXCLUDED.score,
      comment_count = EXCLUDED.comment_count,
      last_seen_at = NOW();
    """

    records = df.to_dict(orient="records")

    with conn.cursor() as cur:
        execute_batch(cur, upsert_sql, records, page_size=200)

    conn.commit()
