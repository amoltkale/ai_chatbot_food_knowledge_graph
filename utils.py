import configparser
import os

import psycopg2
from langchain import SQLDatabase
from urllib.parse import quote
from arcgis.gis import GIS



class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PURPLE = '\033[35m'       # Purple
    WHITE = '\033[37m'
    WHITE_BG = '\033[47m'
    AMBER = '\u001b[38;5;215m'

def print_in_color(text,color=bcolors.WHITE):
    print(f"{color}{text}{bcolors.ENDC}")

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
        host=get_config("nourish_db","host"),
        database=get_config("nourish_db","db"),
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

def get_postgres_db_obj():
    # Creating Postgres SQL DB
    username = get_config("nourish_db","username")
    password = get_config("nourish_db","passkey")
    host = get_config("nourish_db","host")
    sql_db_name = get_config("nourish_db","db")
    sql_db = SQLDatabase.from_uri(f"postgresql://{username}:%s@{host}/{sql_db_name}" % quote(password))
    return sql_db