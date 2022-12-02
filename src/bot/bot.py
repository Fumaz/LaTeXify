from pyrogram import Client
from pyrogram.handlers import InlineQueryHandler

import config
from bot.plugin import inline

client = Client(
    name=config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    workers=config.BOT_WORKERS,
    plugins=dict(root='plugin')
)

client.add_handler(InlineQueryHandler(
    inline.on_inline_query,
))


def run():
    client.run()
