import os
import uuid
import logging
from asyncio import sleep
from bot.config import config
from pyrogram.types import Message
from difflib import SequenceMatcher
from pyrogram import filters, Client
from pyrogram.enums import MessagesFilter
from bot.helpers.progress import progress
from bot.scrapers.images import ImageScraper
from bot import assistant, kreacher, tgcalls, VOICE_CHATS
from bot.decorators.only_grps_chnns import only_grps_chnns
from bot.helpers.queues import (
    remove_queue,
)

_cwd = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]streaming"))
@only_grps_chnns
async def _(client: Client, message: Message):
    results = []
    try:
        if " " not in message.text:
            return await message.reply(
                "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**"
            )
        msg = await message.reply("**__Searching...__**")
        await sleep(2)
        search = message.text.split(maxsplit=1)[1]
        movie_name = os.path.join(
            _cwd, f"../../downloads/movies/{str(uuid.uuid4())}.mp4"
        )
        serie_name = os.path.join(
            _cwd, f"../../downloads/series/{str(uuid.uuid4())}.mp4"
        )
        tmp = os.path.join(_cwd, "../../tmp")
        series_channel = await assistant.get_chat(config.ES_SERIES_CHANNEL)
        movies_channel = await assistant.get_chat(config.ES_MOVIES_CHANNEL)
        async for serie in assistant.search_messages(
            chat_id=series_channel.id,
            query=search,
            limit=1000,
            filter=MessagesFilter.VIDEO,
        ):
            results.append(
                {
                    "type": "serie",
                    "caption": serie.caption,
                    "file_id": serie.video.file_id,
                }
            )
        async for movie in assistant.search_messages(
            chat_id=movies_channel.id,
            query=search,
            limit=1000,
            filter=MessagesFilter.VIDEO,
        ):
            results.append(
                {
                    "type": "movie",
                    "caption": movie.caption,
                    "file_id": movie.video.file_id,
                }
            )
        for media in results:
            similary = SequenceMatcher(None, search, media["caption"]).ratio()
            if similary >= 0.3:
                await msg.edit(
                    f"**__Yeehaw, I found the {media['type']} you asked for...__**"
                )
                await sleep(2)
                await msg.edit("💾 **__Downloading...__**")
                image_scraper = ImageScraper(
                    tmp, search_key=f"{media['caption']} poster"
                )
                image_urls = image_scraper.find_image_urls()
                photo = image_scraper.save_images(image_urls, keep_filenames=True)
                if media["type"] == "serie":
                    video = await assistant.download_media(
                        media["file_id"],
                        file_name=serie_name,
                        progress=progress,
                        progress_args=(client, message.chat, msg),
                    )
                if media["type"] == "movie":
                    video = await assistant.download_media(
                        media["file_id"],
                        file_name=movie_name,
                        progress=progress,
                        progress_args=(client, message.chat, msg),
                    )
                if VOICE_CHATS.get(message.chat.id) is None:
                    await msg.edit("🪄 **__Joining the voice chat...__**")
                    await tgcalls.start(message.chat.id)
                    VOICE_CHATS[message.chat.id] = tgcalls
                await sleep(2)
                await VOICE_CHATS[message.chat.id].start_video(
                    video,
                    enable_experimental_lip_sync=True,
                    repeat=False,
                    with_audio=True,
                )
                await msg.delete()
                await client.send_photo(
                    message.chat.id,
                    photo=photo,
                    caption=f"**__Streaming {media['type'].upper()}__**",
                )
                await msg.pin()
                break

            await msg.edit(
                "**__The request has not been found in our database, please try another name__**"
            )
            break
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            await remove_queue(str(message.chat.id))
            VOICE_CHATS.pop(message.chat.id)
