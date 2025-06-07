
"""
Doctor CRUD operations
"""
from typing import List, Dict, Any
from tabulate import tabulate
from .database import Database

TABLE = "doctors"

def create_table(db: Database):
    db.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE}(
        doctor_id          INT AUTO_INCREMENT PRIMARY KEY,
        full_name          VARCHAR(100) NOT NULL,
        specialization     VARCHAR(100),
        phone_number       VARCHAR(20),
        email              VARCHAR(100),
        year_of_experience INT
    )
    """)

# ---------------------------------------------------------------------- #
def list_all(db: Database, order: str='ASC') -> List[Dict[str, Any]]:
    return db.execute(f"SELECT * FROM {TABLE} ORDER BY full_name {order}", fetch=True)

def search_by_id(db: Database, did: int):
    return db.execute(f"SELECT * FROM {TABLE} WHERE doctor_id=%s", (did,), fetch=True)

def search_by_name(db: Database, name: str, order: str='ASC'):
    like = f"%{name}%"
    return db.execute(f"SELECT * FROM {TABLE} WHERE full_name LIKE %s ORDER BY full_name {order}", (like,), fetch=True)

def sort_by_experience(db: Database, order: str='ASC'):
    return db.execute(f"SELECT * FROM {TABLE} ORDER BY year_of_experience {order}", fetch=True)

def existing_names(db: Database):
    rows = db.execute(f"SELECT full_name FROM {TABLE}", fetch=True)
    return [r['full_name'] for r in rows]

def add_doctor(db: Database, data: dict):
    sql = f"""INSERT INTO {TABLE}
            (full_name, specialization, phone_number, email, year_of_experience)
            VALUES (%(full_name)s, %(specialization)s, %(phone_number)s, %(email)s, %(year_of_experience)s)"""
    db.execute(sql, data)
