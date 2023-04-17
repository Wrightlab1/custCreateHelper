# CustCreate user Migration

>  ==**Warning!**==

> ==Running this script will **delete** users on your account.==

This script is intended to help ISV partners migrate non custCreate users to the custCreate user type. IT does this in the following way.
- Reads a list of email addresses from a csv file
- A new email address will be created by base64 encoding the original email address and a configurable domain will be added
- A new custCreate user will be created with the new email address
- The original user is deleted and their meetings, webinars, and recordings are transferred to the new user

## Installation

```

git clone https://github.com/Wrightlab1/custCreateHelper.git

```

 ## Authentication
 This script uses Zoom [Server to Server Authentication](https://developers.zoom.us/docs/internal-apps/s2s-oauth/)
 A new Server to Server App should be created to run this script.
 ### scopes
 Be sure to add the necessary scopes
 - ```user.write.admin```

## Usage

- Create a ```.env``` Use the sample env as a guide

- Create a csv file containing the email addresses you would like migrated

- Run the script

  

## Logging

A logfile is generated for you in ``` ./logs/log.log```

This logfile will contain all of the information you need to debug your Zoom REST API requests