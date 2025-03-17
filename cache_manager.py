import psycopg2
from datetime import datetime
import os
import json
from logger import logger

class CacheManager:
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self._init_db()

    def _init_db(self):
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS stock_cache (
                        id SERIAL PRIMARY KEY,
                        symbol VARCHAR(10),
                        start_date DATE,
                        end_date DATE,
                        data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()

    def cache_data(self, symbol, start_date, end_date, data):
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO stock_cache (symbol, start_date, end_date, data)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (symbol, start_date, end_date) 
                        DO UPDATE SET data = EXCLUDED.data
                    """, (symbol, start_date, end_date, json.dumps(data)))
                    conn.commit()
                    logger.info(f"Cached data for {symbol} from {start_date} to {end_date}")
        except Exception as e:
            logger.error(f"Failed to cache data: {str(e)}")

    def get_cached_data(self, symbol, start_date, end_date):
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT data FROM stock_cache 
                        WHERE symbol = %s 
                        AND start_date = %s 
                        AND end_date = %s
                    """, (symbol, start_date, end_date))
                    result = cur.fetchone()
                    if result:
                        logger.info(f"Retrieved cached data for {symbol}")
                        return json.loads(result[0])
        except Exception as e:
            logger.error(f"Failed to retrieve cached data: {str(e)}")
        return None