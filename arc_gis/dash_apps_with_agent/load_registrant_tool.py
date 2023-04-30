from langchain.agents import Tool

from load_registrant import get_welcome_prompt


def load_registrant(request: str = None) -> str:
    return request


#
# instantiate the langchain tool.
# The tool description instructs the LLM to pass data using a JSON.
# Note the "{{" and "}}": this double quotation is needed to avoid a runt-time error triggered by the agent instatiation.
#
name = "load_registrant"
request_format = '{{"specific_variables":["variable_name"]"}}'


#request_format = '{{"first_name":"first_name","id":"id","email":"email", "langauges_spoken":"langauges_spoken", "langauges_written":"langauges_written", "location","home_state","specific_variables":["variable_name"]}}'
response_format = '{{"response":"response"}}'
description = f'''
Please remember to professional and friendly to the Human interacting.
Input must be JSON in the following format : {request_format}
{get_welcome_prompt()}
Respond as if you are talking to a person by greeting them by name.
'''


LoadRegistrant = Tool(
    name=name,
    func=load_registrant,
    description=description,
    return_direct=False
)