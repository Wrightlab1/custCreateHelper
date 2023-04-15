# IMPORT
from utils.log import *
from utils.req import *
from utils.printJSON import *

import csv
import base64
import os
from dotenv import load_dotenv

# VARIABLES
load_dotenv()
custDomain = os.environ.get('DOMAIN')
csvFile = os.environ.get('CSVFILE')

# SETUP LOGGING
create_log()

# Function to base 64 encopde the users original email address and add a configurable domain


def createEmail(email):
    encoded_email = base64.b64encode(email.encode())
    newEmail = encoded_email
    return (str(newEmail))

# function to create a new custCreate  user


def createUser(email):
    finalEmail = email[2:] + custDomain
    url = '/users'
    data = {"action": "custCreate", "user_info": {
        "email": finalEmail, "type": 2}}
    # data = {'action' : 'custCreate', 'user_info' : {'email' : %s, 'type' : 2}} % email
    action = "post"
    response = send_request(action, url, data)
    # printJSON(response)

# function to delete old user


def deleteUser(oldEmail, newEmail):
    queryString = "%s?action=delete&transfer+email=%s&transfer_meeting=true&transfer_webinar=true&transfer_recording=true" % (
        oldEmail, newEmail)
    url = '/users/%s' % queryString
    data = {"action": "delete", "transfer_email": newEmail[2:],
            "transfer_meeting": True, "transfer_webinar": True, "transfer_recording": True}
    action = "delete"
    response = send_request(action, url, data)
    # printJSON(response)

# Open CSV FIle containing user email addresses


def migrateUser():
    with open(csvFile) as csv_file:
        # create the reader object
        csv_reader = csv.reader(csv_file)
    # iterate over each row of the file
        for row in csv_reader:
            userEmail = row[0]
        # create anew email address for the user
            email = createEmail(userEmail)
        # create a new custCreate user
            createUser(email)
        # delete old suer and transfer data to new user
            deleteUser(userEmail, email)


migrateUser()
