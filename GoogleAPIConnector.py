import http.client
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
        self.gmaps = googlemaps.Client(key=config['googlemaps']['key'])
        pass

    def setup_places_api(self):
        self.url = 'maps.googleapis.com'
        self.path = '/maps/api/place/findplacefromtext/json?'

    def send_dummy_test(self, address):
        candidates_dict = self.gmaps.find_place(address, 'textquery')
        return self.gmaps.place(candidates_dict['candidates'][0]['place_id'])
