"""Doctor table operations."""
from ..utils.validators import validate_required, get_valid_input, validate_phone, validate_email
from .database import Database


class Doctor:
    TABLE = "doctors"

    @staticmethod
    def create_table(db: Database) -> None:
        db.execute(f"""
        CREATE TABLE IF NOT EXISTS {Doctor.TABLE} (
            doctor_id          INT AUTO_INCREMENT PRIMARY KEY,
            full_name          VARCHAR(100) NOT NULL,
            specialization     VARCHAR(100),
            phone_number       VARCHAR(20),
            email              VARCHAR(100),
            year_of_experience INT,
            created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )""")

    @staticmethod
    def add(db: Database) -> None:
        print("\n🔹 Add New Doctor")
        
        full_name = get_valid_input(
            "Full name           : ",
            validate_required,
            "Name cannot be empty"
        )
        
        specialization = get_valid_input(
            "Specialization      : ",
            validate_required,
            "Specialization cannot be empty"
        )
        
        phone = get_valid_input(
            "Phone number        : ",
            validate_phone,
            "Invalid phone number (min 8 digits)"
        )
        
        email = get_valid_input(
            "Email               : ",
            validate_email,
            "Invalid email format",
            ""
        )
        
        years = get_valid_input(
            "Years of experience : ",
            lambda x: x.isdigit(),
            "Years must be a number"
        )

        try:
            db.begin_transaction()
            sql = f"""INSERT INTO {Doctor.TABLE}
                     (full_name, specialization, phone_number, email, year_of_experience)
                     VALUES (%s, %s, %s, %s, %s)"""
            db.execute(sql, (full_name, specialization, phone, email, int(years)))
            db.commit()
            print("✅ Doctor added successfully!\n")
        except Error:
            db.rollback()
            print("❌ Failed to add doctor\n")
