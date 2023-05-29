#
#
# A langchain tool that retreives location and radius to plot opportunity map
#
import json
from langchain.agents import Tool

from typing import List

from arcgis_functions import  get_block_group_map_with_opp_comp_score

# import to read configs
import sys
sys.path.append('../../../../')
from utils import get_gis_context


def location_map_retreiver(
    location: str = None,
    state: str = None,
    radius: str = None,
) -> str:
    '''
    The function is an example of a custom python function
    that takes a list of custom arguments and returns a text (or in general any data structure)

    Given a location and radius, this custom function
    returns the intent of the query (in JSON format).

    This is a mockup function, returning a fixed JSON tempalte.
    The function could wrap an external API returning realtime data.

    parameters:
        location: location as text, e.g. 'Chula Vista, San Diego'
        radius: 10 miles
        specific_variables: list of specific/required variable names, e.g ["radius", "2.0"]

    returns:
        Intent of the question along with locationa and business type as a JSON. E.g.
        {"file_path": "static/block_level_map.html", "verbal_desc": " "}

    '''
    data = {}
    verbal_desc_map = get_block_group_map_with_opp_comp_score(f"{location}, {state}", radius, get_gis_context())  

    # this function is a mockup, returns fake/hardcoded weather forecast data
    #data['utterance'] = 'location recommendation'
    data['file_path'] = verbal_desc_map['file_path']
    data['verbal_desc'] = verbal_desc_map['verbal_desc']

    data['location'] = location

    # ERROR/EXCEPTION: DISAMBIGUATION REQUIRED
    # the tool can't elaborate because it doesn't has the mandatory variable 'location',
    # so the returned content is an hardcoded error sentence (not a JSON), requiring a user disambiguation.
    if not location or ('location' in location):
        return 'The location is not specified. Where are you located or your prospective location?'

    # warning: the variable radius is not defined so a default value is assigned
    if not radius or radius == 'radius':
        data['radius'] = '5.0'


    return json.dumps(data)


def location_recommendation(json_request: str) -> str:
    '''
    wraps the location_biz_type_retriever function,
    converting the input JSON in separated arguments.
    '''
    ## Sometimes GPT is converting json with single quote  {'home_street_address': '581 Moss St', 'home_zip': '91911', 'home_city': 'Chula Vista', 'home_state': 'CA'}
    ## instead of {"home_street_address": "581 Moss St", "home_zip": "91911", "home_city": "Chula Vista", "home_state": "CA"}
    ## So adding this hack to make it work
    json_string = json_request.replace("'", "\"") 
    arguments = json.loads(json_string)

    
    location = arguments.get('location', None)
    state = arguments.get('state', None)
    # food_biz_type = arguments.get('food_biz_type', None)
    radius = arguments.get('radius', None)

    return location_map_retreiver(location, state, radius)


#
# instantiate the langchain tool.
# The tool description instructs the LLM to pass data using a JSON.
# Note the "{{" and "}}": this double quotation is needed
# to avoid a runt-time error triggered by the agent instatiation.
#
name = 'business_location_recommendation'
request_format = '{{"location":"location","state":"state","radius":"radius",}}'
output_format = '{{"file_path":"file_path","verbal_desc":"verbal_desc","location":"location","radius":"radius"}}'

## We were getting the below error:
## json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
description = f'''
Helps to identify the intent of the question.
Input must be valid JSON in the following format with double quotes: {request_format}
In the input format, do not add units for radius. Just keep a float value such as 5.0.
If don't know the value to be assigned to a key, omit the key.
Output must be valid JSON in the following format: {output_format}. 
In the output format, do not add units.
'''

# create an instance of the custom langchain tool
LocationRecommendation = Tool(
    name=name,
    func=location_recommendation,
    description=description,
    return_direct=True
)


if __name__ == '__main__':

    print(location_recommendation('{ "location":"Chula Vista", "food_biz_type":"Mexican Grocery Store" }'))
    # => {"location": "Chula Vista", "radius": "within 10 mile radius"}

    print(location_recommendation('{ "location":"Chula Vista" }'))
    # => The business you want to open is not specified. What kind of business do you want to set up?

    # print the Weather tool
    print(LocationRecommendation)