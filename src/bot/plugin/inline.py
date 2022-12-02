import random
import subprocess

from PIL import Image, ImageOps
from generativepy.color import Color
from generativepy.formulas import rasterise_formula, tex2, _crop, _remove_ignore_errors
from pyrogram import Client, raw
from pyrogram.types import InlineQuery, InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultCachedPhoto

tex1 = '\n'.join([r'\documentclass[preview]{standalone}'
                  r'\usepackage{amsfonts,amsmath,amssymb,dsfont,mathtools}',
                  r'\begin{document}',
                  r'\begin{equation*}'])


def rasterize_formula(name, formula, color, dpi):
    unique_name = "{}-{}".format(name, random.randint(100000, 999999))
    tex = '\n'.join([tex1, formula, tex2])
    tex_fn = '{}.tex'.format(unique_name)
    with open(tex_fn, 'w') as tex_file:
        tex_file.write(tex)
    process = subprocess.Popen('latex {}.tex'.format(unique_name), shell=True,
                               stdout=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen('dvipng -T tight -D {} {}.dvi'.format(dpi, unique_name), shell=True,
                               stdout=subprocess.PIPE)
    process.wait()

    filename, size = _crop(unique_name, name, color)

    _remove_ignore_errors("{}.aux".format(unique_name))
    _remove_ignore_errors("{}.log".format(unique_name))
    _remove_ignore_errors("{}.tex".format(unique_name))
    _remove_ignore_errors("{}.dvi".format(unique_name))
    _remove_ignore_errors("{}1.png".format(unique_name))

    return filename, size


@Client.on_inline_query()
async def on_inline_query(_: Client, query: InlineQuery):
    try:
        random_file_name = str(random.randint(100000, 999999))
        output = rasterize_formula(f"/usr/src/app/{random_file_name}", query.query, Color(0, 0, 0), 1000)

        image = Image.open(f"/usr/src/app/{random_file_name}.png")
        image = ImageOps.expand(image, border=50, fill="white")

        new_image = Image.new("RGBA", image.size, "WHITE")
        new_image.paste(image, (0, 0), image)
        new_image.convert("RGB").save(f"/usr/src/app/{random_file_name}.png", "PNG")

        file = await _.save_file(f"/usr/src/app/{random_file_name}.png")
        media = raw.types.InputMediaUploadedPhoto(
            file=file,
            ttl_seconds=None
        )

        await query.answer(
            results=[
                InlineQueryResultCachedPhoto(
                    photo_file_id=str(media.file.id),
                    title='Your LaTeX is ready!',
                    description='Click to view your LaTeX image.',
                )
                # InlineQueryResultPhoto(
                #     photo_url=f'https://api.fumaz.dev/latex/{random_file_name}.png',
                #     thumb_url=f'https://api.fumaz.dev/latex/{random_file_name}.png',
                #     title='Your LaTeX is ready!',
                #     description='Click to view your LaTeX image.',
                # )
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
