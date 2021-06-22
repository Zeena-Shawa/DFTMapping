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
        postcode_pattern = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1," \
                           "2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\\s?[0-9][A-Za-z]{2})"
        for address in addresses:
            # Messy, inconsistent data rows
            # link in address
            if 'https://' in address:
                address_truncated = re.sub('\\shttps.*$', '', address)
                clean_address_string_list.append(address_truncated.split(":", 1)[1].strip().rstrip('.'))
            # 2 postcodes
            elif len(re.findall(postcode_pattern, address)) > 1:
                postcodes = re.findall(postcode_pattern, address)
                if 'and' in address:
                    address = re.sub('and', '&', address)
                # Postcodes example
                # [('', 'EN3 5PT', 'EN3', '', 'EN3', 'EN3', '', '', ''), ('', 'N7 0BT', 'N7', 'N7', '', '', '', '', '')]
                second_postcode_index = address.find(postcodes[1][1]) + len(postcodes[1][1])
                clean_address_string_list.append('#' + address[:second_postcode_index])
                continue
            # todo check again
            # special case with following text
            elif 'This post will be split across practice and community' in address:
                clean_address_string_list.append(DataTransformer.clean_split_practice(address).rstrip('.'))
            # N/A text
            elif 'N/A' in address:
                clean_address_string_list.append('')
            # for the rest of the cases, check for Dentistry/clinic/Practice in string (to skip name of DR/MS/MR)
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
                        clean_address_string_list.append(
                            DataTransformer.retrieve_substring_with_regex(comma_split_address,
                                                                          start_substring_index,
                                                                          True,
                                                                          "-"))
                    elif start_substring_index > 0:
                        #print(address)
                        # address is always in last element, so check if last element has it
                            if 'WWW' in comma_split_address[-1]:
                                print("Caught bad address: " + address)
                                # all addresses caught have Title Name - address, website
                                # removing website from the end
                                address_truncated = re.sub(', www.*$', '', address)
                                # split at the first dask, and take the 2nd part of the string, i.e. address
                                clean_address_string_list.append(address_truncated.split("-", 1)[1].strip().rstrip('.'))
                                print("Fixed bad address: " + address_truncated.split("-", 1)[1].strip().rstrip('.'))
                            else:
                                continue
                                # TODO (Jason) : I think the mistake is here, as this line below would have added the
                                #  address as many times as there are 'string' terms in that address
                                #clean_address_string_list.append(', '.join(comma_split_address[start_substring_index:]))
                        # TODO (Jason): So instead I removed it fomr the for loop but kept it under the current if statement
                        #print('NOT TAKEN BY FOR LOOP:' + ', '.join(comma_split_address[start_substring_index:]))
                        clean_address_string_list.append(', '.join(comma_split_address[start_substring_index:]))
            # If no dentistry at this point, remove Longitute xyz text preceding a dash
            elif '-' in address.split(",")[0] and ',' in address:
                clean_address_string_list.append((address.split("-", 1)[1]).strip().rstrip('.'))
            # Remaining cases might contain excess text below
            elif 'HEE Thames Valley and Wessex' in address:
                clean_address_string_list.append(DataTransformer.truncate_hee_thames(address).rstrip('.'))
            else:
                # print(address)
                clean_address_string_list.append(address)

        print(len(clean_address_string_list))
        print(clean_address_string_list)
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

    @staticmethod
    def retrieve_substring_with_regex(comma_split_address, start_substring_index, is_substring_after_index, index_char):
        current_work_string = comma_split_address[start_substring_index]
        dash_index = current_work_string.index(index_char)
        if is_substring_after_index:
            current_work_string = current_work_string[dash_index + 1:]
        comma_split_address[start_substring_index] = current_work_string
        return ', '.join(comma_split_address[start_substring_index:]).strip().rstrip('.')
