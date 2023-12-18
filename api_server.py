from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, PositiveInt
from starlette.middleware.gzip import GZipMiddleware


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class MaritalStatus(Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    UNKNOWN = "unknown"

class AddressUse(Enum):
    HOME = "home"
    WORK = "work"
    TEMP = "temp"
    BILL = "billing"
    OLD = "old"

class AddressType(Enum):
    POSTAL = "postal"
    PHYSICAL = "physical"
    BOTH = "both"

class StateAbbrevation(Enum):
    AL = "AL"   # Alabama
    AK = "AK"   # Alaska
    AZ = "AZ"   # Arizona
    AR = "AR"   # Arkansas
    CA = "CA"   # California
    CO = "CO"   # Colorado
    CT = "CT"   # Connecticut
    DE = "DE"   # Delaware
    FL = "FL"   # Florida
    GA = "GA"   # Georgia
    HI = "HI"   # Hawaii
    ID = "ID"   # Idaho
    IL = "IL"   # Illinois
    IN = "IN"   # Indiana
    IA = "IA"   # Iowa
    KS = "KS"   # Kansas
    KY = "KY"   # Kentucky
    LA = "LA"   # Louisiana
    ME = "ME"   # Maine
    MD = "MD"   # Maryland
    MA = "MA"   # Massachusetts
    MI = "MI"   # Michigan
    MN = "MN"   # Minnesota
    MS = "MS"   # Mississippi
    MO = "MO"   # Missouri
    MT = "MT"   # Montana
    NE = "NE"   # Nebraska
    NV = "NV"   # Nevada
    NH = "NH"   # New Hampshire
    NJ = "NJ"   # New Jersey
    NM = "NM"   # New Mexico
    NY = "NY"   # New York
    NC = "NC"   # North Carolina
    ND = "ND"   # North Dakota
    OH = "OH"   # Ohio
    OK = "OK"   # Oklahoma
    OR = "OR"   # Oregon
    PA = "PA"   # Pennsylvania
    RI = "RI"   # Rhode Island
    SC = "SC"   # South Carolina
    SD = "SD"   # South Dakota
    TN = "TN"   # Tennessee
    TX = "TX"   # Texas
    UT = "UT"   # Utah
    VT = "VT"   # Vermont
    VA = "VA"   # Virginia
    WA = "WA"   # Washington
    WV = "WV"   # West Virginia
    WI = "WI"   # Wisconsin
    WY = "WY"   # Wyoming

class ContactPointSystem(Enum):
    PHONE = "phone"
    FAX = "fax"
    EMAIL = "email"
    PAGER = "pager"
    URL = "url"
    SMS = "sms"
    OTHER = "other"

class ContactPointUse(Enum):
    HOME = "home"
    WORK = "work"
    TEMP = "temp"
    OLD = "old"
    MOBILE = "mobile"

class HumanNameUse(Enum):
    USUAL = "usual"
    OFFICIAL = "official"
    TEMP = "temp"
    NICKNAME = "nickname"
    ANONYMOUS = "anonymous"
    OLD = "old"
    MAIDEN = "maiden"

class PatientContactRelationship(Enum):
    EMERGENCY = "emergency"	    # Contact for use in case of emergency.
    FAMILY = "family"
    GUARDIAN = "guardian"
    FRIEND = "friend"
    PARTNER = "partner"
    WORK = "work"	            # Contact for matters related to the patients occupation/employment.
    CAREGIVER = "caregiver"     # (Non)professional caregiver
    AGENT = "agent"             # Contact that acts on behalf of the patient
    GUARANTOR = "guarantor"     # Contact for financial matters
#   OWNER = "owner of animal"   # For animals, the owner of the animal
    PARENT = "parent"           # Parent of the patient


class Address(BaseModel):
    ID : PositiveInt
    use : AddressUse        # purpose of this address
    type : AddressType
    text : str                          # Text representation of the address
    line : Optional[str]                # Street name, number, direction & P.O. Box etc.
    city : Optional[str]                # Name of city, town etc.
    district : Optional[str]            # District name (aka county)
    state : Optional[StateAbbrevation]  # Sub-unit of country (abbreviations ok)
    postal_code : Optional[str]         # Postal code for area
    country : Optional[str] = "US"      # Country (e.g. can be ISO 3166 2 or 3 letter code)
    # Time period when address was/is in use
    active_from : datetime  = datetime.utcnow()       # Starting time with inclusive boundary
    active_thru : Optional[datetime]                  # End time with inclusive boundary, if not ongoing

class ContactPoint(BaseModel):
    ID : PositiveInt
    system:  ContactPointSystem
    value: str              # The actual contact point details
    use: ContactPointUse    # purpose of this contact point
    rank: PositiveInt = 1   # Specify preferred order of use (1 = highest)
    # Time period when the contact point was/is in use
    active_from : datetime  = datetime.utcnow()     # Starting time with inclusive boundary
    active_thru : Optional[datetime]                # End time with inclusive boundary, if not ongoing

class HumanName(BaseModel):
    ID : PositiveInt
    use : HumanNameUse
    text : str              # Text representation of the full name
    family : str            # Family name (often called 'Surname')
    given : str             # Given names (not always 'first'). Includes middle names
    prefix : Optional[str]  # Parts that come before the name
    suffix : Optional[str]  # Parts that come after the name
    # Time period when name was/is in use
    active_from : datetime  = datetime.utcnow()     # Starting time with inclusive boundary
    active_thru : Optional[datetime]                # End time with inclusive boundary, if not ongoing

class ContactParty(BaseModel):
    ID : PositiveInt
    relationship : PatientContactRelationship       # The kind of relationship
    name : HumanName                                # A name associated with the contact person
    telecom : Optional[list[ContactPoint]]          # A contact detail for the person
    address : Optional[Address]                     # Address for the contact person
    gender : Optional[Gender]
#   organization : { Reference(Organization) }, // C? Organization that is associated with the contact
    # The period during which this contact person or organization is valid to be contacted relating to this patient
    active_from : datetime  = datetime.utcnow()     # Starting time with inclusive boundary
    active_thru : Optional[datetime]                # End time with inclusive boundary, if not ongoing

class Patient(BaseModel):
    ID : PositiveInt
    active : bool = True
    name : Optional[list[HumanName]] = None
    telecom : Optional[list[ContactPoint]] = None
    gender : Optional[Gender]
    birth_date: Optional[date]
    deceased_on: Optional[date]
    addresses: Optional[list[Address]] = None
    marital_status: Optional[MaritalStatus] = None  # Marital (civil) status of a patient
    contact: Optional[list[ContactParty]] = None    # A contact party (e.g. guardian, partner, friend) for the patient
    preferred_language: Optional[str]               # A language which may be used to communicate with the patient about his or her health.
    # Time period when the patient was/is in use
    active_from : datetime  = datetime.utcnow()     # Starting time with inclusive boundary
    active_thru : Optional[datetime]                # End time with inclusive boundary, if not ongoing


####

# The following serialize into 1254 bytes of json text send down to the browser.
# The raw data is about 380 bytes.
# Usually  the largers MTU is 1500 bytes.
addresses = {
    1: Address(ID=1, use=AddressUse.HOME, type=AddressType.PHYSICAL ,text="1 Main Street, Troy, MI 48084", line="1 Main Street", city="Troy1", state=StateAbbrevation.MI, postal_code="48084"),
    2: Address(ID=2, use=AddressUse.BILL, type=AddressType.POSTAL   ,text="2 Main Street, Troy, MI 48084", line="2 Main Street", city="Troy2", state=StateAbbrevation.MI, postal_code="48084"),
    3: Address(ID=3, use=AddressUse.TEMP, type=AddressType.BOTH     ,text="3 Main Street, Troy, MI 48084", line="3 Main Street", city="Troy3", state=StateAbbrevation.MI, postal_code="48084"),
    4: Address(ID=4, use=AddressUse.WORK, type=AddressType.PHYSICAL ,text="4 Main Street, Troy, MI 48084", line="4 Main Street", city="Troy4", state=StateAbbrevation.MI, postal_code="48084"),
    5: Address(ID=5, use=AddressUse.OLD , type=AddressType.POSTAL   ,text="5 Main Street, Troy, MI 48084", line="5 Main Street", city="Troy5", state=StateAbbrevation.MI, postal_code="48084"),
}


# TODO: Enable compression.
#       Externalize messages.
#       Enable HTTP/2 protocol.
#       Set the correct response HTTP code according to standard.

app = FastAPI()

# The following order is important for the server to pick which conpression algorithm.
# The following will pick Brotli first before gzip.
#
# Enable response compression using BrotliMiddleware
app.add_middleware( BrotliMiddleware )  # Content compressed down from 1254b to 263b 0.44ms!
# Enable response compression using GZipMiddleware
app.add_middleware( GZipMiddleware )  # Content compressed down from 1254b to 299b!



@app.get("/")
def address_list( response:Response ) -> dict[str ,dict[int ,Address]]:
    response.headers['Server'] = 'My Example Server'
    print(response.headers)
    return {"addresses" : addresses}

@app.get("/addresses/{id}")
def query_address_by_id(id:PositiveInt, response:Response ) -> Address:
    if id not in addresses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address {id} does NOT exist."
        )
    return addresses[id]

@app.get("/addresses/")
def query_address_by_params(
    use : AddressUse | None = None,
    type : AddressType | None = None,
    city : str | None = None,
    state : StateAbbrevation | None = None,
    postal_code : str | None = None,
    country : str | None = None,
) -> Address:
    def match_address(address: Address) -> bool:
        return all(
            use is None or type == address.use,
            type is None or type == address.type,
            city is None or city == address.city,
            state is None or state == address.state,
            postal_code is None or postal_code == address.postal_code,
            country is None or country == address.country,
        )

    return {
        "params" : {"use": use, "type": type, "city": city, "satte": state, "postal_code": postal_code, "country": country},
        "result" : [address for address in addresses.values()]
    }

def address_insert():
    pass

def address_update():
    pass

def address_delete(id:PositiveInt):
    if id not in addresses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address {id} does NOT exist."
        )
    addresses.pop(id)
