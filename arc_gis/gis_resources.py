import os
import pickle
from arcgis.geocoding import geocode


def san_diego_county_zips():
    
    with open(os.path.dirname(__file__)+"/resources/san_diego_county_zips", "rb") as fp:   # Unpickling
        read_list = pickle.load(fp)
    return [int(i) for i in read_list]

def get_lat_long(address):
    loc = geocode(address)[0]['location']
    return loc['x'],loc['y']