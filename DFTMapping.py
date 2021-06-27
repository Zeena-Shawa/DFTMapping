# DFTMapping Script
# Authors: Zeena Shawa, Jason Sklavenitis
# TODO: My takeaways: don't just choose any random method
#  don't copy paste argument names thinking they are consistent
# how to add instance of package to pycharm: https://stackoverflow.com/questions/35623776/import-numpy-on-pycharm
from DataLoader import CsvDao
from GoogleAPIConnector import GoogleAPIHttpClient

if __name__ == "__main__":
    data_loader = CsvDao()
    addresses = data_loader.get_addresses()
    client = GoogleAPIHttpClient()
    client.setup_places_api()
    address_info_list = client.get_address_info(addresses)

    place_ids = []
    dental_practice_review_info = []
    for address_info in address_info_list:
        if 'result' in address_info:
            dental_practice_review_info.append(','+','.join(data_loader.get_reviews_csv_fornmat(address_info)))
            place_ids.append(address_info['result']['place_id'])
        # How to deal with double addresses
        elif len(address_info) > 1 and 'result' in address_info[0]:
            double_address_reviews = []
            for address in address_info:
                double_address_reviews.append(data_loader.get_reviews_csv_fornmat(address))
                place_ids.append(address['result']['place_id'])

            csv_format_address_reviews = ''
            for column_value_index in range(len(data_loader.get_reviews_csv_fornmat(address_info[0]))):

                csv_format_address_reviews += ','+'\"' + double_address_reviews[0][column_value_index] \
                                              + ',' + double_address_reviews[1][column_value_index] + '\"'

            dental_practice_review_info.append(csv_format_address_reviews)
        elif 'N/A' in address_info:
            print("nfrvinfen")
        else:
            dental_practice_review_info.append(','+','.join(data_loader.get_reviews_csv_fornmat(address_info)))
            place_ids.append(address_info['result']['place_id'])

    client.setup_directions_matrix_api()
    travel_times_London = client.get_directions_to_London(place_ids)
    london_distance_list = []
    for distance_object in travel_times_London:
        distance_to_london = ''
        if isinstance(distance_object, list):
            distance_to_london += ',\"'
            distance_to_london_list = []
            for element in distance_object:
                elements = element['rows']
                distance_to_london_list.append(str(elements[0]['elements'][0]['duration']['text']))
            distance_to_london += ','.join(distance_to_london_list)
            distance_to_london += '\"'
        else:
            elements = distance_object['rows']
            distance_to_london += ','+str(elements[0]['elements'][0]['duration']['text'])

        london_distance_list.append(distance_to_london)

    data_loader.write_addresses_to_file(dental_practice_review_info, london_distance_list)
