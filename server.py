from flask import Flask, request, json
from render import ThreadedMix
import os


app = Flask(__name__)


@app.route('/render')
def render():
    if request.args.get('id'):
        thread = ThreadedMix(request.args.get('id'), 10)
        thread.start()
        return "OKEY"
    else:
        return "cant get id"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', threaded=True)
