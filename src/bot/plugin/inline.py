import random

from generativepy.color import Color
from pyrogram import Client
from pyrogram.types import InlineQuery, InlineQueryResultPhoto
from generativepy.formulas import rasterise_formula


@Client.on_inline_query()
async def on_inline_query(_: Client, query: InlineQuery):
    output = rasterise_formula("latex", query.query, Color(0, 0, 0))
    print("Output:", output, flush=True)
    # output = pnglatex(query.query, output=f'/usr/src/app/images/{random_file_name}')

    # await query.answer(
    #     results=[
    #         InlineQueryResultPhoto(
    #             photo_url=f'https://api.fumaz.dev/latex/{random_file_name}',
    #             thumb_url=f'https://api.fumaz.dev/latex/{random_file_name}',
    #             title='Your LaTeX is ready!',
    #             description='Click to view your LaTeX image.',
    #             caption='🤖 Powered by @LaTeXifyBot'
    #         )
    #     ],
    #     cache_time=0,
    #     is_personal=True
    # )
