"""Entry point for the application."""
import sys
from getpass import getpass
from hospital_management.models.database import Database
from hospital_management.cli.menu import HospitalCLI
from mysql.connector import Error

def main():
    print("\n🏥 Hospital Management System Setup")
    print("Configure your database connection (press Enter for defaults)\n")
    
    host = input("MySQL Host [localhost]: ").strip() or "localhost"
    user = input("MySQL User [root]: ").strip() or "root"
    password = getpass("MySQL Password: ")
    db_name = input("Database Name [hospital_db]: ").strip() or "hospital_db"

    try:

        db = Database(host, user, password, db_name)
        cli = HospitalCLI(db)
        cli.run()
    except Error as e:
        print(f"❌ Failed to initialize database: {e}")
        sys.exit(1)
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()