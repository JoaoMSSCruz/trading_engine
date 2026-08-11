import psycopg2
from psycopg2 import pool
from .schemas import CREATE_BARS_TABLE

class DatabaseManager:
    def __init__(self, db_url: str, min_conn: int = 1, max_conn: int = 10):
        self.db_url = db_url
        self.min_conn = min_conn
        self.max_conn = max_conn
        self.pool = None

    def connect(self):
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            self.min_conn, 
            self.max_conn, 
            dsn=self.db_url
        )
        self._init_db()
        return self.pool

    def _init_db(self):
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(CREATE_BARS_TABLE)
            conn.commit()
        finally:
            self.pool.putconn(conn) 

    def disconnect(self):
        if self.pool:
            self.pool.closeall()