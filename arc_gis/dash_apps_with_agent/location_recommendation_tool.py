#
#
# A langchain tool that retrieves (fake) location recommendations.
#
import json
from typing import List
from langchain.agents import Tool

from arcgis_functions import get_block_group_map


def location_map_retreiver(
    location: str = None,
    radius: str = None,
    specific_variables: List[str] = []
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

    verbal_desc_map = get_block_group_map(location, radius)  

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
        data['radius'] = '2.0'

    # if required variable names are not included in the data section,
    # the attribute is added to the dictionary with value I don't know.
    for variable_name in specific_variables:
        if variable_name not in data.keys():
            data[variable_name] = 'data not available'


    return json.dumps(data)


def location_recommendation(json_request: str) -> str:
    '''
    wraps the location_biz_type_retriever function,
    converting the input JSON in separated arguments.

    Args:
        request (str): The JSON dictionary input string.

        Takes a JSON dictionary as input in the form:
            { "location":"<location>", "food_biz_type":"<food_biz_type>", "specific_variables":["variable_name", ... ]}

        Example:
            { "location":"Chula Vista", "food_biz_type":"Mexican Grocery Store", "specific_variables":["humidity"]}

    Returns:
        The location and food business type.
    '''
    arguments = json.loads(json_request)

    
    location = arguments.get('location', None)
    # food_biz_type = arguments.get('food_biz_type', None)
    radius = arguments.get('radius', None)
    specific_variables = arguments.get('specific_variables', [])

    return location_map_retreiver(location, radius, specific_variables)


#
# instantiate the langchain tool.
# The tool description instructs the LLM to pass data using a JSON.
# Note the "{{" and "}}": this double quotation is needed
# to avoid a runt-time error triggered by the agent instatiation.
#
name = 'location_recommendation'
request_format = '{{"location":"location","radius":"radius","specific_variables":["variable_name"]}}'
output_format = '{{"file_path":"file_path","verbal_desc":"verbal_desc","location":"location","radius":"radius"}}'
print("----")
print(request_format)
print("----")
## We were getting the below error:
## json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
description = f'''
Helps to identify the intent of the question.
Input must be valid JSON in the following format with double quotes. DO NOT USE SINGLE QUOTES. : {request_format}
In the input format, do not add units for radius. Just keep a float value such as 2.0.
Supply "specific_variables" list just if you really need them.
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