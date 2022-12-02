import os
import os.path as op
import random
import shutil
import subprocess
import tempfile
from pathlib import Path

from IPython.lib.latextools import genelatex
from pnglatex import pnglatex
from pyrogram import Client
from pyrogram.types import InlineQuery, InlineQueryResultPhoto


def latex_to_image(latex, eps_path):
    eps_path = op.realpath(eps_path)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfile = os.path.join(tmpdir, "tmp.tex")
        dvifile = os.path.join(tmpdir, "tmp.dvi")
        psfile = os.path.join(tmpdir, "tmp.ps")
        pdffile = os.path.join(tmpdir, "tmp.pdf")
        epsfile = os.path.join(tmpdir, "tmp.eps")
        pngfile = os.path.join(tmpdir, "tmp.png")

        contents = list(genelatex(latex, False))
        with open(tmpfile, "w") as f:
            f.writelines(contents)

        with open(os.devnull, 'w') as devnull:
            try:
                subprocess.check_call(
                    ["latex", "-halt-on-error", tmpfile], cwd=tmpdir,
                    stdout=devnull, stderr=devnull)
            except Exception as e:
                print("************")
                print(len(contents))
                print('\n'.join(contents))
                raise (e)

            subprocess.check_call(
                ["dvips", dvifile, "-o", psfile], cwd=tmpdir,
                stdout=devnull, stderr=devnull)

            subprocess.check_call(
                ["gs",
                 "-o",
                 pdffile,
                 "-dNoOutputFonts",
                 "-sDEVICE=pdfwrite",
                 "-dEPSCrop",
                 psfile,
                 ], cwd=tmpdir,
                stdout=devnull, stderr=devnull)

            subprocess.check_call(
                ["pdf2ps", pdffile], cwd=tmpdir,
                stdout=devnull, stderr=devnull)

            subprocess.check_call(
                ["ps2eps", psfile], cwd=tmpdir,
                stdout=devnull, stderr=devnull)

            subprocess.check_call(
                ["dvipng", "-T", "tight", "-x", "6000", "-z", "9",
                 "-bg", "transparent", "-o", pngfile, dvifile], cwd=tmpdir,
                stdout=devnull, stderr=devnull)

        shutil.copy(epsfile, eps_path)
        shutil.copy(pngfile, Path(eps_path).with_suffix('.png'))


@Client.on_inline_query()
async def on_inline_query(_: Client, query: InlineQuery):
    print(query.query, flush=True)

    random_file_name = str(random.randint(100000, 999999)) + ".png"
    output = latex_to_image(query.query, f"/usr/src/app/images/{random_file_name}")
    # output = pnglatex(query.query, output=f'/usr/src/app/images/{random_file_name}')

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
