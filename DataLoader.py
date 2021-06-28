import csv
from DataTransformer import transform_addresses

# Determine whether address column is correctly formatted version or not

# extract address based on case

extra_column_headers = ['rating', 'user_ratings_total', 'url', 'website', 'transit_time_london']


# DAO: Data Access Object
class CsvDao(object):
    file = None
    ADDRESS_CSV_COLUMN = 10

    def __init__(self, file="data\Preferences_ThamesValley.csv"):
        self.file = file

    def load_data(self, filename):
        # load in data
        self.file = filename

    # Both lists are ordered to csv
    def write_addresses_to_file(self, address_list, london_distance_list):
        with open(self.file, 'r') as read_file, open('data\Preferences_ThamesValley_full.csv', 'w') as write_file:
            first_line = read_file.readline()
            write_file.write(first_line.strip('\n') + ',' + ','.join(extra_column_headers) + '\n')
            # read content from first file
            read_file_len = len(address_list)
            print('Read File Length' + str(read_file_len))
            row_count = 0
            for line in read_file:
                # append content to second file
                print(row_count)
                write_file.write(
                    line.strip('\n') + address_list[row_count] + london_distance_list[row_count] + '\n')
                row_count += 1

    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def get_reviews_csv_fornmat(self, address_info):
        rating_and_reviews = [str(address_info['result']["rating"]),
                              str(address_info['result']["user_ratings_total"]),
                              str(address_info['result']['url'])]
        if 'website' in address_info['result']:
            rating_and_reviews.append(str(address_info['result']['website']))
        else:
            rating_and_reviews.append("")
        return rating_and_reviews

    def read_file_addresses(self):
        with open(self.file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Skip first line, csv header
            next(csv_reader)
            addresses = list(row[self.ADDRESS_CSV_COLUMN] for row in csv_reader)
            return addresses

    def get_addresses(self):
        transformed_addresses = transform_addresses(self.read_file_addresses())
        return transformed_addresses
