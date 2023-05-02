import configparser
import os

import psycopg2

from arcgis.gis import GIS

import pandas as pd


def get_config(section_name,config_name):
    # Reading the configuration
    parse = configparser.ConfigParser()
    parse.read(os.path.dirname(__file__)+"/config.ini")
    config_details = parse.get(section_name, config_name)
    # print(str(parse))
    return config_details
    
def get_gis_context():
    '''
    Return the GIS Object.
    '''
    username = get_config("arcgis","username")
    password = get_config("arcgis","passkey")
    gis = GIS("https://ucsdonline.maps.arcgis.com/home", username=username, password=password)
    return gis

def format_json(rings_json):    
    new_string = ""

    for char in rings_json:
        if char == "'":
            new_string += "\""
        else:
            new_string += char
            
    return new_string

def server_connect():
    # load
    nourish_user = get_config("nourish_db","username")
    nourish_pswd = get_config("nourish_db","passkey")
    conn = psycopg2.connect(
        host="awesome-hw.sdsc.edu",
        database="nourish",
        user=nourish_user,
        password=nourish_pswd)
    return conn

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