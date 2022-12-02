from pyrogram import Client

import config

client = Client(
    name=config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    workers=config.BOT_WORKERS,
    plugins=dict(root='bot/plugin')
)