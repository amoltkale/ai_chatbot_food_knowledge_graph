
import json
from langchain.agents import Tool

from arcgis_functions import nearest_facility

from arcgis.features import FeatureLayer


# import to read configs
import sys
sys.path.append('../../../../')
from utils import get_gis_context

sys.path.append('../../')
from gis_resources import SBA_FEATURE_LAYER


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

    nearest_sba_json = nearest_facility(originating_address=f"{home_street_address}, {home_zip}, {home_city}, {home_state}", facilities_feat_lyr=SBA_FEATURE_LAYER, gis=gis)

    return json.dumps(nearest_sba_json)


name = 'nearest_sba'
request_format = '{{"home_street_address":"home_street_address","home_zip":"home_zip","home_city":"home_city", "home_state":"home_state","organization_name":"organization_name","contact_instruction":"contact_instruction","specific_variables":["variable_name"]}}'
output_format = '{{"nearest_facility":"facility_address","facility_name":"facility_name","organization_name":"organization_name","contact_number":"contact_number","distance":"distance_in_miles","specific_variables":["variable_name"]}}'

description = f'''
Gives contact information on nearest Small Business Development Agency / SBA / Small Business Administrations /
Small Business Development Agency affiliated with the SBA."
Input must be valid JSON in the following format with double quotes on the keys and values : {request_format}
The address should abide by the standard of  United States of America.
If you don't know the value to be assigned to a key, omit the key.
Output must be valid JSON in the following format: {output_format}. 
Try to refer Small Business Development Agency instead of SBA while responding.
'''

# create an instance of the custom langchain tool
NearestSBATool = Tool(
    name=name,
    func=nearest_sba,
    description=description,
    return_direct=False
)