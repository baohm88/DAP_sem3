# 🏥 Hospital Management System

A lightweight **Python + MySQL** CLI application for managing patients, doctors, and their appointments. Ideal for coursework, demos, or small clinics that need a simple terminal‑based workflow.

> **Tech stack**
>
> * Python 3.9 +(tested on 3.12)
> * MySQL 8 (or compatible MariaDB)
> * `mysql‑connector‑python` – database driver
> * `tabulate` – pretty tabular output in the console

---

## 📁 Project Structure

```
hospital_management/
├── models/                   # Database models & data access
│   ├── database.py           # MySQL connection handler
│   ├── patient.py            # Patient operations (CRUD)
│   ├── doctor.py             # Doctor operations (CRUD)
│   └── appointment.py        # Appointment operations (CRUD + reporting)
│
├── cli/                      # Command‑line interface helpers
│   └── menu.py               # Main menu & routing
│
├── utils/                    # General‑purpose helpers
│   ├── validators.py         # Input validation (email, phone, dates)
│   └── enums.py              # Enumerations (Gender, Status)
│
├── main.py                   # Application entry‑point
└── README.md                 # This file
```

*(If you cloned the one‑file demo you will only see **`hospital_management_system.py`** – the logic is the same, just not split into packages.)*

---

## 🚀 Features

### 1. Patient Management

* **Add** new patients with full name, birthday, gender, address, phone, email
* **List** existing patients in a neatly formatted table

### 2. Doctor Management

* **Add** doctors with name, specialization, years of experience, phone, email
* **List** registered doctors

### 3. Appointment Scheduling

* **Book** appointments linking a patient ↔ doctor on a specific date
* **Status tracking**: `Pending`, `Done`, or `Cancelled`
* Built‑in reports:

  * **All appointments** (template‑styled)
  * **Today’s appointments** (grouped by address, matches assignment spec)

### 4. Data Validation & Safety

* Enumerated gender / status fields to avoid typos
* Email & phone format checking via `utils.validators`
* Prevent appointments in the past (future‑date enforcement)
* Live **ID look‑ups** so users choose valid `patient_id` & `doctor_id`
* All SQL calls use **parameterised queries** to thwart SQL injection

---

## 🛠  Quick Start

### 1  Install Dependencies (inside a venv)

```bash
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python tabulate
```

### 2  Create the MySQL Database

```sql
CREATE DATABASE hospital_db;
```

*(You can name it differently – you’ll point the app at it in step 3.)*

### 3  Run the Application

```bash
python main.py   # or python hospital_management_system.py
```

When prompted, enter your MySQL credentials. Press **Enter** to accept the defaults:

```
Host [localhost]:
User [root]:
Password: ******
Database [hospital_db]:
```

### 4  Navigate the Menu

```
==================== Hospital Management System ====================
1. Add Patient             5. View Today’s Appointments
2. Add Doctor              6. View Doctors
3. Schedule Appointment    7. View Patients
4. View All Appointments   8. Exit
====================================================================
```

Enter the corresponding **number** and follow the prompts. Tables are rendered with borders via **tabulate** for clarity.

---

## ✏️  Configuration Tips

* **Change defaults** – Edit constants at the top of `models/database.py` (or the prompt function in the monolithic script).
* **Seed data** – You can import CSVs or run SQL inserts; foreign‑key constraints are enabled.
* **Docker‑ise** – Wrap MySQL + the Python app in a `docker‑compose.yml` (optional, not included here).

---

## 📜 License

MIT License – do whatever you’d like, but please retain attribution.

---

## 🤝 Contributing

Pull requests are welcome! Open an issue first to discuss major changes.

Happy coding ‑ and stay healthy! :)
