# DFTMapping Script
# Authors: Zeena Shawa, Jason Sklavenitis
# TODO: My takeaways: don't just choose any random method
#  don't copy paste argument names thinking they are consistent
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

        if 'result' in address_info:
            print(address_info['result']['name'] + ' rating: ' + str(address_info['result']["rating"]))
            print(address_info['result']['name'] + ' amount of reviews: ' + str(
                address_info['result']["user_ratings_total"]))
        elif 'results' in address_info:
            for address in address_info['results']:
                if 'rating' in address:
                    print(address['name'] + ' rating: ' + str(address['rating']))
                    print(address['name'] + ' amount of reviews: ' + str(
                         address['user_ratings_total']))
                    break

        elif 'N/A' in address_info:
            print("nfrvinfen")
        else:
            print(address_info)
            print('no rating')












                # if len(address_info) > 1:
                #     print(address_info_list)
                #     print(address_info[0])
                #     # print(address_info[0]['result']['name'] + ' rating: ' + str(address_info[0]['result']["rating"]))
                #     # print(address_info[0]['result']['name'] + ' amount of reviews: ' + str(
                #     #     address_info[0]['result']["user_ratings_total"]))
                #     # print(address_info[1]['result']['name'] + ' rating: ' + str(address_info[1]['result']["rating"]))
                #     # print(address_info[1]['result']['name'] + ' amount of reviews: ' + str(
                #     #     address_info[1]['result']["user_ratings_total"]))
                # else:
                #     continue