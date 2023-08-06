from asyncio import sleep
from kreacher import kreacher
from kreacher.dicts.dicts import QUEUE, VOICE_CHATS
from telethon import events, Button
from kreacher.helpers.queues_handler import next_item, skip_current
thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"


@kreacher.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(event):
    await event.delete()


@kreacher.on(events.callbackquery.CallbackQuery(data="pause_or_resume_callback"))
async def _(event):
    chat = await event.get_chat()
    if VOICE_CHATS[chat.id].is_video_paused:
        await VOICE_CHATS[chat.id].set_pause(True)
        await kreacher.edit_message(event.sender_id, event.message_id,
            "\U00002378 <i>Started Video Streaming!</i>",
            file=thumb,
            buttons=[
                [Button.inline("\U000023ee ʙᴀᴄᴋ", data="back_callback"),
                 Button.inline("\U00002378 ᴘᴀᴜsᴇ", data="pause_or_resume_callback"),
                 Button.inline("\U000023ED ɴᴇxᴛ", data="next_callback")
                 ],
                [Button.inline("cʟᴏꜱᴇ", data="cls")],
            ],
            parse_mode="HTML")
        return await sleep(3)
    await VOICE_CHATS[chat.id].set_pause(True)
    await kreacher.edit_message(event.sender_id, event.message_id,
        "\U00002378 <i>Started Video Streaming!</i>",
        file=thumb,
        buttons=[
            [Button.inline("\U000023ee ʙᴀᴄᴋ", data="back_callback"),
             Button.inline("\U0001F501 ʀᴇsᴜᴍᴇ", data="pause_or_resume_callback"),
             Button.inline("\U000023ED ɴᴇxᴛ", data="next_callback")
             ],
            [Button.inline("cʟᴏꜱᴇ", data="cls")],
        ],
        parse_mode="HTML")
    return await sleep(3)


@kreacher.on(events.callbackquery.CallbackQuery(data="back_callback"))
async def _(event):
    chat = await event.get_chat()
    await VOICE_CHATS[chat.id].set_pause(False)


@kreacher.on(events.callbackquery.CallbackQuery(data="next_callback"))
async def _(event):
    chat = await event.get_chat()
    if len(event.text.split()) < 2:
        op = await skip_current(chat)
        if op == 0:
            await event.reply("**Nothing Is Streaming**")
        elif op == 1:
            await event.reply("empty queue, leaving voice chat")
        else:
            await event.reply(
                f"**⏭ Skipped**\n**🎧 Now Playing** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
            return await sleep(3)
    else:
        skip = event.text.split(maxsplit=1)[1]
        DELQUE = "**Removing Following Songs From Queue:**"
        if chat.id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await next_item(chat, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await event.reply(DELQUE)
            return await sleep(3)


@kreacher.on(events.callbackquery.CallbackQuery(data="end_callback"))
async def _(event):
    chat = await event.get_chat()
    QUEUE.pop(chat.id)
    await VOICE_CHATS[chat.id].stop_media()
    await VOICE_CHATS[chat.id].stop()
    VOICE_CHATS.pop(chat.id)
    return await sleep(3)