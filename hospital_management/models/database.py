"""Handles MySQL connection and queries with transaction support."""
import sys
import mysql.connector
from mysql.connector import Error
from typing import Optional, Sequence, Tuple, Any, Callable

class Database:
    """Enhanced database wrapper with transaction support and better error handling."""
    
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self._connect_and_prepare()

    def _connect_and_prepare(self) -> None:
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                autocommit=False
            )
            self._ensure_database()
            self.conn.database = self.database
        except Error as err:
            sys.exit(f"❌ Database connection failed: {err}")

    def _ensure_database(self) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                self.conn.commit()
        except Error as err:
            sys.exit(f"❌ Database creation failed: {err}")

    def execute(
        self,
        sql: str,
        params: Optional[Tuple | Sequence[Tuple]] = None,
        *,
        fetch: bool = False,
        many: bool = False
    ) -> Sequence[dict[str, Any]] | None:
        params = params or ()
        try:
            with self.conn.cursor(dictionary=True) as cur:
                if many:
                    cur.executemany(sql, params)
                else:
                    cur.execute(sql, params)
                return cur.fetchall() if fetch else None
        except Error as err:
            self.conn.rollback()
            print(f"⚠️ Database error: {err}")
            return None

    def begin_transaction(self) -> None:
        self.execute("START TRANSACTION")

    def commit(self) -> None:
        self.conn.commit()

    def rollback(self) -> None:
        self.conn.rollback()

    def close(self) -> None:
        if self.conn and self.conn.is_connected():
            self.conn.close()
