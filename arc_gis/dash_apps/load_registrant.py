import sys
import os

import psycopg2

import pandas as pd

sys.path.append('../../')
from utils import get_config

def get_welcome_prompt(*, id=32):
    user_df = load_user(id=id)

    # clean user_df
    user_meta = convert_df(user_df)

    # TODO READ PROMPT FROM FILE
    # Initial prompt
    prompt = f"Here is some information about a person. There information is given in json format below." \
            "Please welcome this person as if you are talking to them, and summarize their business needs, location, and funding needs. " \
            "At the end you should ask the user if the information is correct. " \
            "Please do not repeat their personal information back to them since they already know this and you are talking to them." \
            f"{user_meta}"
    return prompt

def load_user(*,id):
    conn = server_connect()
    user_df = get_user_df(conn, id=id)
    return user_df

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

def get_user_df(conn, *, id):
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

    query_str = f"select * "\
                f"from registrants " \
                f"where id = {id}"

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
    return {c.replace("biz", "business"): res_df[c][0] for c in res_df.columns}