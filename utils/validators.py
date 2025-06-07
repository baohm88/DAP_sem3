
import re
from datetime import datetime, date

_email_re = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
_phone_re = re.compile(r"^\+?\d{7,15}$")

def validate_email(email: str) -> bool:
    return bool(_email_re.match(email))

def validate_phone(phone: str) -> bool:
    return bool(_phone_re.match(phone))

def future_date(input_str: str):
    try:
        dt = datetime.strptime(input_str, "%Y-%m-%d").date()
        return dt if dt >= date.today() else None
    except ValueError:
        return None
