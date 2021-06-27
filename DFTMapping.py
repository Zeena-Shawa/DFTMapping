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
def print_result(address_info):
    print(address_info['result']['name'] + ' rating: ' + str(address_info['result']["rating"]))
    print(address_info['result']['name'] + ' amount of reviews: ' + str(
        address_info['result']["user_ratings_total"]))
    if 'website' in address_info['result']:
        print(address_info['result']['name'] + ' website: ' + str(address_info['result']['website']))
    return address_info['result']['place_id']

if __name__ == "__main__":
    data_loader = CsvDao("data\Preferences_2addresses.csv")
    addresses = data_loader.get_addresses()
    client = GoogleAPIHttpClient()
    client.setup_places_api()
    # print(client.send_dummy_test('CavendishDentalCare Chesterfield Derbyshire'))
    address_info_list = client.get_address_info(addresses)

    place_ids = []
    for address_info in address_info_list:
        print(address_info)
        if 'result' in address_info:
            place_id = print_result(address_info)
            place_ids.append(place_id)
        # How to deal with double addresses
        elif len(address_info) > 1 and 'result' in address_info[0]:
            for address in address_info:
                place_id = print_result(address)
                place_ids.append(place_id)
        elif 'N/A' in address_info:
            print("nfrvinfen")
        else:
            print(address_info)
            place_ids.append(address_info['result']['place_id'])
            print('no rating')

    client.setup_directions_matrix_api()
    travel_times_London = client.get_directions_to_London(place_ids)
    print(travel_times_London)
    for travel_time in travel_times_London:
        elements = travel_time['rows']
        for element in elements:
            print('Travel time to London:' + str(element['elements'][0]['duration']['text']))









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