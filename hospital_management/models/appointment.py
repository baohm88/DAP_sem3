"""Appointment table operations."""
from ..utils.validators import validate_required, validate_date, get_valid_input, validate_future_date
from .database import Database
from .patient import Patient
from .doctor import Doctor
from typing import Sequence, Any
from tabulate import tabulate
from mysql.connector import Error
from ..utils.enums import AppointmentStatus
from datetime import date

class Appointment:
    TABLE = "appointments"

    @staticmethod
    def create_table(db: Database) -> None:
        db.execute(f"""
        CREATE TABLE IF NOT EXISTS {Appointment.TABLE} (
            appointment_id   INT AUTO_INCREMENT PRIMARY KEY,
            patient_id       INT NOT NULL,
            doctor_id        INT,
            appointment_date DATE NOT NULL,
            reason           VARCHAR(255) NOT NULL,
            status           ENUM('Pending','Done','Cancelled') DEFAULT 'Pending',
            created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES {Patient.TABLE}(patient_id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES {Doctor.TABLE}(doctor_id) ON DELETE SET NULL,
            INDEX (appointment_date),
            INDEX (status)
        )""")

    @staticmethod
    def _print_records(title: str, records: Sequence[dict[str, Any]]) -> None:
        if not records:
            print(f"ℹ️ No {title.lower()} found")
            return
        
        print(f"\n📋 {title}")
        print(tabulate(records, headers="keys", tablefmt="pretty"))

    @staticmethod
    def add(db: Database) -> None:
        print("\n🔹 Schedule New Appointment")
        
        # Get available patients
        patients = db.execute(
            f"SELECT patient_id AS id, full_name AS name FROM {Patient.TABLE} ORDER BY full_name",
            fetch=True
        )
        Appointment._print_records("Available Patients", patients)
        if not patients:
            print("⚠️ No patients available - add patients first")
            return
        
        # Get available doctors
        doctors = db.execute(
            f"SELECT doctor_id AS id, full_name AS name, specialization FROM {Doctor.TABLE} ORDER BY full_name",
            fetch=True
        )
        Appointment._print_records("Available Doctors", doctors)
        if not doctors:
            print("⚠️ No doctors available - add doctors first")
            return

        # Get valid patient ID
        patient_id = get_valid_input(
            "\nEnter patient ID: ",
            lambda x: x.isdigit() and any(p['id'] == int(x) for p in patients),
            "Invalid patient ID"
        )

        # Get valid doctor ID
        doctor_id = get_valid_input(
            "Enter doctor ID : ",
            lambda x: x.isdigit() and any(d['id'] == int(x) for d in doctors),
            "Invalid doctor ID"
        )

        # Get appointment details
        appt_date = get_valid_input(
            "Appointment date (YYYY-MM-DD): ",
            lambda x: validate_date(x) and validate_future_date(x),
            "Invalid date (must be YYYY-MM-DD and not in the past)"
        )
        
        reason = get_valid_input(
            "Reason for appointment     : ",
            validate_required,
            "Reason cannot be empty"
        )
        
        status = get_valid_input(
            "Status [Pending/Done/Cancelled] (default: Pending): ",
            lambda x: not x or x.title() in [s.value for s in AppointmentStatus],
            "Invalid status",
            "Pending"
        ).title()

        try:
            db.begin_transaction()
            sql = f"""INSERT INTO {Appointment.TABLE}
                     (patient_id, doctor_id, appointment_date, reason, status)
                     VALUES (%s, %s, %s, %s, %s)"""
            db.execute(sql, (int(patient_id), int(doctor_id), appt_date, reason, status))
            db.commit()
            print("✅ Appointment scheduled successfully!\n")
        except Error:
            db.rollback()
            print("❌ Failed to schedule appointment\n")

    @staticmethod
    def get_report(db: Database) -> None:
        sql = f"""SELECT
            a.appointment_id AS id,
            p.full_name AS patient,
            DATE_FORMAT(p.date_of_birth, '%Y-%m-%d') AS dob,
            p.gender,
            p.address,
            d.full_name AS doctor,
            a.reason,
            DATE_FORMAT(a.appointment_date, '%Y-%m-%d') AS date,
            a.status
        FROM {Appointment.TABLE} a
        JOIN {Patient.TABLE} p ON a.patient_id = p.patient_id
        LEFT JOIN {Doctor.TABLE} d ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_date DESC"""
        
        appointments = db.execute(sql, fetch=True)
        Appointment._print_records("All Appointments", appointments)

    @staticmethod
    def get_todays(db: Database) -> None:
        today = date.today().strftime('%Y-%m-%d')
        sql = f"""SELECT
            a.appointment_id AS id,
            p.full_name AS patient,
            DATE_FORMAT(p.date_of_birth, '%Y-%m-%d') AS dob,
            p.gender,
            p.address,
            d.full_name AS doctor,
            a.status,
            a.reason AS notes
        FROM {Appointment.TABLE} a
        JOIN {Patient.TABLE} p ON a.patient_id = p.patient_id
        LEFT JOIN {Doctor.TABLE} d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_date = %s
        ORDER BY a.status"""
        
        appointments = db.execute(sql, (today,), fetch=True)
        if appointments:
            print(f"\n📅 Today's Appointments ({today})")
            print(tabulate(appointments, headers="keys", tablefmt="pretty"))
        else:
            print(f"ℹ️ No appointments scheduled for {today}")
