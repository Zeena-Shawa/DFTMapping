import csv
from DataTransformer import transform_addresses

# Determine whether address column is correctly formatted version or not

# extract address based on case

# DAO: Data Access Object
class CsvDao(object):
    file = None
    ADDRESS_CSV_COLUMN = 10

    def __init__(self, file):
        self.file = file

    def load_data(self, filename):
        # load in data
        self.file = filename

    def read_file(self):
        with open(self.file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Skip first line, csv header
            next(csv_reader)
            addresses = list(row[self.ADDRESS_CSV_COLUMN] for row in csv_reader)
            return addresses

    def get_addresses(self):
        transformed_addresses = transform_addresses(self.read_file())
        return transformed_addresses
