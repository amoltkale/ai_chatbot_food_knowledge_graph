import os
import pickle
from arcgis.geocoding import geocode


def san_diego_county_zips():
    
    with open(os.path.dirname(__file__)+"/resources/san_diego_county_zips", "rb") as fp:   # Unpickling
        read_list = pickle.load(fp)
    return [i for i in read_list]

def get_lat_long(address):
    try:
        loc = geocode(address)[0]['location']
        ret_val = loc['x'],loc['y']
    except IndexError:
        print(f"Problem with address: {address}")
        ret_val = 0.0,0.0
    return ret_val