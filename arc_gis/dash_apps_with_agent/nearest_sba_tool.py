
import json
from langchain.agents import Tool

from arcgis_functions import nearest_facility

from arcgis.features import FeatureLayer


# import to read configs
import sys
sys.path.append('../../../../')
from utils import get_gis_context


def nearest_sba(json_request: str) -> str:

    ## Sometimes GPT is converting json with single quote  {'home_street_address': '581 Moss St', 'home_zip': '91911', 'home_city': 'Chula Vista', 'home_state': 'CA'}
    ## instead of {"home_street_address": "581 Moss St", "home_zip": "91911", "home_city": "Chula Vista", "home_state": "CA"}
    ## So adding this hack to make it work
    json_string = json_request.replace("'", "\"") 
    arguments = json.loads(json_string)

    
    home_street_address = arguments.get('home_street_address', None)
    home_zip = arguments.get('home_zip', None)
    home_city = arguments.get('home_city', None)
    home_state = arguments.get('home_state', None)
    specific_variables = arguments.get('specific_variables', [])

    gis = get_gis_context()

    sba_feat_layer = FeatureLayer(gis= gis, url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a8d231/FeatureServer/0")

    nearest_sba_json = nearest_facility(originating_address=f"{home_street_address}, {home_zip}, {home_city}, {home_state}", facilities_feat_lyr=sba_feat_layer, gis=gis)

    return json.dumps(nearest_sba_json)


name = 'nearest_sba'
request_format = '{{"home_street_address":"home_street_address","home_zip":"home_zip","home_city":"home_city", "home_state":"home_state","specific_variables":["variable_name"]}}'
output_format = '{{"nearest_sba":"facility_address","sba_name":"sba_name","contact_number":"contact_number","distance":"distance_in_miles","specific_variables":["variable_name"]}}'

## We were getting the below error:
## json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
description = f'''
Helps identofy the query is about SBA or Small Business Administrations.
Input must be valid JSON in the following format with double quotes on the keys and values : {request_format}
Create the input with exactly similar format of JSON with double quotes.
The address should abide by the standard of  United States of America.
If you don't know the value to be assigned to a key, omit the key.
Output must be valid JSON in the following format: {output_format}. 
Round off the distance in miles to 2 decimal places.
'''

# create an instance of the custom langchain tool
NearestSBATool = Tool(
    name=name,
    func=nearest_sba,
    description=description,
    return_direct=False
)