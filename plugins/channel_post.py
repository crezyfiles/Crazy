# (©) Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from bot import Bot
from config import (
    ADMINS,
    CHANNEL_ID,
    DISABLE_CHANNEL_BUTTON,
    WEBSITE_URL,
    PERMANENT,
    IS_SHORTLINK
)
from helper_func import encode
from .shortener import get_markup, get_shortlink


@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'users', 'broadcast', 'batch', 'genlink', 'stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)

    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went wrong..!")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    base64_string = await encode(f"get-{converted_id}")

    long_link = f"{WEBSITE_URL}?ref={base64_string}" if PERMANENT else f"https://telegram.me/{client.username}?start={base64_string}"
    short_link = await get_shortlink(long_link) if IS_SHORTLINK else None

    reply_markup = get_markup(short_link, long_link)
    text = (
        f"<b>🔗 Shortened Link:</b>\n{short_link}\n\n<b>🌐 Original Link:</b>\n{long_link}"
        if short_link else
        f"<b>Here is your link</b>\n\n{long_link}"
    )

    await reply_text.edit(text, reply_markup=reply_markup, disable_web_page_preview=True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)


@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    base64_string = await encode(f"get-{converted_id}")

    long_link = f"{WEBSITE_URL}?ref={base64_string}" if PERMANENT else f"https://telegram.me/{client.username}?start={base64_string}"
    short_link = await get_shortlink(long_link) if IS_SHORTLINK else None

    reply_markup = get_markup(short_link, long_link)

    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
