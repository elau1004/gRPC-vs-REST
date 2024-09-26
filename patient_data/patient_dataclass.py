from dataclasses import dataclass, field
from datetime import date


@dataclass
class Name:
    use: str
    text: str
    given: str
    family: str
    active: date


@dataclass
class Telecom:
    system: str
    use: str
    rank: int
    active: date
    value: str = field(default='')


@dataclass
class Address:
    use: str
    type: str
    line: str
    city: str
    state: str
    zipcode: str
    country: str
    period_start: date
    text: str = field(default='')
    period_end: date = field(default=None)


@dataclass
class Contact:
    relation: str
    name: Name
    address: Address
    telecom: Telecom = field(default=Telecom)


@dataclass
class Patient:
    id: int
    active: bool
    gender: str
    birth_date: date
    marital_status: str
    deceased_on: str = field(default='')
    names: list[Name] = field(default_factory=list)
    telecoms: list[Telecom] = field(default_factory=list)
    addresses: list[Address] = field(default_factory=list)
    contacts: list[Contact] = field(default_factory=list)
