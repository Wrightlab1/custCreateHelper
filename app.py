# IMPORT
from utils.log import *
from utils.req import *
from utils.printJSON import *

import csv
import base64
import os
import json
from dotenv import load_dotenv

# VARIABLES
load_dotenv()
custDomain = os.environ.get('DOMAIN')
csvFile = os.environ.get('CSVFILE')

# SETUP LOGGING
create_log()

# Create a new email address for the user by Base64 encoding the original email address


def createEmail(email):
    encoded_email = base64.b64encode(email.encode())
    newEmail = encoded_email
    return (str(newEmail))

# create a new custCreate  user


def createUser(email):
    finalEmail = email[2:] + custDomain
    url = '/users'
    data = {"action": "custCreate", "user_info": {
        "email": finalEmail, "type": 2}}
    action = "post"
    response = send_request(action, url, data)
    # printJSON(response)

# Delete user and transfer upcoming meetings, webinars and recordings to a new user
# oldEmail: user being deleted
# newEMail: New user that data is being transferred to


def deleteUser(oldEmail, newEmail):
    queryString = "%s?action=delete&transfer+email=%s&transfer_meeting=true&transfer_webinar=true&transfer_recording=true" % (
        oldEmail, newEmail)
    url = '/users/%s' % queryString
    data = {"action": "delete", "transfer_email": newEmail[2:],
            "transfer_meeting": True, "transfer_webinar": True, "transfer_recording": True}
    action = "delete"
    response = send_request(action, url, data)
    # printJSON(response)

# Check if the user had any additional addon licenses such as large meeting or webinar


def check_user_settings(oldEmail, newEmail):
    url = '/users/%s/settings' % oldEmail
    data = ''
    action = 'get'
    response = send_request(action, url, data)
    webinar = ''
    large_meeting = ''
    d = json.loads(response.text)
    return (d['feature'])

 #   if d['featuer']['webinar'] == True:
 #       webinar_capacity = d['feature']['webinar_capacity']
 #       data = {"feature": {"webinar": True,
 #                           "webinar_capacity": webinar_capacity}}
 #       update_user_settings(newEmail, data)
 #   if d['feature']['large_meeting'] == True:
 #       meeting_capacity = d['feature']['large_meeting_capacity']
 #       data = {"feature": {"large_meeting": True,
 #                           "meeting_capacity": meeting_capacity}}
 #       update_user_settings(newEmail, data)

# Updates the setting for a specific user
# body is returned from check_user_settings and specifically updates addon licenses


def update_user_settings(email, body):
    url = '/users/%s/settings' % email
    data = body
    action = 'post'
    response = send_request(action, url, data)

# Open CSV FIle containing user email addresses
# This function reads each email address from the csv file perform the API calls needed
# to migrate the user


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
        # apply addon licenses if required
            response = check_user_settings(userEmail, email)
            update_user_settings(email, response)


# run the script
migrateUser()
