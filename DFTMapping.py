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
    data_loader = CsvDao("data\Preferences_small.csv")
    addresses = data_loader.get_addresses()
    client = GoogleAPIHttpClient()
    client.setup_places_api()
    # print(client.send_dummy_test('CavendishDentalCare Chesterfield Derbyshire'))
    address_info_list = client.get_address_info(addresses)
    for address_info in address_info_list:
        try:
            print(address_info['result']['name'] + ' rating: ' + str(address_info['result']["rating"]))
            print(address_info['result']['name'] + ' amount of reviews: ' + str(
                address_info['result']["user_ratings_total"]))
        except:
            if 'N/A' in address_info:
                print("nfrvinfen")
            else:
                print("no rating")
