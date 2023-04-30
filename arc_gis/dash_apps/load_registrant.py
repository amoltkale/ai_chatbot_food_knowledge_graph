import sys
import os

import psycopg2

import pandas as pd

sys.path.append('../../')
from utils import get_config

def get_welcome_prompt(*, id=32, email="m.hernandez@gmail.com"):
    conn = server_connect()
    # user_df = load_user(conn, id=id)

    # # clean user_df
    # user_meta = convert_df(user_df)

    # # TODO READ PROMPT FROM FILE
    # # Initial prompt
    # prompt = f"Here is some information about a person. There information is given in json format below." \
    #         "Please welcome this person as if you are talking to them, and summarize their business needs, location, and funding needs. " \
    #         "At the end you should ask the user if the information is correct. " \
    #         "Please do not repeat their personal information back to them since they already know this and you are talking to them." \
    #         f"{user_meta}"
    user_df, user_profile = load_user(conn, email=email)
    biz_profile = get_user_business_profile(conn, email=email)
    # prompt = f"""
    #             State the speaker's business and intended use of the funding in one sentence. 
    #             Phrase the response as if you are addressing the author. 
    #             Do not add any preamble like "based on your text". 
    #             Make the response a little personal but not very long".
    #             End by asking "How can I help you"?
    #             Here is the business profile in json format: {profile}
    #          """
    prompt = f"""
                State the speaker's business and intended use of the funding in one sentence. 
                You are directly talking to the author so do not add any preamble like "based on your text". 
                Please treat the person as if you are directly talking with them.
                Make your response professional, friendly, and concise.
                End by asking "How can I help you"?
                Here is general information on the person you are talking to: {user_profile}
                Here is the business profile in json format: {biz_profile}
             """
    print(prompt)
    return prompt

def load_user(conn, *,email):
    user_df = get_user_df(conn, email=email)
    return user_df, convert_df(user_df)

def server_connect():
    # load
    nourish_user = get_config("nourish_db","username")
    nourish_pswd = get_config("nourish_db","passkey")
    conn = psycopg2.connect(
        host="awesome-hw.sdsc.edu",
        database="nourish",
        user=nourish_user,
        password=nourish_pswd)
    return conn

def get_user_df(conn, *, email):
    # Get resgistrant attributes
    # TODO generalize getting table attributes
    col_qry = """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'registrants';
                """

    cur = conn.cursor()

    # execute a statement
    cur.execute(col_qry)

    # display the PostgreSQL database server version
    col_names = cur.fetchall()
    col_names = [c[0] for c in col_names]
        
    # Close the communication with the PostgreSQL
    cur.close()

    # Get registrant of interest
    # create a cursor
    cur = conn.cursor()

    query_str = f"""select * 
                from registrants 
                where email @> '{{{email}}}'
                """

    # execute a statement
    cur.execute(query_str)


    # display the PostgreSQL database server version
    reg_obs = cur.fetchall()

    # Close the communication with the PostgreSQL
    cur.close()

    # make df
    df = pd.DataFrame(reg_obs, columns=col_names)
    return df

def convert_df(df):
    # TODO Generalize dropping
    assert df.shape[0] == 1
    res_df = df.copy()
    res_df.dropna(inplace=True, axis=1)
    res_df.drop(columns=["id", "insert_dts"], inplace=True)
    return {c: res_df[c][0] for c in res_df.columns if "biz" not in c}

def get_user_business_profile(conn, *, email):
    qry = f"""
            select 'My home address is ' || home_street_address || ' '|| home_city || ' '  || home_state || '. ' ||
            case
            when  current_business_description is not null then current_business_description
            else ''
            end ||
            prospective_business_description || ' ' || planned_fund_use as business_profile
            from registrants
            where email @> '{{{email}}}'
            """

    obs = run_qry(conn, qry)

    assert len(obs) == 1

    return {"business_profile": obs[0][0]}

def run_qry(conn, query_str):
    # Get registrant of interest
    # create a cursor
    cur = conn.cursor()

    # execute a statement
    cur.execute(query_str)


    # display the PostgreSQL database server version
    obs = cur.fetchall()

    # Close the communication with the PostgreSQL
    cur.close()

    return obs