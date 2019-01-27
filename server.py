from flask import Flask, request, json
from render import ThreadedMixCV
import os


app = Flask(__name__)


@app.route('/render')
def render():
    if request.args.get('id'):
        thread = ThreadedMixCV(request.args.get('id'))
        thread.start()
        return "OKEY"
    else:
        return "cant get id"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', threaded=True)
