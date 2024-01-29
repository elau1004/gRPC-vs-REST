import datetime
import protobuf_grpc_pb2 as pb2
import patient_dataclass as pd


def generate_name(n: pd.Name):
    name = pb2.Name()
    name.use = n.use
    name.text = n.text
    name.given = n.given
    name.family = n.family
    name.active = n.active.strftime('%m/%d/%Y')
    return name


def generate_telecom(t: pd.Telecom):
    contact_point = pb2.Telecom()
    contact_point.system = t.system
    contact_point.use = t.use
    contact_point.rank = t.rank
    contact_point.active = t.active.strftime('%m/%d/%Y')
    contact_point.value = t.value
    return contact_point


def generate_address(a: pd.Address):
    address = pb2.Address()
    address.use = a.use
    address.type = a.type
    address.line = a.line
    address.city = a.city
    address.state = a.state
    address.zipcode = a.zipcode
    address.country = a.country
    address.period_start = a.period_start.strftime('%m/%d/%Y')
    address.text = a.text
    address.period_end = a.period_end.strftime('%m/%d/%Y') if isinstance(a.period_end, datetime.date) else ''
    return address


def generate_contact(c: pd.Contact):
    contact = pb2.Contact()
    contact.relation = c.relation
    contact.name.CopyFrom(generate_name(c.name))
    contact.address.CopyFrom(generate_address(c.address))
    contact.telecom.CopyFrom(generate_telecom(c.telecom))
    return contact


def generate_patient(p: pd.Patient):
    patient = pb2.Patient()
    patient.id = p.id
    patient.active = p.active
    patient.gender = p.gender
    patient.birth_date = p.birth_date.strftime('%m/%d/%Y')
    patient.deceased_on = p.deceased_on
    patient.marital_status = p.marital_status

    # Generate repeated Name objects
    for n in p.names:
        patient.names.append(generate_name(n))
    # Generate repeated Telecom objects
    for t in p.telecoms:
        patient.telecoms.append(generate_telecom(t))
    # Generate repeated Address objects
    for a in p.addresses:
        patient.addresses.append(generate_address(a))
    # Generate repeated Contact objects
    for c in p.contacts:
        patient.contacts.append(generate_contact(c))

    return patient


def generate_patients(patient_list: list[pd.Patient]):
    patients = pb2.Patients()
    for p in patient_list:
        patients.all_patients.append(generate_patient(p))

    return patients
