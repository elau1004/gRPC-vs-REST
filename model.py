"""
The patient data model for our testing and experiment.
"""
import  random

from    datetime   import  date
from    enum       import  Enum
from    typing     import  List ,Optional

from    faker              import  Faker
from    faker.providers    import  address ,date_time ,phone_number
from    pydantic           import  BaseModel ,PositiveInt

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

# NOTE: DONT change the seed.
random.seed( 101 )
Faker.seed(  101 )
fake = Faker()
fake.add_provider( date_time )
fake.add_provider( phone_number )
fake.add_provider( address )

patient_id = 0
address_id = 0
contact_id = 0
phone_id   = 0

def random_addresses() -> List[Address]:
    global address_id
    addresses: List[Address] = list()

    address_id += 1
    address = Address(
        id      =  address_id,
        type    =  HomeType.MAILING,
        number  =  fake.building_number(),
        street  =  fake.street_name(),
        city    =  fake.city(),
        state   =  fake.state(),
        zip     =  fake.zipcode(),
        country = "USA",
    )
    addresses.append( address )

    if  fake.boolean:
        address_id += 1
        address = Address(
            id      =  address_id,
            type    =  HomeType.BILLING,
            number  =  fake.building_number(),
            street  =  fake.street_name(),
            city    =  fake.city(),
            state   =  fake.state(),
            zip     =  fake.zipcode(),
            country = "USA",
        )
        addresses.append( address )

    return addresses

def random_phones() -> List[PhoneNumber]:
    global phone_id
    phones: List[PhoneNumber] = list()

    phone_id += 1
    phone = PhoneNumber(
        id      = phone_id,
        number  = fake.phone_number(),
        type    = PhoneType.CELL
    )
    phones.append( phone )

    if  fake.boolean:
        phone_id += 1
        phone = PhoneNumber(
            id      = phone_id,
            number  = fake.phone_number(),
            type    = PhoneType.HOME
        )
        phones.append( phone )

    if  fake.boolean():
        phone_id += 1
        phone = PhoneNumber(
            id      = phone_id,
            number  = fake.phone_number(),
            type    = PhoneType.WORK
        )
        phones.append( phone )

    return phones

def random_contacts() -> List[Contact]:
    global contact_id
    contacts: List[Contact] = list()

    if  fake.boolean:
        contact_id += 1
        contact = Contact(
            id          = contact_id,
            relationship= "Mother",
            name        = fake.name(),
            addresses   = random_addresses(),
            phoneNumbers= random_phones()
        )
        contacts.append( contact )

    if  fake.boolean:
        contact_id += 1
        contact = Contact(
            id          = contact_id,
            relationship= "Father",
            name        = fake.name(),
            addresses   = random_addresses(),
            phoneNumbers= random_phones()
        )
        contacts.append( contact )

    if  fake.boolean:
        contact_id += 1
        contact = Contact(
            id          = contact_id,
            relationship= "Social", # Social worker
            name        = fake.name(),
            addresses   = random_addresses(),
            phoneNumbers= random_phones()
        )
        contacts.append( contact )

    return contacts


def random_patients() -> List[Patient]:
    global patient_id
    patients: List[Patient] = list()

    for i in range( 5000 ):
        patient_id = i+1
        patient = Patient(
            id              =  patient_id,
            status          =  Status.ALIVE,
            name            =  "",
            gender          =  Gender.MALE if fake.boolean() else Gender.FEMALE,
            birthDay        =  fake.date_of_birth(),
            deceasedOn      =  None,
            maritalStatus   =  True if fake.boolean() else False,
            preferredLanguage= fake.language_name(),
            activeFrom      =  fake.date(),
            activeThru      =  None,
            addresses       =  random_addresses(),
            phoneNumbers    =  random_phones(),
            contacts        =  random_contacts()
        )
        if  patient.gender  == Gender.MALE:
            patient.name    =  fake.name_male()
        else:
            patient.name    =  fake.name_female()

        if  random.randint(0 ,9)== 0: # 10% are inactive.
            temp_date       =  fake.date_between( patient.activeFrom )
            if  isinstance( temp_date ,date):
                patient.activeThru  =  temp_date
            elif isinstance(temp_date ,list):
                patient.activeThru  =  temp_date[0]

        if  random.randint(0 ,9)== 4: # 10% are deceased.
            patient.status      =  Status.DEAD
            patient.deceasedOn  =  fake.date_between( patient.birthDay )
            patient.activeThru  =  patient.deceasedOn

        patients.append( patient )
    return  patients

# Pre-generate a list 5000 fake patients.
# To be reuse between RESTful and gRPC.
patients: List[Patient] = random_patients()

# Set the first patient to be small in size.
patients[0].addresses = patients[0].addresses[0:1]
patients[0].contacts  = patients[0].contacts[0:1]
patients[0].phoneNumbers = patients[0].phoneNumbers[0:1]
