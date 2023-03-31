import configparser
import os

def get_config(section_name,config_name):
    # Reading the configuration
    parse = configparser.ConfigParser()
    config = parse.read(os.path.dirname(__file__)+"/config.ini")
    config_details = parse.get(section_name, config_name)
    print(str(parse))
    return config_details
    