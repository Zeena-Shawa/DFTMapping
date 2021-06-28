import re

postcode_pattern = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1," \
                   "2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\\s?[0-9][A-Za-z]{2})"
clean_address_string_list = []


def transform_addresses(addresses):
    clean_address_string_list.clear()
    # Messy, inconsistent data rows
    for address in addresses:
        # link in address
        # clean_address_string_list.append()
        if 'https://' in address:
            address_truncated = re.sub('\\shttps.*$', '', address)
            if ':' in address_truncated:
                clean_address_string_list.append(address_truncated.split(":", 1)[1].strip().rstrip('.'))
            elif '-' in address_truncated:
                clean_address_string_list.append(address_truncated.split("-", 1)[1].strip().rstrip('.'))
        # 2 postcodes
        elif len(re.findall(postcode_pattern, address)) > 1:
            handle_double_postcode_addresses(address)
        # todo check again
        # special case with following text
        elif 'This post will be split across practice and community' in address:
            clean_split_practice(address)
        # N/A text
        elif 'N/A' in address:
            clean_address_string_list.append('')
        # for the rest of the cases, check for Dentistry/clinic/Practice in string (to skip name of DR/MS/MR)
        elif check_dent_exists_in_substring(address):
            if ',' in address:
                add_comma_addresses_to_list(address)
            else:
                clean_address_string_list.append(truncate_hee_thames(address))
        # If no dentistry at this point, remove Longitute xyz text preceding a dash
        elif '-' in address.split(",")[0] and ',' in address:
            clean_address_string_list.append((address.split("-", 1)[1]).strip().rstrip('.'))
        # Remaining cases might contain excess text below
        elif 'HEE Thames Valley and Wessex' in address:
            clean_address_string_list.append(truncate_hee_thames(address))
        else:
            clean_address_string_list.append(address.strip().rstrip('.'))

    return clean_address_string_list


def handle_double_postcode_addresses(address):
    postcodes = re.findall(postcode_pattern, address)
    if 'and' in address:
        address = re.sub('and', '&', address)
    # Postcodes example
    # [('', 'EN3 5PT', 'EN3', '', 'EN3', 'EN3', '', '', ''), ('', 'N7 0BT', 'N7', 'N7', '', '', '', '', '')]
    second_postcode_index = address.find(postcodes[1][1]) + len(postcodes[1][1])
    clean_address_string_list.append('#' + address[:second_postcode_index])


def clean_split_practice(address):
    if ':' in address:
        clean_address_string_list.append(address.split(":", 1)[1].strip().rstrip('.'))
    else:
        m = re.search(r"([A-Za-z0-9,\s]+)", address)
        clean_address_string_list.append(m.group(1).strip().rstrip('.'))


def check_dent_exists_in_substring(address):
    comma_separated_address = address.upper().split(",")
    for i in comma_separated_address:
        if ("DENT" in i) or ("PRACTICE" in i) or ("SMIL" in i):
            return True
    return False


def truncate_hee_thames(address):
    substring = 'HEE Thames Valley and Wessex'
    if substring in address:
        return re.sub('-\\s+' + substring, '', address).strip().rstrip('.')
    return address.strip().rstrip('.')


def retrieve_substring_with_regex(comma_split_address, start_substring_index, is_substring_after_index, index_char):
    current_work_string = comma_split_address[start_substring_index]
    dash_index = current_work_string.index(index_char)
    if is_substring_after_index:
        current_work_string = current_work_string[dash_index + 1:]
    comma_split_address[start_substring_index] = current_work_string
    clean_address_string_list.append(', '.join(comma_split_address[start_substring_index:]).strip().rstrip('.'))


def comma_join_address_list(address_list, start_substring_index):
    clean_address_string_list.append(', '.join(address_list[start_substring_index:]).strip().rstrip('.'))


def add_comma_addresses_to_list(address):
    comma_split_address = address.upper().strip().split(",")
    # Always for first result in list
    start_substring_index = [comma_split_address.index(i) for i in comma_split_address if
                             "DENT" in i or "PRACTICE" in i or "SMIL" in i][0]
    if '-' in comma_split_address[start_substring_index]:
        retrieve_substring_with_regex(comma_split_address,
                                      start_substring_index,
                                      True,
                                      "-")
    # TODO recheck else
    else:
        # address is always in last element, so check if last element has it and remove
        if 'WWW' in comma_split_address[-1] and start_substring_index > 0:
            # all addresses caught have Title Name - address, website
            address_truncated = re.sub(', www.*$', '', address)
            # split at the first dash, and take the 2nd part of the string, i.e. address
            clean_address_string_list.append(address_truncated.split("-", 1)[1].strip().rstrip('.'))
        else:
            comma_join_address_list(comma_split_address, start_substring_index)
