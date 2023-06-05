import logging
import requests
import json
from utils.token import *


BASE_URL = 'https://api.zoom.us/v2/'

# FUNCTION TO SEND REQUESTS TO THE ZOOM REST API


def send_request(action, url, data):
    # get OAuth2 token
    t = token()
    # assemble the url for the request
    FINAL_URL = BASE_URL+url
    # convert dict to JSON
    d = json.dumps(data)
    # Assemble Headers
    headers = {'authorization': 'Bearer %s' % t,
               'content-type': 'application/json'}
    # Log the API request
    logging.debug("'URL: {0}', 'headers: {1}', 'body: {2}'".format(
        FINAL_URL, headers, data))
    # send the request
    if action == "post":
        r = requests.post(FINAL_URL, headers=headers, data=d)
    elif action == "patch":
        r = requests.patch(FINAL_URL, headers=headers, data=d)
    elif action == "put":
        r = requests.put(FINAL_URL, headers=headers, data=d)
    elif action == "get":
        r = requests.get(FINAL_URL, headers=headers, data=d)
    elif action == "delete":
        r = requests.delete(FINAL_URL, headers=headers, data=d)
    # Log the successful API response
    if str(r.status_code).startswith('2'):
        logging.info("'Status: {0}', 'RESPONSE: {1}'".format(
            r.status_code, r.content))
    # Log the unsuccessful API response
    else:
        logging.warning("'Status: {0}', 'RESPONSE: {1}'".format(
            r.status_code, r.content))
    print("Status Code: %s" % r.status_code)
    return r.content
