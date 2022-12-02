import os.path
from threading import Thread
from time import sleep

from flask import Flask, send_file

app = Flask('latex')


def remove(filename: str):
    sleep(15)
    os.remove(filename)


@app.route("/<filename>", methods=['GET'])
def image(filename: str):
    if not filename.endswith('.png') or '/' in filename:
        return 'Not found'

    Thread(target=remove, args=(filename,)).start()

    return send_file(filename)


def run():
    thread = Thread(target=lambda: app.run(host='0.0.0.0', debug=False))
    thread.start()
