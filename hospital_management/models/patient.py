"""Patient table operations."""
from ..utils.validators import validate_required, validate_date, get_valid_input, validate_phone, validate_email
from ..utils.enums import Gender
from .database import Database
from mysql.connector import Error


class Patient:
    TABLE = "patients"

    @staticmethod
    def create_table(db: Database) -> None:
        db.execute(f"""
        CREATE TABLE IF NOT EXISTS {Patient.TABLE} (
            patient_id      INT AUTO_INCREMENT PRIMARY KEY,
            full_name       VARCHAR(100) NOT NULL,
            date_of_birth   DATE NOT NULL,
            gender          ENUM('Male','Female','Other') NOT NULL,
            address         VARCHAR(255),
            phone_number    VARCHAR(20),
            email           VARCHAR(100),
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )""")

    @staticmethod
    def add(db: Database) -> None:
        print("\n🔹 Add New Patient")
        
        full_name = get_valid_input(
            "Full name                 : ",
            validate_required,
            "Name cannot be empty"
        )
        
        dob = get_valid_input(
            "Date of birth (YYYY-MM-DD): ",
            validate_date,
            "Invalid date format (use YYYY-MM-DD)"
        )
        
        gender = get_valid_input(
            "Gender (Male/Female/Other): ",
            lambda g: g.title() in [e.value for e in Gender],
            "Invalid gender"
        ).title()
        
        address = get_valid_input(
            "Address                   : ",
            validate_required,
            "Address cannot be empty"
        )
        
        phone = get_valid_input(
            "Phone                     : ",
            validate_phone,
            "Invalid phone number (min 8 digits)"
        )
        
        email = get_valid_input(
            "Email                     : ",
            validate_email,
            "Invalid email format",
            ""
        )

        try:
            db.begin_transaction()
            sql = f"""INSERT INTO {Patient.TABLE}
                     (full_name, date_of_birth, gender, address, phone_number, email)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            db.execute(sql, (full_name, dob, gender, address, phone, email))
            db.commit()
            print("✅ Patient added successfully!\n")
        except Error:
            db.rollback()
            print("❌ Failed to add patient\n")
