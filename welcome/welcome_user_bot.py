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
    CardImage,
    CardAction,
    ActionTypes,
    Attachment,
    MediaUrl,
    ConversationReference,
    Activity,
    Mention
)

from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo
from botframework.connector import Channels
from data_models import WelcomeUserState
import requests
import json
from datetime import datetime
from dateutil import tz
from typing import List, Dict
import webbrowser

#Globals for patient data
trak_url = ''
trak_name = ''
trak_recordNumber = ''
trak_gender = ''
trak_dob = ''
trak_careProvider= ''
trak_allergy_url = ''
gname = ''
trak_lastUpdated = ''
allergy_data = ''
cp_list = ''
OAuth_url = ''
token = ''


class WelcomeUserBot(ActivityHandler):
    def __init__(self, conversation_references: Dict[str, ConversationReference], user_state: UserState, list_care_provider):
        self.conversation_references = conversation_references
        self.list_care_provider = list_care_provider
        if user_state is None:
            raise TypeError(
                "[WelcomeUserBot]: Missing parameter. user_state is required but None was given"
            )

        self._user_state = user_state

        self.user_state_accessor = self._user_state.create_property("WelcomeUserState")

        self.WELCOME_MESSAGE = "Hi I am InterSystems Bot"

        self.INFO_MESSAGE = "I am here to make your life easy"

        self.PATTERN_MESSAGE = "Not sure what you should do next ?   Try typing help or intro"

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        self._add_conversation_reference(turn_context.activity)
        return await super().on_conversation_update_activity(turn_context)
    
    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # save changes to WelcomeUserState after each turn
        await self._user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        """
        Greet when users are added to the conversation.
        Note that all channels do not send the conversation update activity.
        If you find that this bot works in the emulator, but does not in
        another channel the reason is most likely that the channel does not
        send this activity.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Hi { member.name }. " + self.WELCOME_MESSAGE
                )

                await turn_context.send_activity(self.PATTERN_MESSAGE)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to messages sent from the user.
        """
        

        self._add_conversation_reference(turn_context.activity)
        
        global trak_name
        global trak_allergy_url
        global trak_careProvider
        global trak_dob
        global trak_gender
        global trak_recordNumber
        global trak_url
        global gname
        global trak_lastUpdated
        global allergy_data
        global OAuth_url
        global token
        
        # Get the state properties from the turn context.
        welcome_user_state = await self.user_state_accessor.get(
            turn_context, WelcomeUserState
        )

        if not welcome_user_state.did_welcome_user:
            welcome_user_state.did_welcome_user = True
            
            # Will be on first message from user
            await turn_context.send_activity(
                "Welcome Back !"
            )

            name = turn_context.activity.from_property.name
            gname = name
            await turn_context.send_activity(
                f"What can I help you with {name} ?"
            )

        else:
            # removes mention from the user input in channels or group
            TurnContext.remove_recipient_mention(turn_context.activity)
            """            
            #Looking for any replies via cards
            channelData = turn_context.activity.channel_data
            if "postBack" in channelData:  
                # Credentials for OAuth2
                authorize_url = "https://tcfhirsandbox.intersystems.com.au/oauth2/authorize"
                token_url = "https://tcfhirsandbox.intersystems.com.au/oauth2/token"
                state = 'asdasdasdasdasdasasd'
                scope = 'patient%2F*.read%20launch%2Fpatient'
                callback_uri = "x-argonaut-app://HealthProviderLogin/"
                client_id = '6A605kYem9GmG38Vo6TTzh8IFnjWHZWtRn46K1hoxQY'
                client_secret = 'POrisHrcdMvUKmaR6Cea0b8jtx-z4ewVWrnaIXASO-H3tB3g5MgPV7Vqty7OP8aEbSGENWRMkeVuJJKZDdG7Pw'
                OAuth_url = authorize_url + '?response_type=code&state=' + state + '&client_id=' + client_id + '&scope='+scope+'&redirect_uri=' + callback_uri
                val = json.dumps(turn_context.activity.value)
                commandToken = json.loads(val)
                authorization_code = commandToken['SimpleVal']
                await turn_context.send_activity(f"your auth Code : {commandToken['SimpleVal']}")
                data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
                access_token_response = requests.post(token_url, data=data, verify=True, allow_redirects=True, auth=(client_id, client_secret))
                tokens = json.loads(access_token_response.text)
                access_token = tokens['access_token']
                token = access_token
                await turn_context.send_activity(f"your token : {token}")
                return None
            """
            
            # makes the text in lower case and strips of any spaces
            text = turn_context.activity.text.lower().strip()
            # splits the user input and makes a list
            ltxt = text.split(" ")

            
            # token needs to be entered manually.
            token = '78qai3V9z7ICJrmfF0mFZXziUkJq8t3XAVcVgjrivs-lBUqhPLUnJZO8it2Wuinbkpqi15zIUvt6O8WmUTWBVg'
            call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}

            # keywords that will be used by the bot to compare the user input
            if text in ("hello", "hi"):
                await turn_context.send_activity(f"why would you say {text} again ?")
            
            elif text in ("help", "intro"):
                await self.__send_intro_card(turn_context)
            
            elif text in ("login"):
                await self.__send_test_card(turn_context)                    
                                        
            elif text in ("patient"):
                await turn_context.send_activity('Please type the patient ID after patient. Eg: "patient 137"')
            
            elif ltxt[0] == "patient":
                if ltxt [1] != "0":
                    url = "https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/" + ltxt[1]
                    response = requests.get(url, headers = call_header, verify = True)
                        
                    if response.status_code == 404:
                        await turn_context.send_activity("Patient not found !")
                    elif response.status_code == 401 :
                        await turn_context.send_activity("Your token has expired !")
                    elif response.status_code == 200 :
                        r_dict = json.loads(response.text)
                    
                        trak_url = (f"https://tcfhirsandbox.intersystems.com.au/t2019grxx/csp/system.Home.cls#/Direct/AW.Direct.EPR?RegistrationNo={str(r_dict['identifier'][1]['value'])}")
                        
                        try:
                            pat_name = (f"{r_dict['name'][0]['text']}")
                            trak_name = pat_name.upper()
                        except:
                            trak_name = "Couldn't find NAME in database"
                        try:
                            lastUpdated = (f"{r_dict['meta']['lastUpdated']}")
                            utc = (f"{lastUpdated[0:10]} {lastUpdated[12:19]}")
                            trak_lastUpdated = zone_convertor(utc)
                        except:
                            trak_lastUpdated = "No DATE found"
                        try:
                            trak_careProvider = (f"{r_dict['careProvider'][0]['display']}")
                        except:
                            trak_careProvider = "Couldn't find CARE PROVIDER in database"
                        try:
                            trak_recordNumber = (f"{r_dict['identifier'][1]['value']}")
                        except:
                            trak_recordNumber = "Couldn't find RECORD NUMBER in database"
                        try:
                            trak_dob = (f"{r_dict['birthDate']}")
                        except:
                            trak_dob = "Couldn't find DOB in database"
                        try:
                            trak_gender = (f"{r_dict['gender']}")
                        except:
                            trak_gender = "GENDER is not disclosed by the patient"

                        trak_allergy_url = (f"https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/{ltxt[1]}/AllergyIntolerance")
                                
                        allergy_resposne = requests.get(trak_allergy_url, headers = call_header, verify = True) 
                        a_dict = json.loads(allergy_resposne.text)
                        a_total = (f"{a_dict['total']}")
                                
                        if a_total != "0":
                            count = int(a_total)
                            index = count - 1
                            allergy_name = ""
                            allergy_reaction = ""
                            allergy_severity = ""
                            allergy_recordedDate = ""
                                    
                            while count != 0:
                                try:
                                    allergy_name = allergy_name + (f"{a_dict['entry'][index]['resource']['substance']['text']}:")
                                except:
                                    allergy_name = "Unknown"
                                try:    
                                    allergy_reaction = allergy_reaction + (f"{a_dict['entry'][index]['resource']['reaction'][0]['manifestation'][0]['text']}:") # it is possible that there are more sublist under reaction and manifestation
                                except:
                                    allergy_reaction = "No record found"
                                try:
                                    allergy_severity = allergy_severity = allergy_severity + (f"{a_dict['entry'][index]['resource']['reaction'][0]['severity']}:")
                                except:
                                    allergy_severity = "No record found"
                                try:
                                    utc_date = (f"{a_dict['entry'][index]['resource']['recordedDate']}|")
                                    dt = utc_date.split("T")
                                    t = dt[1].split("+")
                                    dt_format =  (f"{dt[0]} {t[0]}")
                                    allergy_recordedDate = allergy_recordedDate + zone_convertor(dt_format) + "|"
                                except:
                                    allergy_recordedDate = "Date Unknown"
                                
                                index = index - 1
                                count = count - 1

                            list_name = allergy_name.split(":")
                            list_reaction = allergy_reaction.split(":")
                            list_severity = allergy_severity.split(":")
                            list_date = allergy_recordedDate.split("|")

                            allergy_data = ""
                            total_allergy = int(a_total)
                                
                            list_index = 0
                            while list_index < total_allergy:
                                allergy_data = allergy_data + (f"Allergen : {list_name[list_index]}\n\nReaction : {list_reaction[list_index]}\n\nSeverity : {list_severity[list_index]}\n\nRecorded Date : {list_date[list_index]}\n\n-------------------------------------\n\n")
                                list_index+=1
                        else:
                            allergy_data = (f"{trak_name} have no recorded allergies")
                        
                        await self.__send_about_card(turn_context)

            elif ltxt[0] == "mrn":
                url = "https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient?identifier=" + ltxt[1]
                response = requests.get(url, headers = call_header, verify = True)
                if response.status_code == 404:
                    await turn_context.send_activity("3rd Patient not found !")
                elif response.status_code == 401 :
                    await turn_context.send_activity("Your token has expired !")
                elif response.status_code == 200 :
                    r_dict = json.loads(response.text)
                    trak_url = (f"https://tcfhirsandbox.intersystems.com.au/t2019grxx/csp/system.Home.cls#/Direct/AW.Direct.EPR?RegistrationNo={ltxt[1]}")
                    
                    try:
                        pat_name = (f"{r_dict['entry'][0]['resource']['name'][0]['text']}")
                        trak_name = pat_name.upper()
                    except:
                        trak_name = "Couldn't find NAME in database"
                    try:
                        lastUpdated = (f"{r_dict['entry'][0]['resource']['meta']['lastUpdated']}")
                        utc = (f"{lastUpdated[0:10]} {lastUpdated[12:19]}")
                        trak_lastUpdated = zone_convertor(utc)
                    except:
                        trak_lastUpdated = "No DATE found"
                    try:
                        trak_careProvider = (f"{r_dict['entry'][0]['resource']['careProvider'][0]['display']}")
                    except:
                        trak_careProvider = "Couldn't find CARE PROVIDER in database"
                    try:
                        trak_recordNumber = (f"{r_dict['entry'][0]['resource']['identifier'][1]['value']}")
                    except:
                        trak_recordNumber = "Couldn't find RECORD NUMBER in database"
                    try:
                        trak_dob = (f"{r_dict['entry'][0]['resource']['birthDate']}")
                    except:
                        trak_dob = "Couldn't find DOB in database"
                    try:
                        trak_gender = (f"{r_dict['entry'][0]['resource']['gender']}")
                    except:
                        trak_gender = "GENDER is not disclosed by the patient"

                    trak_allergy_url = (f"https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/{r_dict['entry'][0]['resource']['id']}/AllergyIntolerance")        
            
                    allergy_resposne = requests.get(trak_allergy_url, headers = call_header, verify = True) 
                    a_dict = json.loads(allergy_resposne.text)
                    a_total = (f"{a_dict['total']}")
                            
                    if a_total != "0":
                        count = int(a_total)
                        index = count - 1
                        allergy_name = ""
                        allergy_reaction = ""
                        allergy_severity = ""
                        allergy_recordedDate = ""
                                
                        while count != 0:
                            try:
                                allergy_name = allergy_name + (f"{a_dict['entry'][index]['resource']['substance']['text']}:")
                            except:
                                allergy_name = "Unknown"
                            try:    
                                allergy_reaction = allergy_reaction + (f"{a_dict['entry'][index]['resource']['reaction'][0]['manifestation'][0]['text']}:") # it is possible that there are more sublist under reaction and manifestation
                            except:
                                allergy_reaction = "No record found"
                            try:
                                allergy_severity = allergy_severity + (f"{a_dict['entry'][index]['resource']['reaction'][0]['severity']}:")
                            except:
                                allergy_severity = "No record found"
                            try:
                                utc_date = (f"{a_dict['entry'][index]['resource']['recordedDate']}|")
                                date_t = utc_date.split("T")
                                t = date_t[1].split("+")
                                dt_format =  (f"{date_t[0]} {t[0]}")
                                allergy_recordedDate = allergy_recordedDate + zone_convertor(dt_format) + "|"
                            except:
                                allergy_recordedDate = "Date Unknown"
                            
                            index = index - 1
                            count = count - 1

                        list_name = allergy_name.split(":")
                        list_reaction = allergy_reaction.split(":")
                        list_severity = allergy_severity.split(":")
                        list_date = allergy_recordedDate.split("|")

                        allergy_data = ""
                        total_allergy = int(a_total)
                            
                        list_index = 0
                        while list_index < total_allergy:
                            allergy_data = allergy_data + (f"Allergen : {list_name[list_index]}\n\nReaction : {list_reaction[list_index]}\n\nSeverity : {list_severity[list_index]}\n\nRecorded Date : {list_date[list_index]}\n\n-------------------------------------\n\n")
                            list_index+=1
                    else:
                        allergy_data = (f"{trak_name} have no recorded allergies")
                        
                    await self.__send_about_card(turn_context)

            #list all providers
            elif text in ("notification", "noti"):
                global cp_list
                cp_list = ""
                for provider in self.list_care_provider:
                    cp_list = cp_list + (f"{provider['id']} - {provider['name']} \n\n")
                await self.__send_result_card(turn_context)
            #mention provider in the teams
            elif text in ("mention", "mention care providers"):
                if turn_context.activity.channel_id == Channels.ms_teams:
                    try:
                        members = await TeamsInfo.get_team_members(turn_context)
                        for provider in self.list_care_provider:
                            for member in members:
                                if member.name == provider['name']:
                                    mention = Mention(
                                    mentioned=member,
                                    text=f"<at>{member.name}</at>",
                                    type="mention",
                                    )
                                    reply_activity = MessageFactory.text(f"{mention.text}")
                                    reply_activity.entities = [Mention().deserialize(mention.serialize())]
                                    await turn_context.send_activity(reply_activity)
                        self.list_care_provider.clear()
                        
                    except:
                        await turn_context.send_activity("This function is only supported in teams/channels!")
                else:
                    await turn_context.send_activity("This function is only supported in Microsoft Teams")
            else:
                await turn_context.send_activity("I am SORRY!, I don't understand that.")



    
    async def __send_about_card(self, turn_context:TurnContext):
        ADAPTIVE_CARD_CONTENT = {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "size": "Medium",
                    "weight": "Bolder",
                    "text": "About Patient",
                    "wrap": True
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "items": [
                                {
                                    "type": "Image",
                                    "style": "Person",
                                    "url": "https://icon-library.com/images/blank-person-icon/blank-person-icon-27.jpg",
                                    "size": "Small"
                                }
                            ],
                            "width": "auto"
                        },
                        {
                            "type": "Column",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "weight": "Bolder",
                                    "text": (f"{trak_name}"),
                                    "wrap": True
                                },
                                {
                                    "type": "TextBlock",
                                    "spacing": "None",
                                    "text": (f"Last Updated : {trak_lastUpdated}"),
                                    "isSubtle": True,
                                    "wrap": True
                                }
                            ],
                            "width": "stretch"
                        }
                    ]
                },
                {
                    "type": "FactSet",
                    "facts": [
                        {
                            "title": "Record Number",
                            "value": (f"{trak_recordNumber}")
                        },
                        {
                            "title": "DOB",
                            "value": (f"{trak_dob}")
                        },
                        {
                            "title": "Sex",
                            "value": (f"{trak_gender}")
                        },
                        {
                            "title": "Care Provider",
                            "value": (f"{trak_careProvider}")
                        }
                    ],
                    "separator": True
                }
            ],
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "title": "Go to trakcare",
                    "url": (f"{trak_url}")
                },
                {
                    "type": "Action.ShowCard",
                    "title": "Show Allergies",
                    "card": 
                    {
                        "type": "AdaptiveCard",
                        "body": [
                            {
                                "type": "TextBlock",
                                "size": "Medium",
                                "weight": "Bolder",
                                "text": (f"Following data is available for {trak_name} : "),
                                "wrap": True
                            },
                            {
                                "type": "TextBlock",
                                "text": (f"{allergy_data}"),
                                "wrap": True
                            }
                        ],
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.0"
                    }
                },
                {
                    "type": "Action.ShowCard",
                    "title": "Observations",
                    "card": {
                        "type": "AdaptiveCard"
                    }
                }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0"
        }

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT))
        )

    async def __send_intro_card(self, turn_context:TurnContext):
        ADAPTIVE_CARD_CONTENT = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "body": [
                {
                    "speak": "Tom's Pie is a Pizza restaurant which is rated 9.3 by customers.",
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "Intersystems Bot",
                                    "weight": "Bolder",
                                    "size": "ExtraLarge",
                                    "spacing": "None",
                                    "wrap": True
                                },
                                {
                                    "type": "TextBlock",
                                    "text": (f"Hi {gname}, I am InterSystems bot."),
                                    "size": "Medium",
                                    "wrap": True,
                                    "maxLines": 3
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Write \"Patient\" followed by patient ID or \"mrn\" followed by Medical Record Number to get details about patient",
                                    "wrap": True,
                                    "size": "Medium"
                                }
                            ],
                            "style": "default"
                        },
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "Image",
                                    "url": "https://media-exp1.licdn.com/dms/image/C560BAQG6u8nOkqxK2w/company-logo_200_200/0?e=2159024400&v=beta&t=7DvyiaL7v0xYIzQtl0kDZCjGs_e-MA7h5xC5Rg5xtaI",
                                    "horizontalAlignment": "Center",
                                    "spacing": "Small"
                                }
                            ]
                        }
                    ]
                }
            ],
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "title": "More Info",
                    "url": "https://usconfluence.iscinternal.com/display/AU101/TEAMS%3A+Technical+Discovery"
                }
            ]
        }

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT))
        )

    async def __send_MDT_card(self, turn_context:TurnContext):
        ADAPTIVE_CARD_CONTENT = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "speak": "<s>Your  Multidisciplinary Team Meeting<break strength='weak'/> is starting at ${formatDateTime(start.dateTime, 'HH:mm')}pm</s><s>Do you want to snooze <break strength='weak'/> or do you want to send a late notification to the attendees?</s>",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Multidisciplinary Team Meeting",
                    "size": "Large",
                    "weight": "Bolder",
                    "wrap": True
                },
                {
                    "type": "TextBlock",
                    "text": "Location : Microsoft Teams",
                    "isSubtle": True,
                    "wrap": True
                },
                {
                    "type": "Input.Time",
                    "id": "T",
                    "label": "Time",
                    "value": "14:00",
                    "min": "07:00",
                    "max": "16:00",
                    "spacing": "Small",
                    "separator": True
                },
                {
                    "type": "TextBlock",
                    "text": "Choose users to add to meeting",
                    "wrap": True,
                    "size": "Medium"
                },
                {
                    "type": "Input.ChoiceSet",
                    "choices": [
                        {
                            "title": "Michael",
                            "value": "None"
                        },
                        {
                            "title": "Quinten",
                            "value": "None"
                        },
                        {
                            "title": "Harshitha",
                            "value": "None"
                        },
                        {
                            "title": "Jolyon",
                            "value": "None"
                        },
                        {
                            "title": "Sergei",
                            "value": "None"
                        }
                    ],
                    "placeholder": "Placeholder text",
                    "isMultiSelect": True,
                    "$data": "Users"
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Create Meeting"
                }
            ],
            "id": "Create Meating",
            "fallbackText": "a"
        }

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT))
        )

    async def __send_result_card(self, turn_context:TurnContext):
        ADAPTIVE_CARD_CONTENT = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.2",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Result from TrakCare",
                    "size": "Large",
                    "weight": "Bolder",
                    "wrap": True
                },
                {
                    "type": "TextBlock",
                    "text": "Click the button below to view the result in TrakCare",
                    "wrap": True
                },
                {
                    "type": "ActionSet",
                    "actions": [
                        {
                            "type": "Action.Submit",
                            "title": "View Result"
                        }
                    ]
                },
                {
                    "type": "TextBlock",
                    "text": "List of Care Providers",
                    "wrap": True,
                    #"horizontalAlignment": "Center",
                    "size": "Medium",
                    "weight": "Bolder",
                    "separator": True
                },
                {
                    "type": "TextBlock",
                    #"horizontalAlignment": "Center",
                    "text": (f"{cp_list}"),
                    "wrap": True,
                    "separator": True
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Mention Care Providers",
                    "data": {
                        "msteams" : {

                                "type":"imBack",
                                "value":"Mention Care Providers"
                        }

                    }
                }
            ],
            "id": "Mention Care Providers",
            "fallbackText": "Mention Care Providers"
        }

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT))
        )
        
    async def __send_oauth_card(self, turn_context:TurnContext):
        ADAPTIVE_CARD_CONTENT = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "body": [
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": 2,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "FHIR Login Wizard",
                                    "weight": "Bolder",
                                    "size": "Medium",
                                    "wrap": True
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Click the button below to open a login window",
                                    "isSubtle": True,
                                    "wrap": True
                                },
                                {
                                    "type": "Container",
                                    "items": [
                                        {
                                            "type": "ActionSet",
                                            "actions": [
                                                {
                                                    "type": "Action.OpenUrl",
                                                    "title": "Login",
                                                    "url":(f"{OAuth_url}")
                                                }
                                            ]
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Enter the Authorization code below and press submit",
                                            "wrap": True
                                        },
                                        {
                                            "type": "Input.Text",
                                            "id": "Auth Code",
                                            "placeholder": "Enter Authorization Code Here"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Submit Authorization Code",
                    "data": {
                        "msteams": {
                            "type":"messageBack",
                            "text":"This goes to the bot",
                            "value":"{\"bfKey\": \"bfVal\", \"conflictKey\": \"from value\"}"
                        }
                    }
                }
            ]
        }
        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT))
        )
    async def __send_test_card(self, turn_context:TurnContext):
        ADAPTIVE_CARD_CONTENT = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "body": [
                {
                    "type": "TextBlock",
                    "size": "Medium",
                    "weight": "Bolder",
                    "text": "EnterAuth code",
                    "horizontalAlignment": "Center",
                    "wrap": True
                },
                {
                    "type": "TextBlock",
                    "text": (f"{OAuth_url}"),
                    "wrap": True
                },
                {
                    "type": "Input.Text",
                    "style": "text",
                    "id": "SimpleVal"
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Click me for messageBack",
                    "data": {
                        "msteams": {
                            "type": "messageBack",
                            "text": "text to bots",
                            "value": "{\"bfKey\": \"bfVal\", \"conflictKey\": \"from value\"}"
                        }
                    }
                }
            ]
        }
        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT))
        )

    def _add_conversation_reference(self, activity: Activity):
            """
            This populates the shared Dictionary that holds conversation references. In this sample,
            this dictionary is used to send a message to members when /api/notify is hit.
            :param activity:
            :return:
            """
            conversation_reference = TurnContext.get_conversation_reference(activity)
            self.conversation_references[
                conversation_reference.user.id
            ] = conversation_reference


#Time Zone converter
def zone_convertor(date_time):
    #Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    # Tell the datetime object that it's in UTC time zone since 
    utc = utc.replace(tzinfo=from_zone)
    # Convert time zone
    central = str(utc.astimezone(to_zone))
    return central[0:16]

