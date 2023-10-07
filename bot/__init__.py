import os
import logging
from pyrogram import Client
from termcolor import colored
from bot.config import config
from pytgcalls import GroupCallFactory
from bot.utils.driver import get_driver

current_dir = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(current_dir, "logs")

if not os.path.exists(folder):
    os.makedirs(folder)
if os.path.exists(f"{folder}/logs.txt") and os.stat(f"{folder}/logs.txt").st_size > 0:
    with open(f"{folder}/logs.txt", "w") as f:
        f.truncate(0)
        print(f'{colored("[INFO]", "blue")}: LOG FILE WAS FLUSHED SUCCESSFULLY')
        f.close()
elif not os.path.exists(f"{folder}/logs.txt"):
    try:
        with open(f"{folder}/logs.txt", "w") as f:
            f.write("")
        print(f'{colored("[INFO]", "blue")}: LOG FILE CREATED')
    except Exception as e:
        logging.err(e)


logging.basicConfig(
    filename=f"{folder}/logs.txt",
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

BOT_USERNAME = config.BOT_USERNAME

assistant = Client(
    "kreacher.client",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING,
)
kreacher = Client(
    "kreacher.bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)
_factory = GroupCallFactory(assistant, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
on_call = _factory.get_group_call()
assistant.start()
kreacher.start()
driver = get_driver()
