from flask import Flask, request, json
import subprocess
import os


app = Flask(__name__)


'''
:5000/render?id={1,2,3...}
trying to find:
game{id}.webm
streamer{id}.webm
'''
@app.route('/render')
def render():
	if request.args.get('id'):
		if 'game' + request.args.get('id') + '.webm' in os.listdir(r'C:\Python27'):
			subprocess.Popen(["python", "main.py", "-t", "10", "-f", request.args.get('id')], close_fds=True)
			
			return "ok"
		else:
			return "file not found"
	else:
		return "cant get id"

if __name__ == '__main__':
	app.run(host = '0.0.0.0', threaded=True)
