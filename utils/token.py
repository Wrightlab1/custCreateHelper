import logging
import requests
import json
import base64
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime
import sqlite3


# auth data for getting server to server OAuth Token requires appropriate scopes
# Read variables from .env
load_dotenv()
CLIENT_ID = os.environ.get('CLIENTID')
CLIENT_SECRET = os.environ.get('CLIENTSECRET')
ACCOUNTID = os.environ.get('ACCOUNTID')

# Connect to the local sqlite3 DB
# if DB deos not exist create one


def connectDB():
    logging.info("Checking for sqlite3 table")
    con = sqlite3.connect("token.db")
    c = con.cursor()
    c.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tokens' ''')
    if c.fetchone()[0] == 1:
        logging.info("Table exists")
    else:
        logging.info("Table does NOT exist Creating Table")
        c.execute("CREATE TABLE tokens(uuid INTEGER UNIQUE, token TEXT)")

# Function to fetch a new token from Zoom REST API


def get_token():
    # connect to local db
    con = sqlite3.connect("token.db")
    c = con.cursor()
    # generate basic auth
    logging.info("Fetching NEW Token")
    message = "%s:%s" % (CLIENT_ID, CLIENT_SECRET)
    auth = base64.b64encode(message.encode()).decode()
    # assemble auth headers
    headers = {'authorization': 'Basic %s' % auth,
               'content-type': 'application/json'}
    FINAL_URL = "https://zoom.us/oauth/token?grant_type=account_credentials&account_id=%s" % ACCOUNTID
    # log auth request
    logging.debug("'{0}', '{1}'".format(FINAL_URL, headers))
    # send the API request for OAuth token
    r = requests.post(FINAL_URL, headers=headers)
    # log the successful response
    if str(r.status_code).startswith('2'):
        logging.info("'Status: {0}', 'RESPONSE: {1}'".format(
            r.status_code, r.content))
    # log an error response
    else:
        logging.warning("'Status: {0}', 'RESPONSE: {1}'".format(
            r.status_code, r.content))
    # ensure data is JSON format
    data = json.loads(r.content)
    # find the access token in the JSON response
    token = data['access_token']
    # Write token to DB
    try:
        c.execute(
            "INSERT OR REPLACE INTO tokens(uuid,token) VALUES (?,?)", (1, token,))
        con.commit()
    except sqlite3.Error:
        logging.warning(sqlite3.Error)
    #print("Token from Zoom API: %s" % token)
    return token

# Function to check if a token is expired


def isExpired(t):
    logging.info("Validating Token")
    # decode the token
    decoded = jwt.decode(t, CLIENT_SECRET,
                         options={"verify_signature": False})
    expiry = decoded["exp"]
    # check if token is expired and return boolean
    if expiry < datetime.now().timestamp():
        logging.info("Token Expired = True")
        return True
    else:
        logging.info("Token Expired = False ")
        return False

# Function to manage token usage


def token():
    # connect to the local db
    connectDB()
    con = sqlite3.connect("token.db")
    c = con.cursor()
    try:
        # Get TOken from DB
        logging.info("Fetching token from DB")
        data = c.execute("SELECT token FROM tokens Where uuid = 1").fetchone()
        token = data[0]
    except Exception as ex:
        logging.info("Token not exist in DB")
        token = get_token()
    # check if token is expired
    if isExpired(token) == True:
        # if token expired get new token
        return get_token()
    else:
        # if token not expired use token
        return token
