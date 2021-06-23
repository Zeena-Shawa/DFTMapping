from configparser import SafeConfigParser
import googlemaps


class GoogleAPIHttpClient(object):
    url = ''
    path = ''
    gmaps = None

    def __init__(self):
        config = SafeConfigParser()
        # do something
        config.read('config.ini')
        self.gmaps = googlemaps.Client(key=config['googlemaps']['key'], queries_per_second=100)
        pass

    def setup_places_api(self):
        self.url = 'maps.googleapis.com'
        self.path = '/maps/api/place/findplacefromtext/json?'

    def send_dummy_test(self, address):
        candidates_dict = self.gmaps.find_place(address, 'textquery', fields=None)
        print(candidates_dict)
        return self.gmaps.place(candidates_dict['candidates'][0]['place_id'])

    def get_address_info(self, address_list):
        address_uuid_list = []
        row_split = []
        row_count = 1
        for address in address_list:
            print(address)
            if address == '':
                address_uuid_list.append('N/A')
                continue
            elif str(address).startswith("#"):
                addresses_split = str(address).split("&")
                for split_address in addresses_split:
                    address_uuid_list.append(split_address)
                    row_split.append(row_count)
            address_uuid_list.append(self.gmaps.find_place(address, 'textquery'))
            row_count += 1
        return self.find_address_uuid_from_list(address_uuid_list, row_split)

    # TODO merge row_split into one result back
    def find_address_uuid_from_list(self, address_uuid_list, row_split):
        address_list_details = []
        print(len(address_uuid_list))
        row_count = 0
        for candidate_list in address_uuid_list:

            print(candidate_list['candidates'])
            if candidate_list == 'N/A':
                address_list_details.append("N/A")
                continue
            if len(candidate_list['candidates']) > 1:
                print(f"Warning, found candidate list with more than 1 result: {candidate_list}, "
                      f"using first result for row: {row_count}")
            elif len(candidate_list['candidates']) == 0:
                print(f"Error, found candidate list with 0 results at row: {row_count}")
                address_list_details.append("NULL_CANDIDATES")
                continue

            #row split contains row count
            address_list_details.append(self.gmaps.place(candidate_list['candidates'][0]['place_id']))
            #address_2 = self.gmaps.place(candidate_list['candidates'][0]['place_id'])
            #address_1 = address_list_details[len(address_list_details)]

            row_count += 1
        print(len(address_list_details))
        return address_list_details
