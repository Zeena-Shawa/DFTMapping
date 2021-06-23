# DFTMapping Script
# Authors: Zeena Shawa, Jason Sklavenitis

# how to add instance of package to pycharm: https://stackoverflow.com/questions/35623776/import-numpy-on-pycharm
from DataLoader import CsvDao
from GoogleAPIConnector import GoogleAPIHttpClient

# def MappingInfo(address, ):

# find nearest_city

# retrieve dist_nearest_city

# retrieve star_rating

# retrieve num_reviews

# retrieve website (what our guess is for the website)

# return nearest_city, dist_nearest_city, star_rating, num_reviews, website


if __name__ == "__main__":
    data_loader = CsvDao("data\Preferences.csv")
    addresses = data_loader.get_addresses()
    client = GoogleAPIHttpClient()
    client.setup_places_api()
    #client.send_dummy_test('CavendishDentalCare0x3BChesterfield0x2CDerbyshire')# unicode(s, "utf-8")