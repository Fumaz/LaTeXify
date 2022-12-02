import random

from pnglatex import pnglatex
from pyrogram import Client
from pyrogram.types import InlineQuery, InlineQueryResultPhoto


@Client.on_inline_query()
async def on_inline_query(_: Client, query: InlineQuery):
    print(query.query, flush=True)

    random_file_name = str(random.randint(100000, 999999)) + ".png"
    output = pnglatex(query.query, output=f'/usr/src/app/images/{random_file_name}')

    await query.answer(
        results=[
            InlineQueryResultPhoto(
                photo_url=f'https://api.fumaz.dev/latex/{random_file_name}',
                thumb_url=f'https://api.fumaz.dev/latex/{random_file_name}',
                title='Your LaTeX is ready!',
                description='Click to view your LaTeX image.',
                caption='🤖 Powered by @LaTeXifyBot'
            )
        ],
        cache_time=0,
        is_personal=True
    )
