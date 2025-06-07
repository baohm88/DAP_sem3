
"""
Database connection handler (MySQL)
"""
from typing import Sequence, Tuple, Any, Optional
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self._connect()

    # ------------------------------------------------------------------ #
    def _connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.conn.autocommit = False
            self._ensure_db()
            self.conn.database = self.database
        except Error as err:
            raise SystemExit(f"DB connection failed: {err}")

    def _ensure_db(self):
        with self.conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.conn.commit()

    # ------------------------------------------------------------------ #
    def execute(self, sql: str, params: Optional[Tuple | Sequence[Tuple]] = None,
                *, fetch: bool=False, many: bool=False):
        params = params or ()
        with self.conn.cursor(dictionary=True) as cur:
            if many:
                cur.executemany(sql, params)  # type: ignore
            else:
                cur.execute(sql, params)  # type: ignore
            rows = cur.fetchall() if fetch else None
        self.conn.commit()
        return rows or []

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
