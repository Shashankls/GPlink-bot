from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID',"16621664")
API_HASH = environ.get('API_HASH',"8b283f2943729318995738b5963f0bcc")
BOT_TOKEN = environ.get('BOT_TOKEN',"6818106042:AAHNMl3BzDewSO3ndKolTaoN-Cpt-POAKj4")
API_KEY = environ.get('API_KEY',"c8ce5ce72bbc4eeea88fa44ce14e06f6e53646b1")

bot = Client('sharedisk bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm GPlink bot. Just send me link and get short link")


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(f'Here is your [short link]({short_link})', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://sharedisk.in/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


bot.run()