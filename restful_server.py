"""
The RESTful server to serve out our test patient data.
"""

import random

from datetime   import  date
from enum       import  Enum
from typing     import  List

from faker              import Faker
from faker.providers    import address ,date_time ,phone_number 
from fastapi            import FastAPI, HTTPException
from fastapi.responses  import RedirectResponse

import model    # Our test patient data model.


# Pre-generate a list 1000 fake patients.
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

def random_addresses() -> List[model.Address]:
    global address_id
    addresses: List[model.Address] = list()

    address_id += 1
    address = model.Address(
        id      =  address_id,
        type    =  model.HomeType.MAILING,
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
        address = model.Address(
            id      =  address_id,
            type    =  model.HomeType.BILLING,
            number  =  fake.building_number(),
            street  =  fake.street_name(),
            city    =  fake.city(),
            state   =  fake.state(),
            zip     =  fake.zipcode(),
            country = "USA",
        )
        addresses.append( address )

    return addresses

def random_phones() -> List[model.PhoneNumber]:
    global phone_id
    phones: List[model.PhoneNumber] = list()

    phone_id += 1
    phone = model.PhoneNumber(
        id      = phone_id,
        number  = fake.phone_number(),
        type    = model.PhoneType.CELL
    )
    phones.append( phone )

    if  fake.boolean:
        phone_id += 1
        phone = model.PhoneNumber(
            id      = phone_id,
            number  = fake.phone_number(),
            type    = model.PhoneType.HOME
        )
        phones.append( phone )

    if  fake.boolean():
        phone_id += 1
        phone = model.PhoneNumber(
            id      = phone_id,
            number  = fake.phone_number(),
            type    = model.PhoneType.WORK
        )
        phones.append( phone )

    return phones

def random_contacts() -> List[model.Contact]:
    global contact_id
    contacts: List[model.Contact] = list()

    if  fake.boolean:
        contact_id += 1
        contact = model.Contact(
            id          = contact_id,
            relationship= "Mother",
            name        = fake.name(),
            addresses   = random_addresses(),
            phoneNumbers= random_phones()
        )
        contacts.append( contact )

    if  fake.boolean:
        contact_id += 1
        contact = model.Contact(
            id          = contact_id,
            relationship= "Father",
            name        = fake.name(),
            addresses   = random_addresses(),
            phoneNumbers= random_phones()
        )
        contacts.append( contact )

    if  fake.boolean:
        contact_id += 1
        contact = model.Contact(
            id          = contact_id,
            relationship= "Social", # Social worker
            name        = fake.name(),
            addresses   = random_addresses(),
            phoneNumbers= random_phones()
        )
        contacts.append( contact )
    
    return contacts


def random_patients() -> List[model.Patient]:
    global patient_id
    patients: List[model.Patient] = list()

    for i in range( 5000 ):
        patient_id = i+1
        patient = model.Patient(
            id              =  patient_id,
            status          =  model.Status.ALIVE,
            name            =  "",
            gender          =  model.Gender.MALE if fake.boolean() else model.Gender.FEMALE,
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
        if  patient.gender  == model.Gender.MALE:
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
            patient.status      =  model.Status.DEAD
            patient.deceasedOn  =  fake.date_between( patient.birthDay )
            patient.activeThru  =  patient.deceasedOn

        patients.append( patient )
    return  patients

patients: List[model.Patient] = random_patients()

# Set the first 2 patient to be small in size.
patients[0].addresses = patients[0].addresses[0:1]
patients[0].contacts  = patients[0].contacts[0:1]
patients[0].phoneNumbers = patients[0].phoneNumbers[0:1]

# Initialized the API server.
class Prot(Enum):
    HTTP1   = 'http1'
    HTTP2   = 'http2'

class Compression(Enum):
    NONE    = 'none'
    BROTLI  = 'brotli'
    DEFLATE = 'deflate'
    GZIP    = "gzip"
    ZSTD    = 'zstd'

class Size(Enum):
    FULL    = 'full'   # Full packet
    SMALL   = 'small'
    MEDIUM  = 'medium'
    LARGE   = 'large'
    HUGE    = 'huge'

app = FastAPI()

@app.get("/")
def index() -> str:
    return 'Hello.  Server is running.  Parameters are: protocol: [http1 ,http2] ,compression: [brotli ,gzip ,deflate ,zstd] ,datasize: [full ,small ,medium ,large ,huge]'

@app.get("/patient/")
def get_patients( runtoken: str = None ,compression: str = None ,datasize: str = None ) -> List[model.Patient]:
    end: int = 1
    match datasize: # The following sizes are obtained from inspecting the traffic in the browser.
        case Size.FULL.value:   end = 1     # 1.1 kb
        case Size.SMALL.value:  end = 5     # 9.9 kb
        case Size.MEDIUM.value: end = 50    # 107 kb
        case Size.LARGE.value:  end = 500   # 1.1 mb
        case Size.HUGE.value:   end = 5000  # 11  mb
        case _: end = 1

    return  patients[0 : end]

@app.get("/patient/{patient_id}")
def get_patient( patient_id: int ) -> model.Patient:
    try:
        patient = patients[ patient_id ]
    except Exception as ex:
        # SEE:  https://www.websitepulse.com/kb/4xx_http_status_codes
        raise HTTPException(status_code=400, detail=f"patient with ID={patient_id=} doesn't exist.")
    return  patient
