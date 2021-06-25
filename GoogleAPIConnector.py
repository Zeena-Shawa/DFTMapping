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

    def setup_places_autocomplete_api(self):
        self.url = 'maps.googleapis.com'
        self.path = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?'

    def send_autocomplete_dummy_test(self, address):
        candidates_dict = self.gmaps.places_autocomplete_query(address, 'textquery', fields=["types", "establishment"])
        print(candidates_dict)
        return self.gmaps.place(candidates_dict['candidates'][0]['place_id'])

    def send_dummy_test(self, address):
        candidates_dict = self.gmaps.find_place(address, 'textquery', fields=None)
        print(candidates_dict)
        return self.gmaps.place(candidates_dict['candidates'][0]['place_id'])

    def get_address_info(self, address_list):
        # Retrieve addresses in form of UUID
        address_uuid_list = []
        row_split = []
        row_count = 1
        for address in address_list:
            if address == '':
                address_uuid_list.append('N/A')
                continue
            elif str(address).startswith("#"):
                addresses_split = str(address).split("&")
                row_split.append(row_count)
                for split_address in addresses_split:
                    address_uuid_list.append(self.gmaps.find_place(split_address, 'textquery'))
            else:
                address_uuid_list.append(self.gmaps.find_place(address, 'textquery'))
            row_count += 1
        return self.find_address_uuid_from_list(address_uuid_list, row_split)

    # TODO merge row_split into one result back
    def find_address_uuid_from_list(self, address_uuid_list, row_split):
        address_list_details = []
        for row_count in range(0, len(address_uuid_list) - 1):
            print(row_count)
            index_address = address_uuid_list[row_count]

            if index_address == 'N/A':
                address_list_details.append("N/A")
            elif len(index_address['candidates']) == 0:
                print(f"Error, found candidate list with 0 results at row: {row_count}")
                address_list_details.append("NULL_CANDIDATES")
            elif row_count in row_split:
                index_address_plus_one = address_uuid_list[row_count + 1]
                joint_address_list = [self.find_place(index_address),
                                      self.find_place(index_address_plus_one)]
                address_list_details.append(joint_address_list)
                row_split.pop(row_split.index(row_count))  # OwO what is this?
                row_count += 1
            else:
                if len(index_address['candidates']) > 1:
                    print(f"Warning, found candidate list with more than 1 result: {index_address}, "
                          f"using first result for row: {row_count}")
                address_list_details.append(self.find_place(index_address))

        return address_list_details

    def find_place(self, address):
        place = self.gmaps.place(address['candidates'][0]['place_id'])
        if 'business_status' in place['result']:
            return place
        else:
            test = self.gmaps.places_nearby(location=place['result']['geometry']['location'],
                                                  radius=100,
                                                  type='dentist')  # try at
            return test