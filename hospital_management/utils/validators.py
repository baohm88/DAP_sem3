"""Reusable input validation functions."""
from datetime import datetime
from typing import Optional, Callable

def get_valid_input(
    prompt: str,
    validator: Callable[[str], bool],
    error_msg: str,
    default: Optional[str] = None
) -> str:
    """Get validated input with optional default value."""
    while True:
        value = input(prompt).strip()
        if not value and default is not None:
            return default
        if validator(value):
            return value
        print(error_msg)

def validate_date(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_future_date(date_str: str) -> bool:
    """Validate date is today or in the future."""
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return input_date >= date.today()
    except ValueError:
        return False

def validate_required(text: str) -> bool:
    """Validate input is not empty."""
    return bool(text.strip())

def validate_phone(phone: str) -> bool:
    """Basic phone number validation."""
    return phone.isdigit() and len(phone) >= 8

def validate_email(email: str) -> bool:
    """Basic email validation."""
    return "@" in email and "." in email.split("@")[-1]