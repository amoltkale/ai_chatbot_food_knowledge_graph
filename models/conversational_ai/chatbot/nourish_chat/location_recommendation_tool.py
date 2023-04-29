#
#
# A langchain tool that retrieves (fake) location recommendations.
#
import json
from typing import List
from langchain.agents import Tool


def location_biz_type_retriever(
    utterance: str = None,
    location: str = None,
    food_biz_type: str = None,
    specific_variables: List[str] = []
) -> str:
    '''
    The function is an example of a custom python function
    that takes a list of custom arguments and returns a text (or in general any data structure)

    Given a location and food business type, this custom function
    returns the intent of the query (in JSON format).

    This is a mockup function, returning a fixed text tempalte.
    The function could wrap an external API returning realtime data.

    parameters:
        location: location as text, e.g. 'Chula Vista, San Diego'
        food_biz_type: Food business in the question, e.g. 'Mexican Grocery Store'
        specific_variables: list of specific/required variable names, e.g ["radius", "10 miles"]

    returns:
        Intent of the question along with locationa and business type as a JSON. E.g.
        {"location": "Chula Vista, San Diego", "radius": "within 10 mile radius"}

    '''
    data = {}

    # this function is a mockup, returns fake/hardcoded weather forecast data
    #data['utterance'] = 'location recommendation'
    data['radius'] = 'within 10 mile radius'
    data['utterance'] = 'Thank you for filling up the form, we understand that you want to open a Mexican Grocery Store in Chula Vista within 10 mile radius.'

    # ERROR/EXCEPTION: DISAMBIGUATION REQUIRED
    # the tool can't elaborate because it doesn't has the mandatory variable 'location',
    # so the returned content is an hardcoded error sentence (not a JSON), requiring a user disambiguation.
    if not location or ('location' in location):
        return 'The location is not specified. Where are you located or your prospective location?'

    # warning: the variable food_biz_type is not defined so a default value is assigned
    if not food_biz_type or food_biz_type == 'food_biz_type':
        data['food_biz_type'] = 'Mexican Grocery Store'

    # if required variable names are not included in the data section,
    # the attribute is added to the dictionary with value I don't know.
    for variable_name in specific_variables:
        if variable_name not in data.keys():
            data[variable_name] = 'data not available'

    return json.dumps(data)


def location_recommendation(json_request: str) -> str:
    '''
    wraps the weather_data_retriever function,
    converting the input JSON in separated arguments.

    Args:
        request (str): The JSON dictionary input string.

        Takes a JSON dictionary as input in the form:
            { "location":"<location>", "food_biz_type":"<food_biz_type>", "specific_variables":["variable_name", ... ]}

        Example:
            { "location":"Chula Vista", "food_biz_type":"Mexican Grocery Store", "specific_variables":["humidity"]}

    Returns:
        The utterance with location and food business type.
    '''
    arguments = json.loads(json_request)

    question_intent= arguments.get('utterance', None)
    location = arguments.get('location', None)
    food_biz_type = arguments.get('food_biz_type', None)
    specific_variables = arguments.get('specific_variables', [])

    return location_biz_type_retriever(utterance=question_intent,location=location, food_biz_type=food_biz_type, specific_variables=specific_variables)


#
# instantiate the langchain tool.
# The tool description instructs the LLM to pass data using a JSON.
# Note the "{{" and "}}": this double quotation is needed
# to avoid a runt-time error triggered by the agent instatiation.
#
name = 'location_recommendation'
request_format = '{{"utterance","utterance","location":"location","food_biz_type":"food_biz_type","specific_variables":["variable_name"]}}'
description = f'''
Helps to identify the intent of the question.
Input should be JSON in the following format: {request_format}
Supply "specific_variables" list just if you really need them.
If don't know the value to be assigned to a key, omit the key.
'''

# create an instance of the custom langchain tool
LocationRecommendation = Tool(
    name=name,
    func=location_recommendation,
    description=description,
    return_direct=False
)


if __name__ == '__main__':

    print(location_recommendation('{ "location":"Chula Vista", "food_biz_type":"Mexican Grocery Store" }'))
    # => {"location": "Chula Vista", "radius": "within 10 mile radius"}

    print(location_recommendation('{ "location":"Chula Vista" }'))
    # => The business you want to open is not specified. What kind of business do you want to set up?

    # print the Weather tool
    print(LocationRecommendation)