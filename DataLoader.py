import csv
import re


# Determine whether address column is correctly formatted version or not

# extract address based on case

# DAO: Data Access Object
class CsvDao(object):
    file = None
    ADDRESS_CSV_COLUMN = 10

    def __init__(self, file):
        self.file = file

    def load_data(self, filename):
        # load in data
        self.file = filename

    def read_file(self):
        with open(self.file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Skip first line, csv header
            next(csv_reader)
            addresses = list(row[self.ADDRESS_CSV_COLUMN] for row in csv_reader)
            return addresses

    def get_addresses(self):
        transformed_addresses = DataTransformer.transform_addresses(self.read_file())
        return transformed_addresses


# https:\/\/[\d\w./]* Regex for link

class DataTransformer(object):

    @staticmethod
    def transform_addresses(addresses):
        clean_address_list = []
        for address in addresses:
            if 'https://' in address:
                address_truncated = re.sub('\\shttps.*$', '', address)
                clean_address_list.append(address_truncated.split(":", 1)[1])
            elif 'This post will be split across practice and community' in address:
                clean_address_list.append(DataTransformer.clean_split_practice(address))
            elif 'N/A' in address:
                clean_address_list.append('')
            else:
                print(address)
                clean_address_list.append(address)

        return clean_address_list

    @staticmethod
    def clean_split_practice(address):
        if ':' in address:
            return address.split(":", 1)[1]
        else:
            m = re.search(r"([A-Za-z0-9,\s]+)", address)
            return m.group(1)

    "Dr Jane Williams - Cerrigcochion Road, Brecon, Ld3 7NS"
    "  https://heeoe.hee.nhs.uk/node/8433   [Derbyshire Scheme]"
    "Matford Dental Clinic, 1A The Venture Centre, Yeoford Way, Marsh Barton Business Centre, Exeter"
    "Gurjit Moore, :  oraco dental PELSALL: Walsall, West Midlands. https://heeoe.hee.nhs.uk/node/8289"
    "Banbury Dental Practice 35 High Street Banbury OX16 5ER - HEE Thames Valley and Wessex"
    "Parkfield Dengh placement where you will spend 12 months in practice as a FD and then 12 months in a hospital post as a DCT at Taunton Hospital."
    "N/A POST"


