from flask import Flask, request, json
from render import ThreadedMixCV
import os


app = Flask(__name__)
videos = {}


@app.route('/render')
def render():
        thread = ThreadedMixCV(request.args.get('id'))
        thread.start()
        
        return "OKEY"
    else:
        return "cant get id"


@app.route('/get')
def get():
	video = request.args.get('id')
	
	if video.get(video) == 100:
		del video[video]
		return str(100)
	else:
		return str(video.get(video))


@app.route('/set')
def set():
	video = request.args.get('id')
	complete = request.args.get('p')

	videos[video] = complete	


if __name__ == '__main__':
    app.run(host = '0.0.0.0', threaded=True, port=5454)

