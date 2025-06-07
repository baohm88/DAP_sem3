"""Handles the CLI menu flow."""
from hospital_management.models.database import Database
from hospital_management.models.patient import Patient
from hospital_management.models.doctor import Doctor
from hospital_management.models.appointment import Appointment
from tabulate import tabulate

class HospitalCLI:
    def __init__(self, db: Database):
        self.db = db

    def _display_menu(self) -> None:
        """Show the main menu"""
        print("""
==================== Hospital Management System ====================
1. Add Patient             5. View Today's Appointments
2. Add Doctor              6. View Doctors
3. Schedule Appointment    7. View Patients
4. View All Appointments   8. Exit
====================================================================
""")

    def run(self) -> None:
        """Main application loop"""
        while True:
            self._display_menu()
            choice = input("Select an option (1-8): ").strip()
            
            try:
                match choice:
                    case "1":
                        Patient.add(self.db)
                    case "2":
                        Doctor.add(self.db)
                    case "3":
                        Appointment.add(self.db)
                    case "4":
                        Appointment.get_report(self.db)
                    case "5":
                        Appointment.get_todays(self.db)
                    case "6":
                        self._show_doctors()
                    case "7":
                        self._show_patients()
                    case "8":
                        print("\n👋 Thank you for using the Hospital Management System!")
                        break
                    case _:
                        print("⚠️ Invalid choice. Please enter a number between 1-8.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
            except Exception as e:
                print(f"❌ An error occurred: {e}")

    def _show_doctors(self) -> None:
        """Display all doctors"""
        doctors = self.db.execute(
            f"""SELECT 
                doctor_id AS id,
                full_name AS name,
                specialization,
                year_of_experience AS experience,
                phone_number AS phone,
                email
            FROM {Doctor.TABLE}
            ORDER BY full_name""",
            fetch=True
        )
        if doctors:
            print("\n👨‍⚕️ Doctors List")
            print(tabulate(doctors, headers="keys", tablefmt="pretty"))
        else:
            print("ℹ️ No doctors found in the system")

    def _show_patients(self) -> None:
        """Display all patients"""
        patients = self.db.execute(
            f"""SELECT 
                patient_id AS id,
                full_name AS name,
                DATE_FORMAT(date_of_birth, '%Y-%m-%d') AS dob,
                gender,
                address,
                phone_number AS phone,
                email
            FROM {Patient.TABLE}
            ORDER BY full_name""",
            fetch=True
        )
        if patients:
            print("\n🏥 Patients List")
            print(tabulate(patients, headers="keys", tablefmt="pretty"))
        else:
            print("ℹ️ No patients found in the system")

