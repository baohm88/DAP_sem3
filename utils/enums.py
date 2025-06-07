
from enum import Enum

class Gender(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class Status(str, Enum):
    Pending = "Pending"
    Done = "Done"
    Cancelled = "Cancelled"
