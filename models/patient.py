
"""
Patient CRUD operations
"""
from datetime import date
from typing import List, Dict, Any
from tabulate import tabulate
from .database import Database

TABLE = "patients"

def create_table(db: Database):
    db.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE}(
        patient_id      INT AUTO_INCREMENT PRIMARY KEY,
        full_name       VARCHAR(100) NOT NULL,
        date_of_birth   DATE NOT NULL,
        gender          ENUM('Male','Female','Other') NOT NULL,
        address         VARCHAR(255),
        phone_number    VARCHAR(20),
        email           VARCHAR(100)
    )
    """)

# ---------------------------------------------------------------------- #
def list_all(db: Database, order: str = 'ASC') -> List[Dict[str, Any]]:
    return db.execute(f"SELECT * FROM {TABLE} ORDER BY full_name {order}", fetch=True)

def search_by_id(db: Database, pid: int):
    return db.execute(f"SELECT * FROM {TABLE} WHERE patient_id=%s", (pid,), fetch=True)

def search_by_name(db: Database, name: str, order: str='ASC'):
    like = f"%{name}%"
    return db.execute(f"SELECT * FROM {TABLE} WHERE full_name LIKE %s ORDER BY full_name {order}", (like,), fetch=True)

def existing_names(db: Database):
    rows = db.execute(f"SELECT full_name FROM {TABLE}", fetch=True)
    return [r['full_name'] for r in rows]

def add_patient(db: Database, data: dict):
    sql = f"""INSERT INTO {TABLE}
            (full_name, date_of_birth, gender, address, phone_number, email)
            VALUES (%(full_name)s, %(date_of_birth)s, %(gender)s, %(address)s, %(phone_number)s, %(email)s)"""
    db.execute(sql, data)
