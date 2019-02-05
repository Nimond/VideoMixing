from flask import Flask, request, json
import subprocess
import os
import datetime
from models import User, session, Base, engine, Place
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import json
import random
from flask import jsonify
from render import ThreadedMixCV

app = Flask(__name__)

@app.route('/render')
def render():
    if 'game{}.mp4'.format(request.args.get('id')) in os.listdir(r'C:\Python27\directorconsole-flutter\video'):
        thread = ThreadedMixCV(request.args.get('id'))
        thread.start()
        
        return "OKEY"
    else:
        return "cant get id"

@app.route('/rend')
def rend():
    if request.args.get('id'):
        if 'stream' + request.args.get('id') + '.webm' in os.listdir(r'C:\Python27\directorconsole-flutter\video'):
            subprocess.Popen(["ffmpeg.exe","-i","video\\streamer.webm","video\\streamer.mp4"])
            subprocess.Popen(["ffmpeg.exe", "-i","video\\stream"+request.args.get('id')+".webm", "video\\game"+request.args.get('id')+".mp4"])
            print('starting')
            render = ThreadedMixCV(request.args.get('id'))
            render.start()

            return "ok"
        else:
            print(os.listdir(r'C:\Python27\directorconsole-flutter\video'), request.args.get('id'))
            return "file not found"
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


@app.route('/init', methods=['GET'])
def init1_db(*args, **kwargs):
    Base.metadata.create_all(engine)
    return 'okes'

@app.route('/list', methods=['GET'])
def list():
    s = ''
    for name in session.query(User):
        s +=str(name.point)+" "+str(name.id) +' '+ str(name.place) + ' '+ str(name.date) +' '+str(name.start_time)+' '+str(name.end_time)+' '+ str(name.url)+'<br>'
    return s

@app.route('/listJSON', methods=['GET'])
def listJSON():
    n = session.query(User).first()
    print(n)

    l = {}
    array = []
    try:
        l2 = {}
        last = n.start_time + '-'+n.end_time
        print('\n\n\n'+last+'\n\n\n')
        array = []
        time = []
        i = 1
        for name in session.query(User):
            if str(name.start_time)+'-'+str(name.end_time)==last:
                time.append({'point':str(name.point),'place':str(name.place),'date':str(name.date),'url':str(name.url)})
            else:
                l2['time'] = last
                l2['content']=time
                time = []
                array.append(l2)
                l2 = {}
                time.append({'point':str(name.point),'place':str(name.place),'date':str(name.date),'url':str(name.url)})
                if session.query(User).count() == i:
                    l2['time'] = str(name.start_time)+'-'+str(name.end_time)
                    l2['content']=time
                    time = []
                    array.append(l2)
            last = str(name.start_time)+'-'+str(name.end_time)
            i+=1
        l['data'] = array
    except AttributeError:
        l['data'] = array
    return jsonify(l)

@app.route('/getText', methods=['GET'])
def textJSON():
    f= open('text.json','r',encoding='utf8')
    temp = f.read()
    print(temp)
    r = eval(temp)
    l = {
    'localStartPageText':r['localStartPageText'],
    'remoteStartPageText': r['remoteStartPageText'],
    'connectionSuccessText': r['connectionSuccessText'],
    'connectionInProgressText': r['connectionInProgressText'],
    'myQrCodeText': r['myQrCodeText']
    }
    return jsonify(l)

@app.route('/setID', methods=['GET'])
def setID():
    request.args.get('place')
    for i in range(0,9):
        session.add(Place(request.args.get('place'),random.randint(100000,999999)))
    session.commit()
    return 'ok'

@app.route('/getID', methods=['GET'])
def getID():
    l = []
    for name in session.query(Place).filter(Place.place==request.args.get('place')):
        l.append(name.point)
    return str(l[int(request.args.get('point'))])

@app.route('/add', methods=['GET','POST'])
def insert():
    r = json.loads(request.json)
    logging.error(request.json)
    logging.error('/n/n/n')
    session.add(User(r['place'],int(r['point']),r['date'],r['stime'],r['etime'],r['url']))
    session.commit()
    logging.error('ok')
    return 'ok'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', threaded=True)
