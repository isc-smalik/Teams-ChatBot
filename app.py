#Author: Yuanhao(Michael) Zheng - Email: likeping13@gmail.com  LinkedIn: https://www.linkedin.com/in/yuanhao-zheng-ba38001b0/
#        Sachin Malik           - Email: Sachin.Malik@intersystems.com
#
#This file is the main file of our chat bot.User will need to run it to run the bot
#it contains serveral http endpoints including the message endpoint, the mdt creation notification endpoint and the result forwarding endpoint
#
import sys
import traceback
from datetime import datetime
from http import HTTPStatus
from typing import Dict

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter, turn_context,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes, ConversationReference

from botbuilder.core import MemoryStorage, UserState
from bot import WelcomeUserBot
from config import DefaultConfig

"""import asyncio
from botdialog import BotDialog #dialog"""

CONFIG = DefaultConfig()

"""CONMEMORY = ConversationState(MemoryStorage()) #dialog
botdialog = BotDialog(CONMEMORY) #dialog"""

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

# Create a shared dictionary.  The Bot will add conversation references when users join the conversation and send messages.
CONVERSATION_REFERENCES: Dict[str, ConversationReference] = dict()

#CareProviders list
lsCP = list()
dicRs = dict()

# Create MemoryStorage, UserState
MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)

# Create the Bot
BOT = WelcomeUserBot(CONVERSATION_REFERENCES,USER_STATE, lsCP, dicRs)


# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    """async def call_fun(turn_context):
        await botdialog.on_turn(turn_context)"""

    try:
        response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        if response:
            return json_response(data=response.body, status=response.status)
        return Response(status=201)
    except Exception as exception:
        raise exception

#Listen for incoming requests on /api/post_notify
async def post_notify(req: Request) -> Response:
    body = await req.json()
    for item in body:
        name = item["name"]
        id = item["id"]
        lsCP.append({"name":name,"id":id})   
    await _send_post_body()
    return Response(status=HTTPStatus.OK, text="Message has been sent")

async def _send_post_body():
    for conversation_reference in CONVERSATION_REFERENCES.values():
        await ADAPTER.continue_conversation(
            conversation_reference,
            lambda turn_context: turn_context.send_activity("You have a new MDT meeting creation, send 'mdt' to view the providers! You can send 'delete' to clear the care provider list"),
            CONFIG.APP_ID
        )
# Listen for auth code
async def auth_code(req: Request) -> Response:
    data = await req.text()
    await _send_auth_data()
    return Response(status=HTTPStatus.OK, text="Login Successful !")

async def _send_auth_data():
    for conversation_reference in CONVERSATION_REFERENCES.values():
        await ADAPTER.continue_conversation(
            conversation_reference,
            lambda turn_context: turn_context.send_activity("you got something"),
            CONFIG.APP_ID
        )

#Listen for incoming requests on /api/results
async def post_results(req: Request) -> Response:
    body = await req.json()
    name = body['name']
    urn = body['urn']
    link = body['link']
    sender = body['sendersName']
    message = body['message']
    BOT.dict_results = {"name":name, "urn":urn, "link":link, "sender" : sender, "message": message}
    await _send_result_body()
    return Response(status=HTTPStatus.OK, text="Result has been sent")

async def _send_result_body():
    for conversation_reference in CONVERSATION_REFERENCES.values():
        await ADAPTER.continue_conversation(
            conversation_reference,
            lambda turn_context: turn_context.send_activity("You have some results"),
            CONFIG.APP_ID
        )

APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)
APP.router.add_post("/api/post_notify", post_notify)
APP.router.add_post("/api/auth_code", auth_code)
APP.router.add_post("/api/results", post_results)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
