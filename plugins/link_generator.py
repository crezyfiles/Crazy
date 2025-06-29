# (©) Codexbotz

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot import Bot
from config import ADMINS, WEBSITE_URL, PERMANENT, IS_SHORTLINK
from helper_func import encode, get_message_id
from .shortener import get_markup, get_shortlink


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nThis post is not valid from DB Channel.", quote=True)
            continue

    while True:
        try:
            second_message = await client.ask(
                text="Forward the Last Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nThis post is not valid from DB Channel.", quote=True)
            continue

    encoded = await encode(f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}")
    long_link = f"{WEBSITE_URL}?ref={encoded}" if PERMANENT else f"https://telegram.me/{client.username}?start={encoded}"
    short_link = await get_shortlink(long_link) if IS_SHORTLINK else None

    reply_markup = get_markup(short_link, long_link)
    text = (
        f"<b>🔗 Shortened Link:</b>\n{short_link}\n\n<b>🌐 Original Link:</b>\n{long_link}"
        if short_link else
        f"<b>Here is your link</b>\n\n{long_link}"
    )

    await second_message.reply_text(text, quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(
                text="Forward Message from the DB Channel (with Quotes)..\n\nor Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nThis post is not valid from DB Channel.", quote=True)
            continue

    encoded = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    long_link = f"{WEBSITE_URL}?ref={encoded}" if PERMANENT else f"https://telegram.me/{client.username}?start={encoded}"
    short_link = await get_shortlink(long_link) if IS_SHORTLINK else None

    reply_markup = get_markup(short_link, long_link)
    text = (
        f"<b>🔗 Shortened Link:</b>\n{short_link}\n\n<b>🌐 Original Link:</b>\n{long_link}"
        if short_link else
        f"<b>Here is your link</b>\n\n{long_link}"
    )

    await channel_message.reply_text(text, quote=True, reply_markup=reply_markup)
