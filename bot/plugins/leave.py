from bot import kreacher
from bot.instance.of_every_vc import VOICE_CHATS
from bot.helpers.queues import clear_queue
from telethon import events


@kreacher.on(events.NewMessage(pattern="[!?/]leave"))
async def leave_handler(event):
    try:
        chat = await event.get_chat()
        if VOICE_CHATS.get(chat.id) is None:
            raise Exception("Streaming is not active")
        await VOICE_CHATS[chat.id].leave_current_group_call()
        VOICE_CHATS.pop(chat.id)
        clear_queue(chat.id)
        await event.reply(
            "__Goodbye master, just call me if you need me. \n\nVoice Chat left successfully.__",
        )
    except Exception as e:
        return await event.reply(
            f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
        )
