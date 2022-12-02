import random

from PIL import Image, ImageOps
from generativepy.color import Color
from generativepy.formulas import rasterise_formula
from pyrogram import Client
from pyrogram.types import InlineQuery, InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent


@Client.on_inline_query()
async def on_inline_query(_: Client, query: InlineQuery):
    try:
        random_file_name = str(random.randint(100000, 999999))
        output = rasterise_formula(f"/usr/src/app/{random_file_name}", query.query, Color(0, 0, 0), 1000,
                                   packages=['amsfonts', 'amsmath', 'amssymb', 'bm', 'cancel', 'color', 'esint'])

        image = Image.open(f"/usr/src/app/{random_file_name}.png")
        image = ImageOps.expand(image, border=50, fill="white")

        new_image = Image.new("RGBA", image.size, "WHITE")
        new_image.paste(image, (0, 0), image)
        new_image.convert("RGB").save(f"/usr/src/app/{random_file_name}.png", "PNG")

        await query.answer(
            results=[
                InlineQueryResultPhoto(
                    photo_url=f'https://api.fumaz.dev/latex/{random_file_name}.png',
                    thumb_url=f'https://api.fumaz.dev/latex/{random_file_name}.png',
                    title='Your LaTeX is ready!',
                    description='Click to view your LaTeX image.',
                )
            ],
            cache_time=0,
            is_personal=True
        )
    except:
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    title='An error has occurred!',
                    description="We couldn't generate your LaTeX.",
                    input_message_content=InputTextMessageContent(
                        message_text='An error has occurred!\nWe couldn\'t generate your LaTeX.'
                    )
                )
            ],
            cache_time=0,
            is_personal=True
        )
