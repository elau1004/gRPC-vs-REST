from json_rest import Patient
from ujson import dumps
from enum import Enum
import sys
from protobuf_grpc import generate_patients


class Format(Enum):
    Json = 1
    Protobuf = 2

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)


def main(size, data_format: Format):
    curr_size = 0
    patient_list = []
    while curr_size < size:
        p = Patient()
        p.generate_names()
        p.generate_telecoms()
        p.generate_addresses()
        p.generate_contacts()
        patient_list.append(p)
        curr_size += sys.getsizeof(p)
    match data_format:
        case Format.Json:
            return dumps([p.ret_dict() for p in patient_list])
        case Format.Protobuf:
            return generate_patients(size).all_patients


if __name__ == '__main__':
    print(main(128, Format.Protobuf))
