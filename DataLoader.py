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
        clean_address_string_list = []
        print(len(addresses))
        for address in addresses:
            # Messy, inconsistent data rows
            # TODO check double post codes
            address = re.sub(',\\s+[A-Z\\d\\s]{3,}$', '', address)
            if 'https://' in address:
                address_truncated = re.sub('\\shttps.*$', '', address)
                clean_address_string_list.append(address_truncated.split(":", 1)[1].strip().rstrip('.'))
            # todo check again
            elif 'This post will be split across practice and community' in address:
                clean_address_string_list.append(DataTransformer.clean_split_practice(address).rstrip('.'))
            elif 'N/A' in address:
                clean_address_string_list.append('')
            elif DataTransformer.check_dent_exists_in_substring(address):
                if ',' not in address:
                    # TODO check if spaces between words (capitals) is needed e.g. Billingshurst Dental Practice114 High StreetBillingshurstRH14 9QS
                    clean_address_string_list.append(DataTransformer.truncate_hee_thames(address).rstrip('.'))
                else:
                    comma_split_address = address.upper().strip().split(",")
                    # Always for first result in list
                    start_substring_index = [comma_split_address.index(i) for i in comma_split_address if
                                             "DENT" in i or "PRACTICE" in i or "SMIL" in i][0]
                    if '-' in comma_split_address[start_substring_index]:
                        current_work_string = comma_split_address[start_substring_index]
                        dash_index = current_work_string.index('-')
                        current_work_string = current_work_string[dash_index + 1:]
                        comma_split_address[start_substring_index] = current_work_string
                        clean_address_string_list.append(
                            ', '.join(comma_split_address[start_substring_index:]).strip().rstrip('.'))
                    elif start_substring_index > 0:
                        current_work_string = comma_split_address[start_substring_index]
                        comma_index = current_work_string.index(',')
                        current_work_string = current_work_string[comma_index + 1:]
                        comma_split_address[start_substring_index] = current_work_string
                        clean_address_string_list.append(
                            ', '.join(comma_split_address[start_substring_index:]).strip().rstrip('.'))

            elif '-' in address.split(",")[0] and ',' in address:
                clean_address_string_list.append((address.split("-", 1)[1]).strip().rstrip('.'))
            elif 'HEE Thames Valley and Wessex' in address:
                clean_address_string_list.append(DataTransformer.truncate_hee_thames(address).rstrip('.'))
            else:
                clean_address_string_list.append(address)

        return clean_address_string_list

    @staticmethod
    def clean_split_practice(address):
        if ':' in address:
            return address.split(":", 1)[1]
        else:
            m = re.search(r"([A-Za-z0-9,\s]+)", address)
            return m.group(1)

    @staticmethod
    def check_dent_exists_in_substring(address):
        comma_separated_address = address.upper().split(",")
        for i in comma_separated_address:
            if ("DENT" in i) or ("PRACTICE" in i) or ("SMIL" in i):
                return True
        return False

    @staticmethod
    def truncate_hee_thames(address):
        substring = 'HEE Thames Valley and Wessex'
        if substring in address:
            return re.sub('-\\s+' + substring, '', address)
        return address
