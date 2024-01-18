import protobuf_grpc_pb2 as pb2
from faker import Faker
import datetime
from dateutil.relativedelta import relativedelta
import random
import sys


def generate_name(full_name, birth_date):
    faker = Faker('en_US')
    name = pb2.Name()
    name.use = faker.word(ext_word_list=['usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden'])
    name.text = full_name
    name.given = full_name.split(' ')[0]
    name.family = full_name.split(' ')[1]
    name.active = faker.date_between(start_date=datetime.datetime.strptime(birth_date, '%m/%d/%Y')).strftime('%m/%d/%Y')
    return name


def generate_telecom(birth_date, given, family):
    faker = Faker('en_US')
    contact_point = pb2.Telecom()
    contact_point.system = faker.word(ext_word_list=['phone', 'fax', 'email', 'sms'])
    contact_point.use = faker.word(ext_word_list=['home', 'work', 'temp', 'old', 'mobile'])
    contact_point.rank = 0  # set in gen_patient()
    contact_point.active = faker.date_between(start_date=datetime.datetime.strptime(birth_date,
                                              '%m/%d/%Y')).strftime('%m/%d/%Y')
    if contact_point.system == 'email':
        contact_point.value = f'{given}{family}@{faker.domain_name()}'
    else:
        contact_point.value = faker.phone_number()
    return contact_point


def generate_address(birth_date):
    faker = Faker('en_US')
    address = pb2.Address()
    address.use = faker.word(ext_word_list=['home', 'work', 'temp', 'old', 'billing'])
    address.type = faker.word(ext_word_list=['postal', 'physical', 'both'])
    address.line = faker.street_address()
    address.city = faker.city()
    address.state = faker.word(ext_word_list=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI",
                                              "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI",
                                              "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                                              "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
                                              "VT", "VA", "WA", "WV", "WI", "WY"])
    address.zipcode = faker.postcode()
    address.country = 'USA'
    address.period['start'] = faker.date_between(start_date=datetime.datetime.strptime(birth_date,
                                                 '%m/%d/%Y')).strftime('%m/%d/%Y')
    address.period['end'] = '' if address.use in ['home', 'work', 'billing'] else faker.date_between(
                            start_date=datetime.datetime.strptime(address.period['start'], '%m/%d/%Y')
                            + relativedelta(years=1)).strftime('%m/%d/%Y')
    address.text = f'{address.line} {address.city}, {address.state} {address.zipcode} {address.country}'
    return address


def generate_contact():
    faker = Faker('en_US')
    contact = pb2.Contact()
    contact.relation = faker.word(ext_word_list=['emergency', 'family', 'guardian', 'friend', 'partner', 'work',
                                                 'caregiver', 'agent', 'guarantor', 'parent'])
    name = faker.name()
    birth_date = faker.date_of_birth(minimum_age=18, maximum_age=100).strftime('%m/%d/%Y')
    contact.name.CopyFrom(generate_name(name, birth_date))
    contact.telecom.CopyFrom(generate_telecom(birth_date, name.split(' ')[0], name.split(' ')[1]))
    contact.address.CopyFrom(generate_address(birth_date))
    return contact


def generate_patients(size):
    curr_size = 0
    patients = pb2.Patients()
    while curr_size < size:
        faker = Faker('en_US')
        # Define preliminary patient attributes using faker
        patient = pb2.Patient()
        patient.id = faker.pyint(min_value=11111, max_value=99999)
        patient.active = faker.boolean(chance_of_getting_true=90)
        patient.gender = faker.word(ext_word_list=['Male', 'Female', 'Non-binary', 'Other'])
        patient.birth_date = faker.date_of_birth(minimum_age=18, maximum_age=100).strftime('%m/%d/%Y')
        patient.deceased_on = (faker.date_between(start_date=datetime.date.today()-relativedelta(years=10)).strftime(
                               '%m/%d/%Y') if datetime.datetime.strptime(patient.birth_date, '%m/%d/%Y')
                               < datetime.datetime.today()-relativedelta(years=65) and
                               faker.boolean(chance_of_getting_true=15) else '')
        patient.marital_status = faker.word(ext_word_list=['Married', 'Single', 'Separated', 'Divorced', 'Widowed'])

        # Set the maximum number of items for each repeated object
        max_names = 3
        max_contact_points = 2
        max_addresses = 2
        max_contacts = 4

        # Generate repeated Name objects
        for x in range(random.randint(1, max_names)):
            if patient.gender == 'Non-Binary' or patient.gender == 'Other':
                full_name = faker.name_nonbinary()
            else:
                full_name = faker.name_male() if patient.gender == 'Male' else faker.name_female()
            patient.names.append(generate_name(full_name, patient.birth_date))
        # Generate repeated Telecom objects
        for x in range(random.randint(1, max_contact_points)):
            given = patient.names[random.randint(0, len(patient.names)-1)].given
            family = patient.names[random.randint(0, len(patient.names)-1)].family
            contact_point = generate_telecom(patient.birth_date, given, family)
            contact_point.rank = x
            patient.telecoms.append(contact_point)
        # Generate repeated Address objects
        for x in range(random.randint(1, max_addresses)):
            patient.addresses.append(generate_address(patient.birth_date))
        # Generate repeated Contact objects
        for x in range(random.randint(1, max_contacts)):
            patient.contacts.append(generate_contact())
        # Update and keep track of size of patients
        patients.all_patients.append(patient)
        curr_size += sys.getsizeof(patient)

    return patients
