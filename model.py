"""
The patient data model for our testing and experiment.
"""
from datetime   import  date
from enum       import  Enum
from typing     import  List ,Optional

from pydantic   import  BaseModel ,PositiveInt

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

class HomeType(Enum):
    MAILING = "Mailing"
    BILLING = "Billing"

class Status(Enum):
    DEAD = "Dead"
    ALIVE = "Alive"

class PhoneType(Enum):
    HOME = "Home"
    CELL = "Cell"
    WORK = "Work"
        
class Address(BaseModel):
    id: PositiveInt
    zip: str
    number: str
    street: str
    city: str
    state: str
    country: str
    type: HomeType
    
class PhoneNumber(BaseModel):
    id: PositiveInt
    number: str
    type: PhoneType

class Contact(BaseModel):
    id: PositiveInt
    relationship: str
    name: str
    addresses: List[Address]
    phoneNumbers: List[PhoneNumber]

class Patient(BaseModel):
    id: PositiveInt
    status: Status
    name: str
    gender: Gender
    birthDay: date
    deceasedOn: Optional[date]
    maritalStatus: bool
    preferredLanguage: str
    activeFrom: date
    activeThru: Optional[date]
    contacts: List[Contact]
    addresses: List[Address]
    phoneNumbers: List[PhoneNumber]
