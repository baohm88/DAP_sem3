
"""
Menu system – Home & submenus
"""
from tabulate import tabulate
from datetime import datetime
from typing import Any, Dict, List
from models import patient as pat, doctor as doc, appointment as app
from utils.enums import Gender, Status
from utils import validators as val
from models.database import Database

class Menu:
    def __init__(self, db: Database):
        self.db = db
        # make tables
        pat.create_table(db)
        doc.create_table(db)
        app.create_table(db)

    # ------------------------------ utils ----------------------------- #
    @staticmethod
    def _print(rows: List[Dict[str, Any]], title: str = ""):
        if rows:
            if title:
                print(f"\n{title}")
            print(tabulate(rows, headers="keys", tablefmt="pretty"))
        else:
            print("No data found.")

    # ------------------------------ flows ----------------------------- #
    def home(self):
        while True:
            print("""\n==================== Hospital Management System ====================
\t1. View Doctors
\t2. View Patients
\t3. View Appointments
\t4. Exit
====================================================================""")
            choice = input("Select » ").strip()
            match choice:
                case "1": self.doctors_menu()
                case "2": self.patients_menu()
                case "3": self.appointments_menu()
                case "4":
                    print("\n👋 Thank you for using the Hospital Management System!")
                    break
                case _: print("⚠️ Invalid choice. Please enter a number between 1-8.")
            
    # ------------------- Doctors ------------------------------------- #
    def doctors_menu(self):
        while True:
            print("""\n==================== Doctors Menu ====================
\t1. Add new doctor
\t2. Search doctor by Id
\t3. Search doctor by name
\t4. Sort doctors by name (ASC)
\t5. Sort doctors by name (DESC)
\t6. Sort doctors by experience (ASC)
\t7. Sort doctors by experience (DESC)
\t8. Back to Home
======================================================""")
            ch = input("Select » ").strip()
            if ch == "1":
                self._add_doctor()
            elif ch == "2":
                did = int(input("Doctor ID: "))
                print(f'\n👩‍⚕️ Doctors with id of \"{did}\"')
                self._print(doc.search_by_id(self.db, did))
            elif ch == "3":
                name = input("Name contains: ")
                print(f'\n👩‍⚕️ Doctors with name of \"{name}\"')
                self._print(doc.search_by_name(self.db, name))
            elif ch == "4":
                print(f'\n👩‍⚕️ Doctors (names sorted ASC)')
                self._print(doc.list_all(self.db, 'ASC'))
            elif ch == "5":
                print(f'\n👩‍⚕️ Doctors (names sorted DESC)')
                self._print(doc.list_all(self.db, 'DESC'))
            elif ch == "6":
                print(f'\n👩‍⚕️ Doctors (experience sorted ASC)')
                self._print(doc.sort_by_experience(self.db, 'ASC'))
            elif ch == "7":
                print(f'\n👩‍⚕️ Doctors (experience sorted DESC)')
                self._print(doc.sort_by_experience(self.db, 'DESC'))
            elif ch == "8":
                break
            else:
                print("Invalid choice")

    # ------------------- Patients ------------------------------------ #
    def patients_menu(self):
        while True:
            print("""\n==================== Patients Menu ====================
\t1. Add new patient
\t2. Search patient by Id
\t3. Search patient by name
\t4. Sort patients by name (ASC)
\t5. Sort patients by name (DESC)
\t6. Sort patients by DOB (ASC)
\t7. Sort patients by DOB (DESC)
\t8. Back to Home
======================================================""")
            
            ch = input("Select » ").strip()
            if ch == "1": self._add_patient()
            elif ch == "2":
                pid = int(input("Patient ID: "))
                print(f'\n👳‍♂️ Patient with id of \"{pid}\"')
                self._print(pat.search_by_id(self.db, pid))
            elif ch == "3":
                name = input("Name contains: ")
                print(f'\n👳‍♂️ Patients with name of \"{name}\"')
                self._print(pat.search_by_name(self.db, name))
            elif ch == "4":
                print(f'\n👳‍♂️ Patients (names sorted ASC)')
                self._print(pat.list_all(self.db, 'ASC'))
            elif ch == "5":
                print(f'\n👳‍♂️ Patients (names sorted DESC)')
                self._print(pat.list_all(self.db, 'DESC'))
            elif ch == "6":
                rows = self.db.execute(f"SELECT * FROM {pat.TABLE} ORDER BY date_of_birth ASC", fetch=True)
                print(f'\n👳‍♂️ Patients (DOB sorted ASC)')
                self._print(rows)
            elif ch == "7":
                rows = self.db.execute(f"SELECT * FROM {pat.TABLE} ORDER BY date_of_birth DESC", fetch=True)
                print(f'\n👳‍♂️ Patients (DOB sorted DESC)')
                self._print(rows)
            elif ch == "8": break
            else: print("Invalid choice")

    # ------------------- Appointments -------------------------------- #
    def appointments_menu(self):
        while True:
            print("""\n==================== Appointments Menu ====================
\t1 Add new appointment
\t2 Search appointment by ID
\t3 Search appointments by Patient ID
\t4 Search appointments by Doctor ID
\t5 View Today's appointments
\t6 Sort appointments by date (ASC)
\t7 Sort appointments by date (DESC)
\t8 Update appointment
\t9 Back to Home
======================================================""")
            
            ch = input("Select » ").strip()
            if ch == "1": self._add_appointment()
            elif ch == "2":
                aid = int(input("Appointment ID: "))
                print(f'\n📅 Appointment with id of \"{aid}\"')
                self._print(app.search_by_id(self.db, aid))
            elif ch == "3":
                pid = int(input("Patient ID: "))
                print(f'\n📅 Appointment with Patient ID of \"{pid}\"')
                self._print(app.search_by_patient(self.db, pid))
            elif ch == "4":
                did = int(input("Doctor ID: "))
                print(f'\n📅 Appointment with Doctor ID of \"{did}\"')
                self._print(app.search_by_doctor(self.db, did))
            elif ch == "5":
                print(f'\n📅 Appointment for Today')
                self._print(app.list_today(self.db))
            elif ch == "6":
                print(f'\n📅 Appointments (date sorted ASC)')
                self._print(app.list_all(self.db, 'ASC'))
            elif ch == "7":
                print(f'\n📅 Appointments (date sorted DESC)')
                self._print(app.list_all(self.db, 'DESC'))
            elif ch == "8":
                self._update_appointment()
            elif ch == "9": break
            else: print("Invalid choice")

    # ===================== helpers to add ============================ #
    def _add_doctor(self):
        existing = doc.existing_names(self.db)
        if existing:
            print("Existing doctors:", ', '.join(existing))
        data = {
            'full_name': input("Full name: ").strip(),
            'specialization': input("Specialization: ").strip(),
            'phone_number': input("Phone: ").strip(),
            'email': input("Email: ").strip(),
            'year_of_experience': int(input("Years of experience: ") or 0)
        }
        if data['full_name'] in existing:
            print("Doctor already exists!")
            return
        doc.add_doctor(self.db, data)
        print("✅ Doctor added successfully!\n")

    def _add_patient(self):
        existing = pat.existing_names(self.db)
        if existing:
            print("Existing patients:", ', '.join(existing))
        data = {
            'full_name': input("Full name: ").strip(),
            'date_of_birth': input("DOB (YYYY-MM-DD): ").strip(),
            'gender': input("Gender (Male/Female/Other): ").strip().title(),
            'address': input("Address: ").strip(),
            'phone_number': input("Phone: ").strip(),
            'email': input("Email: ").strip(),
        }
        if data['full_name'] in existing:
            print("Patient already exists!")
            return
        pat.add_patient(self.db, data)
        print("✅ Patient added successfully!\n.")

    def _add_appointment(self):
        print(f'\n👳‍♂️ Patients (names sorted ASC)')
        self._print(pat.list_all(self.db, 'ASC'))
        patient_id = int(input("Enter Patient ID from the list above: "))

        print(f'\n👩‍⚕️ Doctors (names sorted ASC)')
        self._print(doc.list_all(self.db, 'ASC'))
        doctor_id = int(input("Enter Doctor ID from the list above: "))
        app_date = input("Appointment Date (YYYY-MM-DD): ")
        reason = input("Reason: ")
        status = input("Status (Pending/Done/Cancelled): ").strip().title() or 'Pending'
        app.add_appointment(self.db, {
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'appointment_date': app_date,
            'reason': reason,
            'status': status
        })
        print("✅ Appointment added successfully!")

    def _update_appointment(self):
        print(f'\n📅 Appointments (date sorted ASC)')
        self._print(app.list_all(self.db, 'ASC'))
        aid = int(input("Enter Appointment ID from the above list to update: "))
        record = app.search_by_id(self.db, aid)
        if not record:
            print("❌ Appointment not found")
            return
        record = record[0]
        print("Leave blank to keep current value")
        data = {}
        for field in ['patient_id','doctor_id','appointment_date','reason','status']:
            new_val = input(f"{field} [{record[field]}]: ")
            if new_val:
                data[field] = new_val if field != 'patient_id' and field != 'doctor_id' else int(new_val)
        if data:
            app.update_appointment(self.db, aid, data)
            print("✅ Appointment updated successfully!")
        else:
            print("Nothing changed.")
