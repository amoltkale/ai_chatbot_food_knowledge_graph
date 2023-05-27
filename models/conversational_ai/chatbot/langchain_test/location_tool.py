#
# location_tool.py
# A langchain tool that retrieves current location data
#
import json
from langchain.agents import Tool


def location(json_request: str = None) -> str:
    '''
    Returns:
        The current location data in JSON format.
    '''
    data = {}

    # this function is a mockup, returns fake/hardcoded location forecast data
    data['city'] = 'Genova'
    data['country'] = 'Italy'
    # data['latitude'] = 44.411111
    # data['longitude'] = 8.932778
    # data['timezone'] = 'CET'

    return json.dumps(data)


#
# instantiate the langchain tool.
# The tool description instructs the LLM to pass data using a JSON.
# Note the "{{" and "}}": this double quotation is needed
# to avoid a runt-time error triggered by the agent instantiation.
#
name = 'current_location'
description = 'Helps to retrieve current location data (where I\'m now). Returns a JSON with relevant variables'

# create an instance of the custom langchain tool
Location = Tool(
    name=name,
    func=location,
    description=description,
    return_direct=False
)


if __name__ == '__main__':

    print(location())
    # => {"city": "Genova", "country": "Italy", "latitude": 44.411111, "longitude": 8.932778, "timezone": "CET"}

    # print the Location tool
    print(Location)