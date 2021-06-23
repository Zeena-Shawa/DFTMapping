import http.client
from configparser import SafeConfigParser

class GoogleAPIHttpClient(object):
    url = ''
    path = ''
    gmaps = ''

    def __init__(self):
        config = SafeConfigParser()
        # do something
        config.read('config.ini')
        print(config.sections())
        # gmaps = googlemaps.Client(key=config['googlemaps']['key'])
        # print(config['googlemaps']['key'])

        pass

    def setup_places_api(self):
        self.url = 'maps.googleapis.com'
        self.path = '/maps/api/place/findplacefromtext/json?'

    def send_dummy_test(self, address):
        connection = http.client.HTTPSConnection(self.url)
        connection.request("GET", self.path + address+"?&fields=photos,formatted_address,name,rating,opening_hours,geometry?key=")
        response = connection.getresponse()
