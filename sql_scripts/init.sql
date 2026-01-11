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
