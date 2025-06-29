import string
import random
from shortzy import Shortzy
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SHORTLINK_URL, SHORTLINK_API


def get_markup(short_link: str = None, long_link: str = None):
    buttons = []
    if short_link:
        buttons.append(InlineKeyboardButton("🔗 Short Link", url=short_link))
    if long_link:
        buttons.append(InlineKeyboardButton("🌐 Original Link", url=long_link))
    return InlineKeyboardMarkup([buttons]) if buttons else None
    
    
def generate_random_string(length=8) -> str:
  
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def get_shortlink(long_url: str, website: str = SHORTLINK_URL, api_key: str = SHORTLINK_API ) -> str:
  
    try:
        shortzy = Shortzy(api_key, website)
        alias = generate_random_string()
        short_url = await shortzy.convert(long_url, alias=alias)
        return short_url
    except Exception as e:
        print(e)
        try:
            return await shortzy.get_quick_link(long_url)
        except Exception as e:
            return long_url
