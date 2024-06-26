from langchain.agents import Tool

import pandas as pd

from load_registrant import server_connect, run_qry, get_user_funding_needs, get_user_business_profile, get_email

def get_funding_prompt():
    email = get_email()
    conn = server_connect()
    qry = """
    SELECT funding_program,
            use_of_funds || business_eligibility || application_requirements AS eligibility
    FROM funding_src
    WHERE id = 3 OR id = 1 
    """

    obs = run_qry(conn, qry)
    funding_df = pd.DataFrame(obs, columns=["funding_program",
                            "eligibility"])
    res_json = {}
    for t in funding_df.itertuples():
        res_json[f"{t.funding_program}"] = t.eligibility

    funding_profile = get_user_funding_needs(conn, email=email)
    biz_profile = get_user_business_profile(conn, email=email)

    template = f"""
                REMEMBER YOU ARE TALKING DIRECTLY TO THE USER.
                Do not answer question about loan locations.
                Do not make any assumptions. You should only refer to the information.
                Here is a json describing loans. The highest level key is the loan name.
                For each loan in the json format, tell the user if they are eligible
                for any of the loans based on the business_eligibility key under each loan key.
                Here is the loan json: {{{res_json}}}
                Here is the user's planned use of funds: {{{funding_profile}}}
                Here is the user's business profile: {{{biz_profile}}}.
                If the Application is eligible for any loan, tell them the loan name.
                If they do not qualify for any loands, state the reason.
                Phrase the response as if you are addressing the applicant.
                Answer question to talk more about loan eligibility.
                """
    #print(template)
    return template
        # t["funding_program"]


def format_funding(request: str = None) -> str:
    return request


#
# instantiate the langchain tool.
# The tool description instructs the LLM to pass data using a JSON.
# Note the "{{" and "}}": this double quotation is needed to avoid a runt-time error triggered by the agent instatiation.
#


name = "funding_recommendation_tool"
request_format = '{{"planned_fund_use":"planned_fund_use","eligibility":"eligibility","specific_variables":["variable_name"]"}}'

response_format = '{{"response":"response"}}'
description = f'''
Please remember to professional and friendly to the Human interacting.
Input must be JSON in the following format : {request_format}
{get_funding_prompt()}
Respond as if you are talking to a person by greeting them by name.
'''


FundingRecommendation = Tool(
    name=name,
    func=format_funding,
    description=description,
    return_direct=False
)

if __name__ == '__main__':
    print(get_funding_prompt())
