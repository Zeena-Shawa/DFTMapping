# DFTMapping Script
# Authors: Zeena Shawa, Jason Sklavenitis

# how to add instance of package to pycharm: https://stackoverflow.com/questions/35623776/import-numpy-on-pycharm
import numpy as np
import pandas as pd

# load in data
data = pd.read_csv('C:\Users\User\PycharmProjects\DFTMapping')
print(data['Description'])

# def MappingInfo(address, ):

# Determine whether address column is correctly formatted version or not
for row in data.row:
    print(data.iloc[row]['Description'])
    if ':' in data.iloc[row]['Description'] :
        print(True)

# extract address based on case

# find nearest_city

# retrieve dist_nearest_city

# retrieve star_rating

# retrieve num_reviews

# retrieve website (what our guess is for the website)


# return nearest_city, dist_nearest_city, star_rating, num_reviews, website

