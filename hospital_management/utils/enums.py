"""Type-safe enumerations."""
from enum import Enum

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class AppointmentStatus(Enum):
    PENDING = "Pending"
    DONE = "Done"
    CANCELLED = "Cancelled"