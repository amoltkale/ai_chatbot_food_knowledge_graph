
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


def nearest_sba(address: str) -> str:

    gis = get_gis_context()

    nearest_sba_json = nearest_facility(originating_address=address, facilities_feat_lyr=SBA_FEATURE_LAYER, gis=gis)

    return json.dumps(nearest_sba_json)
    


name = 'nearest_help_center_enhanced'
request_format = '{{"home_street_address":"home_street_address","home_zip":"home_zip","home_city":"home_city", "home_state":"home_state"}}'
output_format = '{{"nearest_facility":"facility_address","facility_name":"facility_name","organization_name":"organization_name","contact_number":"contact_number","distance":"distance_in_miles","specific_variables":["variable_name"]}}'

description = f'''
Gives contact information on nearest help for Small Business Development Agency / SBA / Small Business Administrations /
Small Business Development Agency affiliated with the SBA."
Input must be valid home address from the user or an address provided to be checked for nearest facility from memory.
Output must be valid JSON in the following format: {output_format}. 
Try to refer Small Business Development Agency instead of SBA while responding.
'''

# create an instance of the custom langchain tool
NearestSBAToolEnhanced = Tool(
    name=name,
    func=nearest_sba,
    description=description,
    return_direct=False
)