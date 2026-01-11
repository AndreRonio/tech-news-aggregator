-- analysis.sql
-- Useful validation / exploration queries for the Tech News Aggregator ETL

-- 1) How many rows are currently stored?
SELECT COUNT(*) AS total_rows
FROM news_archive;

-- 2) Time coverage of the data we have collected
SELECT
  MIN(first_seen_at) AS first_seen_min,
  MAX(last_seen_at)  AS last_seen_max
FROM news_archive;

-- 3) Latest 20 stories by when we last saw them in the top list
SELECT
  story_id,
  title,
  author,
  domain,
  score,
  comment_count,
  first_seen_at,
  last_seen_at
FROM news_archive
ORDER BY last_seen_at DESC
LIMIT 20;

-- 4) Top domains (most stories collected)
SELECT
  COALESCE(domain, '(null)') AS domain,
  COUNT(*) AS stories_count
FROM news_archive
GROUP BY 1
ORDER BY stories_count DESC
LIMIT 15;

-- 5) Stories that stayed visible for the longest time in our top list
-- (duration is approximate because the pipeline runs periodically)
SELECT
  story_id,
  title,
  domain,
  first_seen_at,
  last_seen_at,
  (last_seen_at - first_seen_at) AS visible_duration
FROM news_archive
ORDER BY visible_duration DESC
LIMIT 20;
