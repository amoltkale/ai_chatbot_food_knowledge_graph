from pathlib import Path

import csv
import pickle

from arcgis.geocoding import geocode

def san_diego_county_zips():
    '''
    TODO
    '''
    with open(Path(__file__).parent.resolve() / "resources/san_diego_county_zips", "rb") as fp:   # Unpickling
        read_list = pickle.load(fp)
    return read_list

def read_exact_food_biz_categories():
    with open(Path(__file__).parent.resolve() / "resources/exact_food_categories.csv", "r") as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        res = []
        for row in reader:
            res.append(row[0])
    return res

def read_exact_unhealthy_food_biz_categories():
    with open(Path(__file__).parent.resolve() / "resources/exact_unhealthy_categories.csv", "r") as fp:   # Unpickling
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        res = []
        for row in reader:
            res.append(row[0])
    return res


def get_lat_long(address):
    try:
        loc = geocode(address)[0]['location']
        ret_val = loc['x'],loc['y']
    except IndexError:
        print(f"Problem with address: {address}")
        ret_val = 0.0,0.0
    return ret_val