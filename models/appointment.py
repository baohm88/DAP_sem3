
"""
Appointment CRUD operations
"""
from datetime import date
from typing import List, Dict, Any
from tabulate import tabulate
from .database import Database

TABLE = "appointments"
PATIENT_TABLE = "patients"
DOCTOR_TABLE = "doctors"

def create_table(db: Database):
    db.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE}(
        appointment_id   INT AUTO_INCREMENT PRIMARY KEY,
        patient_id       INT,
        doctor_id        INT,
        appointment_date DATE,
        reason           VARCHAR(255),
        status           ENUM('Pending','Done','Cancelled') DEFAULT 'Pending',
        FOREIGN KEY(patient_id) REFERENCES {PATIENT_TABLE}(patient_id) ON DELETE CASCADE,
        FOREIGN KEY(doctor_id)  REFERENCES {DOCTOR_TABLE}(doctor_id) ON DELETE SET NULL
    )
    """)

# ---------------------------------------------------------------------- #
def list_all(db: Database, order: str='ASC'):
    return db.execute(f"""SELECT a.*, p.full_name as patient_name, d.full_name as doctor_name
                        FROM {TABLE} a
                        JOIN {PATIENT_TABLE} p ON a.patient_id=p.patient_id
                        JOIN {DOCTOR_TABLE} d ON a.doctor_id=d.doctor_id
                        ORDER BY appointment_date {order}""", fetch=True)

def search_by_id(db: Database, aid: int):
    return db.execute(f"""SELECT a.*, p.full_name as patient_name, d.full_name as doctor_name
                        FROM {TABLE} a
                        JOIN {PATIENT_TABLE} p ON a.patient_id=p.patient_id
                        JOIN {DOCTOR_TABLE} d ON a.doctor_id=d.doctor_id
                        WHERE appointment_id=%s""", (aid,), fetch=True)

def search_by_patient(db: Database, pid: int):
    return db.execute(f"""SELECT a.*, p.full_name as patient_name, d.full_name as doctor_name
                        FROM {TABLE} a
                        JOIN {PATIENT_TABLE} p ON a.patient_id=p.patient_id
                        JOIN {DOCTOR_TABLE} d ON a.doctor_id=d.doctor_id
                        WHERE a.patient_id=%s
                        ORDER BY appointment_date""", (pid,), fetch=True)

def search_by_doctor(db: Database, did: int):
    return db.execute(f"""SELECT a.*, p.full_name as patient_name, d.full_name as doctor_name
                        FROM {TABLE} a
                        JOIN {PATIENT_TABLE} p ON a.patient_id=p.patient_id
                        JOIN {DOCTOR_TABLE} d ON a.doctor_id=d.doctor_id
                        WHERE a.doctor_id=%s
                        ORDER BY appointment_date""", (did,), fetch=True)

def list_today(db: Database):
    today = date.today()
    return db.execute(f"""SELECT a.*, p.full_name as patient_name, d.full_name as doctor_name
                        FROM {TABLE} a
                        JOIN {PATIENT_TABLE} p ON a.patient_id=p.patient_id
                        JOIN {DOCTOR_TABLE} d ON a.doctor_id=d.doctor_id
                        WHERE appointment_date=%s
                        ORDER BY appointment_date""", (today,), fetch=True)

def add_appointment(db: Database, data: dict):
    sql = f"""INSERT INTO {TABLE}
            (patient_id, doctor_id, appointment_date, reason, status)
            VALUES (%(patient_id)s, %(doctor_id)s, %(appointment_date)s, %(reason)s, %(status)s)"""
    db.execute(sql, data)

def update_appointment(db: Database, appointment_id: int, data: dict):
    sets = []
    params = []
    for field, value in data.items():
        sets.append(f"{field}=%s")
        params.append(value)
    params.append(appointment_id)
    sql = f"UPDATE {TABLE} SET {', '.join(sets)} WHERE appointment_id=%s"
    db.execute(sql, tuple(params))
