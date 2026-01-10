from extract import top_stories_only
from transform import transform_stories_to_df
from load import get_conn, create_table_if_not_exists, upsert_news_archive


def run(limit: int = 20):
    stories = top_stories_only(limit=limit)
    df = transform_stories_to_df(stories)

    conn = get_conn()
    try:
        create_table_if_not_exists(conn)
        upsert_news_archive(conn, df)
    finally:
        conn.close()

    print(f"ETL completed. Loaded/Upserted rows: {len(df)}")


if __name__ == "__main__":
    run()
