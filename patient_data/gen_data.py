import random
from faker import Faker
from ujson import dumps
from enum import Enum
import sys
from datetime import date
from dateutil.relativedelta import relativedelta
import protobuf_grpc as proto
import patient_dataclass as pd
from dataclasses import asdict

faker = Faker('en_US')


# Method to create a fake name
def generate_name(seed, birth_date, gender=''):
    Faker.seed(seed)
    if gender == 'Non-Binary' or gender == 'Other':
        full_name = faker.name_nonbinary()
    elif gender == 'Male':
        full_name = faker.name_male()
    elif gender == 'Female':
        full_name = faker.name_female()
    else:
        full_name = faker.name()
    n = pd.Name(
        faker.word(ext_word_list=['usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden']),
        full_name,
        full_name.split(' ')[0],
        full_name.split(' ')[1],
        faker.date_between(start_date=birth_date)
    )

    return n


# Method to create a fake telecom
def generate_telecom(seed, rank, birth_date, names):
    Faker.seed(seed)
    t = pd.Telecom(
        faker.word(ext_word_list=['phone', 'fax', 'email', 'sms']),
        faker.word(ext_word_list=['home', 'work', 'temp', 'old', 'mobile']),
        rank,
        faker.date_between(start_date=birth_date)
    )
    if t.system == 'email':
        t.value = f'{names[random.randint(0, len(names) - 1)].given}' \
                  f'{names[random.randint(0, len(names) - 1)].family}@{faker.domain_name()}'
    else:
        t.value = faker.phone_number()

    return t


# Method to create a fake address
def generate_address(seed, birth_date):
    Faker.seed(seed)
    a = pd.Address(
        faker.word(ext_word_list=['home', 'work', 'temp', 'old', 'billing']),
        faker.word(ext_word_list=['postal', 'physical', 'both']),
        faker.street_address(),
        faker.city(),
        faker.state(),
        faker.postcode(),
        'USA',
        faker.date_between(start_date=birth_date),
    )
    a.text = f'{a.line} {a.city}, {a.state} {a.zipcode} {a.country}'
    if a.use in ['temp', 'old']:
        a.period_end = faker.date_between(start_date=a.period_start + relativedelta(years=1))

    return a


# Format class for ease of selecting data format
class Format(Enum):
    Json = 1
    Protobuf = 2

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)


def main(size, data_format: Format):
    # Set-up
    curr_size = 0
    seed = 1
    patient_list = []

    # Set the maximum number of items for each repeated dataclass
    max_names = 3
    max_telecoms = 2
    max_addresses = 2
    max_contacts = 4

    # Generate patients
    while curr_size < size:
        Faker.seed(seed)
        random.seed(seed)
        p = pd.Patient(
            faker.pyint(min_value=11111, max_value=99999),
            faker.boolean(chance_of_getting_true=90),
            faker.word(ext_word_list=['Male', 'Female', 'Non-binary', 'Other']),
            faker.date_of_birth(minimum_age=18, maximum_age=100),
            faker.word(ext_word_list=['Married', 'Single', 'Separated', 'Divorced', 'Widowed'])
        )

        # Find date of death if applicable
        if p.birth_date < date.today() - relativedelta(years=65) and \
           faker.boolean(chance_of_getting_true=15):
            p.deceased_on = faker.date_between(start_date=date.today()-relativedelta(years=10)).strftime('%m/%d/%Y')

        # Generate names
        for x in range(random.randint(1, max_names)):
            seed += 1
            p.names.append(generate_name(seed, p.birth_date, p.gender))

        # Generate telecoms
        for x in range(random.randint(1, max_telecoms)):
            seed += 1
            p.telecoms.append(generate_telecom(seed, x+1, p.birth_date, p.names))

        # Generate addresses
        for x in range(random.randint(1, max_addresses)):
            seed += 1
            p.addresses.append(generate_address(seed, p.birth_date))
        # Generate contacts
        for x in range(random.randint(1, max_contacts)):
            c_birth_date = faker.date_of_birth(minimum_age=18, maximum_age=100)
            c = pd.Contact(
                faker.word(ext_word_list=['emergency', 'family', 'guardian', 'friend', 'partner', 'work',
                                          'caregiver', 'agent', 'guarantor', 'parent']),
                generate_name(seed+1, c_birth_date),
                generate_address(seed+1, c_birth_date)
            )
            seed += 3
            c.telecom = generate_telecom(seed, 1, c_birth_date, [c.name])
            p.contacts.append(c)
        # Add patient to list and keep track of size
        patient_list.append(p)
        curr_size += sys.getsizeof(p)
        seed += 1

    match data_format:
        case Format.Json:
            return dumps([asdict(p) for p in patient_list], indent=4, default=str)
        case Format.Protobuf:
            return proto.generate_patients(patient_list).all_patients


if __name__ == '__main__':
    print(main(128, Format.Protobuf))
