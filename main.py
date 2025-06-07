
from getpass import getpass
from models.database import Database
from cli.menu import Menu
from mysql.connector import Error
import sys

def prompt_creds():
    host = input("Host [localhost]: ").strip() or "localhost"
    user = input("User [root]: ").strip() or "root"
    pwd  = getpass("Password: ") or "Bao@1234"
    db   = input("Database [hospital_db]: ").strip() or "hospital_db"
    return host, user, pwd, db

def main():
    print("\n🏥 Hospital Management System Setup")
    print("Configure your database connection (press Enter for defaults)\n")

    creds = prompt_creds()
    db = Database(*creds)
    try:
        Menu(db).home()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Error as e:
        print(f"❌ Failed to initialize database: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
