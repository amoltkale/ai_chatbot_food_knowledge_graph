import configparser
import os

def get_config(section_name,config_name):
    # Reading the configuration
    parse = configparser.ConfigParser()
    parse.read(os.path.dirname(__file__)+"/config.ini")
    config_details = parse.get(section_name, config_name)
    print(str(parse))
    return config_details
    
def format_json(rings_json):    
    new_string = ""

    for char in rings_json:
        if char == "'":
            new_string += "\""
        else:
            new_string += char
            
    return new_string