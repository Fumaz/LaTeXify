import random

from generativepy.color import Color
from pyrogram import Client
from pyrogram.types import InlineQuery, InlineQueryResultPhoto
from generativepy.formulas import rasterise_formula


@Client.on_inline_query()
async def on_inline_query(_: Client, query: InlineQuery):
    random_file_name = str(random.randint(100000, 999999))
    output = rasterise_formula(random_file_name, query.query, Color(0, 0, 0))

    await query.answer(
        results=[
            InlineQueryResultPhoto(
                photo_url=f'https://api.fumaz.dev/latex/{random_file_name}.png',
                thumb_url=f'https://api.fumaz.dev/latex/{random_file_name}.png',
                title='Your LaTeX is ready!',
                description='Click to view your LaTeX image.',
                caption='🤖 Powered by @LaTeXifyBot'
            )
        ],
        cache_time=0,
        is_personal=True
    )
