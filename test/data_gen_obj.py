from faker import Faker
import datetime
from dateutil.relativedelta import relativedelta
import sys
import random
from json import dumps


class Telecom:
    def __init__(self, birth_date=datetime.date(2000, 1, 1)):
        faker = Faker('en_US')
        self.__system = faker.word(ext_word_list=['phone', 'fax', 'email', 'sms'])
        self.__value = ''
        self.__use = faker.word(ext_word_list=['home', 'work', 'temp', 'old', 'mobile'])
        self.__rank = 0
        self.__active = faker.date_between(start_date=birth_date).strftime('%m/%d/%Y')

    def set_value(self, first_name, last_name):
        faker = Faker('en_US')
        if self.__system == 'email':
            self.__value = f'{first_name}{last_name}@{faker.domain_name()}'
        else:
            self.__value = faker.phone_number()

    def set_rank(self, num):
        self.__rank = num

    def ret_dict(self):
        return {'System': self.__system,
                'Value': self.__value,
                'Use': self.__use,
                'Rank': self.__rank,
                'Active Since': self.__active}


class Address:
    def __init__(self, birth_date=datetime.date(2000, 1, 1)):
        faker = Faker('en_US')
        self.__use = faker.word(ext_word_list=['home', 'work', 'temp', 'old', 'billing'])
        self.__type = faker.word(ext_word_list=['postal', 'physical', 'both'])
        self.__text = ''
        self.__line = faker.street_address()
        self.__city = faker.city()
        self.__state = faker.word(ext_word_list=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI",
                                                 "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI",
                                                 "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                                                 "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
                                                 "VT", "VA", "WA", "WV", "WI", "WY"])
        self.__zipcode = faker.postcode()
        self.__country = 'USA'
        self.__period = {'start': faker.date_between(start_date=birth_date), 'end': ''}

    def set_text(self):
        self.__text = f'{self.__line} {self.__city}, {self.__state} {self.__zipcode} {self.__country}'

    def set_end_date(self):
        faker = Faker('en_US')
        if self.__use in ['home', 'work', 'billing']:
            self.__period['end'] = ''
        else:
            self.__period['end'] = faker.date_between(
                start_date=self.__period['start'] + relativedelta(years=1))

    def ret_dict(self):
        return {'Use': self.__use,
                'Type': self.__type,
                'Text': self.__text,
                'Line': self.__line,
                'City': self.__city,
                'State': self.__state,
                'Zipcode': self.__zipcode,
                'Country': self.__country,
                'Period': f'{self.__period["start"]} - {self.__period["end"]}'}


class Patient:
    def __init__(self):
        faker = Faker('en_US')
        self.__id = faker.pyint(min_value=11111, max_value=99999)
        self.__active = faker.boolean(chance_of_getting_true=90)
        self.__names = []
        self.__telecoms = []
        self.__gender = faker.word(ext_word_list=['Male', 'Female', 'Non-binary', 'Other'])
        self.__birth_date = faker.date_of_birth(minimum_age=18, maximum_age=100)
        self.__deceased_on = (faker.date_between(start_date=datetime.date.today()-relativedelta(years=10))
                              if self.__birth_date < datetime.date.today()-relativedelta(years=65) and
                              faker.boolean(chance_of_getting_true=15) else '')
        self.__addresses = []
        self.__marital_status = faker.word(ext_word_list=['Married', 'Single', 'Separated', 'Divorced', 'Widowed'])
        self.__contacts = []

    def generate_names(self, max_names=3):
        faker = Faker('en_US')
        for x in range(random.randint(1, max_names)):
            if self.__gender == 'Non-Binary' or self.__gender == 'Other':
                full_name = faker.name_nonbinary()
            else:
                full_name = faker.name_male() if self.__gender == 'Male' else faker.name_female()
            name = {
                'use': faker.word(ext_word_list=['usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden']),
                'text': full_name,
                'given': full_name.split(' ')[0],
                'family': full_name.split(' ')[1],
                'active': faker.date_between(start_date=self.__birth_date).strftime('%m/%d/%Y')
            }
            self.__names.append(name)

    def generate_telecoms(self, max_contact_points=3):
        for x in range(random.randint(1, max_contact_points)):
            contact_point = Telecom(birth_date=self.__birth_date)
            contact_point.set_value(self.__names[random.randint(0, len(self.__names)-1)]['given'],
                                    self.__names[random.randint(0, len(self.__names)-1)]['family'])
            contact_point.set_rank(x)
            self.__telecoms.append(contact_point)

    def generate_addresses(self, max_addresses=3):
        for x in range(random.randint(1, max_addresses)):
            address = Address(birth_date=self.__birth_date)
            address.set_text()
            address.set_end_date()
            self.__addresses.append(address)

    def generate_contacts(self, max_contacts=3):
        faker = Faker('en_US')
        for x in range(random.randint(1, max_contacts)):
            contact = {
                'relation': faker.word(ext_word_list=['emergency', 'family', 'guardian', 'friend', 'partner', 'work',
                                                      'caregiver', 'agent', 'guarantor', 'parent']),
                'name': faker.name(),
                'telecom': Telecom(),
                'address': Address()
            }
            contact['telecom'].set_value(contact['name'].split(' ')[0], contact['name'].split(' ')[1])
            contact['telecom'].set_rank(x)
            contact['address'].set_text()
            contact['address'].set_end_date()
            self.__contacts.append(contact)

    def ret_dict(self):
        p_dict = {
            'ID': self.__id,
            'Active': self.__active,
            'Names': self.__names,
            'Telecoms': [t.ret_dict() for t in self.__telecoms],
            'Gender': self.__gender,
            'Date of Birth': self.__birth_date.strftime('%m/%d/%Y'),
            'Deceased Date': self.__deceased_on.strftime('%m/%d/%Y') if self.__deceased_on != '' else self.__deceased_on,
            'Addresses': [a.ret_dict() for a in self.__addresses],
            'Marital Status': self.__marital_status,
            'Contacts': [{'Relation': c["relation"],
                          'Name': c["name"] ,
                          'Telecom': c["telecom"].ret_dict(),
                          'Address': c["address"].ret_dict()}
                         for c in self.__contacts]
        }
        return p_dict


def main(size):
    curr_size = 0
    patient_list = []
    while curr_size < size:
        p = Patient()
        p.generate_names()
        p.generate_telecoms()
        p.generate_addresses()
        p.generate_contacts()
        patient_list.append(p)
        print(dumps(p.ret_dict(), indent=4))
        curr_size += sys.getsizeof(p)

    return patient_list


if __name__ == '__main__':
    print(main(128))
