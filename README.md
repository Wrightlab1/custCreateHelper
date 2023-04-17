# CustCreate user Migration

>  ==**Warning!**==

> ==Running this script will **delete** users on your account.==

  

## Installation

```

git clone https://github.com/Wrightlab1/custCreateHelper.git

```

 ## Authentication
 This script uses Zoom [Server to Server Authentication](https://developers.zoom.us/docs/internal-apps/s2s-oauth/)
 

## Usage

- Create a ```.env``` Use the sample env as a guide

- Create a csv file containing the email addresses you would like migrated

- Run the script

  

## Logging

A logfile is generated for you in ``` ./logs/log.log```

This logfile will contain all of the information you need to debug your Zoom REST API requests