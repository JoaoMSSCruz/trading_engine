class MarketDataRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def save_bar(self, symbol: str, timestamp, open_p, high, low, close, volume):
        query = """
            INSERT INTO market_bars (timestamp, symbol, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, timestamp) DO UPDATE
            SET open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume;
        """
        
        conn = self.db_manager.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (timestamp, symbol, open_p, high, low, close, volume))
            conn.commit()
        finally:
            # Liberta a ligação de volta para o pool
            self.db_manager.pool.putconn(conn)