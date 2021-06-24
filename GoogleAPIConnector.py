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
        # Retrieve addresses in form of UUID
        address_uuid_list = []
        row_split = []
        row_count = 1
        for address in address_list:
            print(row_count)
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
        for row_count in range(0, len(address_uuid_list)):
            index_address = address_uuid_list[row_count]
            index_address_minus_one = address_uuid_list[row_count-1]
            if index_address == 'N/A':
                address_list_details.append("N/A")
            elif len(index_address['candidates']) == 0:
                print(f"Error, fou  nd candidate list with 0 results at row: {row_count}")
                address_list_details.append("NULL_CANDIDATES")
            elif row_count in row_split:
                joint_address_list = [self.gmaps.place(index_address['candidates'][0]['place_id']),
                                      self.gmaps.place(index_address_minus_one['candidates'][0]['place_id'])]
                address_list_details.append(joint_address_list)
                row_split.pop(row_split.index(row_count)) # OwO what is this?
                row_count += 1
            else:
                if len(index_address['candidates']) > 1:
                    print(f"Warning, found candidate list with more than 1 result: {index_address}, "
                          f"using first result for row: {row_count}")
                address_list_details.append(self.gmaps.place(index_address['candidates'][0]['place_id']))

        return address_list_details
