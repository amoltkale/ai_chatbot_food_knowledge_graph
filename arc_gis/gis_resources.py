import warnings

from pathlib import Path

import csv
import pickle

import psycopg2

from arcgis.geocoding import geocode
from arcgis.features import FeatureLayer

import sys
sys.path.append('../../')
from utils import get_gis_context

gis = get_gis_context()
SD_BLOCK_GROUP_OPPORTUNITY_SCORE_LAYER = FeatureLayer(url="https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a3eb8f/FeatureServer/0")
SBA_FEATURE_LAYER = FeatureLayer(gis= gis, url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a8d231/FeatureServer/0")
SANDAG_MGRA_FEATURE_LAYER = FeatureLayer(gis=gis, url="https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/SANDAG_MGRA13/FeatureServer/0")


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

def create_where_clause(in_list):
    '''
    This is only applicable for ca_business table from postgresSQL nourish db
    '''
    qry_where_list = []
    for c in in_list:

        if "'" in c:
            where_part = c.replace("'", "''")
            where_part = "'" + where_part + "' = any(categories) OR "
        else:
            where_part = "'" + c + "' = any(categories) OR "
        qry_where_list.append(where_part)
    # clean up last or
    qry_where_list[-1] = qry_where_list[-1].replace(" OR ", "")

    qry_where = "WHERE ("
    for w in qry_where_list:
        qry_where = fr"{qry_where}{w} "
    qry_where = qry_where  + "))"
    return qry_where

def get_lat_long(address):
    try:
        loc = geocode(address)[0]['location']
        ret_val = loc['x'],loc['y']
    except IndexError:
        print(f"Problem with address: {address}")
        ret_val = 0.0,0.0
    return ret_val

def execute_sql(conn, qry):
    '''
    This executed the SQL query and returns the output in form of a list.
    '''
    cur = conn.cursor()

    # execute a statement
    cur.execute(qry)


    # display the PostgreSQL database server version
    res = cur.fetchall()
    # res = [c[0] for c in col_names]

    # Close the communication with the PostgreSQL
    cur.close()
    
    return res

def create_feature_layer(gis, sdf, title, tags, folder='nourish_gis'):
    items = gis.content.search(query="title:'{}' AND type:'Feature Service'".format(title))
    if len(items) > 0 and items[0].owner=='akale_UCSD':
        warnings.warn("Feature Layer already exists with title {}".format(title), category=UserWarning)
        lyr = items[0].layers[0]
        return lyr
    else:
        # Convert back from a SEDF into a feature layer, and publishing on AGOL
        my_new_featurelayer = sdf.spatial.to_featurelayer(title=title, 
                                                                 gis=gis, 
                                                                 folder='nourish_gis',
                                                                 tags=tags)
        lyr = my_new_featurelayer.layers[0]
        return lyr