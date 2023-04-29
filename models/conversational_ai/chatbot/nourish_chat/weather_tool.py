#
# weather_tool.py
# A langchain tool that retrieves (fake) weather forecasts data
#
import json
from typing import List
from langchain.agents import Tool


def weather_data_retriever(
    location: str = None,
    period: str = None,
    specific_variables: List[str] = []
) -> str:
    '''
    The function is an example of a custom python function
    that takes a list of custom arguments and returns a text (or in general any data structure)

    Given a location and a time period, this custom function
    returns weather forecast as a data structure (in JSON format).

    This is a mockup function, returning a fixed text tempalte.
    The function could wrap an external API returning realtime weather forecast.

    parameters:
        location: location as text, e.g. 'Genova, Italy'
        period: time period, e.g. 'today'
        specific_variables: list of specific/required variable names, e.g ["temperature", "humidity"]

    returns:
        weather foreast description as a JSON. E.g.
        {"forecast": "sunny all the day", "temperature": "20 degrees Celsius"}

    '''
    data = {}

    # this function is a mockup, returns fake/hardcoded weather forecast data
    data['forecast'] = 'sunny'
    data['temperature'] = '20 degrees Celsius'

    # ERROR/EXCEPTION: DISAMBIGUATION REQUIRED
    # the tool can't elaborate because it doesn't has the mandatory variable 'location',
    # so the returned content is an hardcoded error sentence (not a JSON), requiring a user disambiguation.
    if not location or ('location' in location):
        return 'The location is not specified. Where are you?'

    # warning: the variable period is not defined so a default value is assigned
    if not period or period == 'period':
        data['period'] = 'now'

    # if required variable names are not included in the data section,
    # the attribute is added to the dictionary with value I don't know.
    for variable_name in specific_variables:
        if variable_name not in data.keys():
            data[variable_name] = 'data not available'

    return json.dumps(data)


def weather(json_request: str) -> str:
    '''
    wraps the weather_data_retriever function,
    converting the input JSON in separated arguments.

    Args:
        request (str): The JSON dictionary input string.

        Takes a JSON dictionary as input in the form:
            { "period":"<period>", "location":"<location>", "specific_variables":["variable_name", ... ]}

        Example:
            { "period":"today", "location":"Genova, Italy", "specific_variables":["humidity"]}

    Returns:
        The weather data for the specified location and time.
    '''
    arguments = json.loads(json_request)

    location = arguments.get('location', None)
    period = arguments.get('period', None)
    specific_variables = arguments.get('specific_variables', [])

    return weather_data_retriever(location=location, period=period, specific_variables=specific_variables)


#
# instantiate the langchain tool.
# The tool description instructs the LLM to pass data using a JSON.
# Note the "{{" and "}}": this double quotation is needed
# to avoid a runt-time error triggered by the agent instatiation.
#
name = 'weather'
request_format = '{{"period":"period","location":"location","specific_variables":["variable_name"]}}'
description = f'''
Helps to retrieve weather forecast.
Input should be JSON in the following format: {request_format}
Supply "specific_variables" list just if you really need them.
If don't know the value to be assigned to a key, omit the key.
'''

# create an instance of the custom langchain tool
Weather = Tool(
    name=name,
    func=weather,
    description=description,
    return_direct=False
)


if __name__ == '__main__':
    # print(weather_data_retriever(location='Genova, Italy', period='today'))
    # => in Genova, Italy, today is sunny! Temperature is 20 degrees Celsius.

    print(weather('{ "period":"today", "location":"Genova, Italy" }'))
    # => {"forecast": "sunny", "temperature": "20 degrees Celsius"}

    print(weather('{ "period":"today" }'))
    # => The location is not specified. Where are you?

    # print the Weather tool
    print(Weather)