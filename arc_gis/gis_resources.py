import os
import pickle

def san_diego_county_zips():
    
    with open(os.path.dirname(__file__)+"/resources/san_diego_county_zips", "rb") as fp:   # Unpickling
        read_list = pickle.load(fp)
    return read_list