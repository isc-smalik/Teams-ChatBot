from os import SEEK_END
from aiohttp.web_urldispatcher import Resource
from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
    CardFactory,
    MessageFactory,
)
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardImage,
    CardAction,
    ActionTypes,
    Attachment,
    MediaUrl,
)

from data_models import WelcomeUserState
import requests
import json
from datetime import datetime
from dateutil import tz

allergy_data = ""
#Time Zone converter
def zone_convertor(date_time):
    #Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # utc = datetime.utcnow()
    utc = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    # Tell the datetime object that it's in UTC time zone since 
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = str(utc.astimezone(to_zone))


    return central[0:16]


token = '78qai3V9z7ICJrmfF0mFZXziUkJq8t3XAVcVgjrivs-lBUqhPLUnJZO8it2Wuinbkpqi15zIUvt6O8WmUTWBVg'
call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}

url = "https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/137"
response = requests.get(url, headers = call_header, verify = True)
r_dict = json.loads(response.text)

lastUpdated = (f"{r_dict['meta']['lastUpdated']}")
utc = (f"{lastUpdated[0:10]} {lastUpdated[12:19]}")
trak_lastUpdated = zone_convertor(utc)

print (trak_lastUpdated)




                        
"""
print(response.status_code)

if response.status_code == 404:
    print ("work")
else:
    print("doesn't work")
"""
#check is a record number is valid
"""
record_number = "12345678"
record_number1 = "RN000012312"

if record_number1.startswith("RN"):
    print("its valid")

else:
    print("Not valid")
"""

#r_dict = json.loads(response.text)


"""
total = 5
list = ["a", "b", "c", "d", "e"]
list1 = ["1","2","3","4","5"]
string = ""
number =0

while number < total:
    string = string + (f"l {list[number]}\nl2 {list1[number]}\n\n")
    number = number + 1

print (string)
"""