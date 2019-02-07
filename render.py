import os
import sys
import subprocess
import requests
import datetime
from moviepy.editor import *
from threading import Thread
# -----
import cv2
import json
import numpy as np
#               ^
#testing OpenCV |


class ThreadedMix(Thread):
    def __init__(self, id, duration):
        super(ThreadedMix, self).__init__()
        self.id = id
        self.duration = duration

    def run(self):
        duration = self.duration
        id = self.id
        self.clips = []
        
        streamer = videoFileClip('streamer.mp4').subclip(0, duration)
        self.clips.append(streamer)
        game = videoFileClip('game' + id + '.mp4').subclip(0, duration)
        self.clips.append(game)

        video = CompositeVideoClip([game, streamer.resize(0.3).set_position(('right', 'top'), relative=True)])
        self.clips.append(video)
        video.write_Videofile('new' + str(id) + '.mp4')
        
        for clip in self.clips:
            clip.close()
        
        upload()
    
    def upload(self):
        subprocess.Popen([
                        'python2', 'upload.py', 
                        '--file=new' + self.id + '.mp4', 
                        '--title=' + self.id, 
                        '--description=' + self.id, 
                        '--keywords=1',
                        '--category=22',
                        '--privacyStatus=public'
                    ],
                        shell=True)
        print(str(self.id) + ' complited')


class ThreadedMixCV(Thread):
    def __init__(self, id, dir,stime,etime):
        super(ThreadedMixCV, self).__init__()
        self.id = str(id)
        self.dir = str(dir)
        self.etime = str(etime)
        self.stime = str(stime)
        print('its ok')
        clip = VideoFileClip('C:\\Python27\\directorconsole-flutter\\video\\'+str(self.dir) + '\\game' + self.id + '.mp4')
        print( clip.duration )
        self.duration = clip.duration
        clip.close()


    def run(self):
        duration = self.duration
        print('C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\game'+self.id+'.mp4')
        streamer = cv2.VideoCapture('C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\streamer.mp4')
        game = cv2.VideoCapture('C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\game' + self.id + '.mp4')
        #player = cv2.videoCapture('C:\\Python27\\directorconsole-flutter\\'+self.dir+'\\player' + self.id + '.mp4')

        fourcc = cv2.VideoWriter_fourcc(*'XVID') # 'M', 'P', 'E', 'G')
        out = cv2.VideoWriter('C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\output' + self.id + '.avi', fourcc, 30.0, (1280, 720))

        stime = str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute)
        print('sended')
        params = {
                          'place': 'Kremlin',
                          'point': self.id,
                          'stime': self.stime,
                          'etime': self.etime,
                          'date': '{}.{}.{}'.format(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year),
                          'url': 'null'
                          }                         
        requests.post('http://localhost:5000/add', json = json.dumps(params))

        total = int(game.get(cv2.CAP_PROP_FRAME_COUNT))
        while True:
            streamer_flag, streamer_frame = streamer.read()
            game_flag, game_frame = game.read()
            #player_flag, player_frame = player.read()

            current = int(game.get(cv2.CAP_PROP_POS_FRAMES))

            # os.system('clear')
            print(str(int(100*current/total))+'%')

            '''
            if int(100*current/total) // 25 == 0:
                params={
                       'id': self.id, 
                       'p': int(100*current/total)
                       }

                requests.get('http://localhost:5000/get', params=params)
            '''

            if not game_flag:
                for cap in [streamer, game, out]:
                    cap.release()

                print('writing audio ' + self.id)
                self.mix_audio_ffmpeg()
                print('uploading ' + self.id)
                url = self.upload()
                params = {
                          'place': 'Kremlin',
                          'point': self.id,
                          'stime': self.stime,
                          'etime': self.etime,
                          'date': '{}.{}.{}'.format(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year),
                          'url': url
                         }
                requests.get('http://127.0.0.1:5000/add_url', json = json.dumps(params)) 
                
                p1 = subprocess.Popen(['del', 'C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\game'+self.id+'.mp4'])
                
                # p2 = subprocess.Popen(['del', 'C:\\Python27\\directorconsole-flutter\\'+self.dir+'\\player'+self.id+'.mp4'])
                p3 = subprocess.Popen(['del', 'C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\output'+self.id+'.avi'])
                p4 = subprocess.Popen(['del', 'C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\new'+self.id+'.avi'])
                p1.wait()
                # p2.wait()
                p3.wait()
                p4.wait()
                
                if not 'streamer' in [temp.split('.')[0][:-1] for temp in os.listdir()]:
                    p = subprocess.Popen(['del', 'C:\\Python27\\directorconsole-flutter\\video\\'+self.dir])
                    p.wait()
                break
            try:
                #player_frame = cv2.resize(player_frame, None, fx=0.25, fy=0.25)
                streamer_frame = cv2.resize(streamer_frame, None, fx=0.25, fy=0.25)
            except Exception as e:
                print('error was excepted: {}'.foramt(e))
                
            #game_frame[0:player_frame.shape[0],0:player_frame.shape[1]] = player_frame
            game_frame[
                game_frame.shape[0]-streamer_frame.shape[0]:game_frame.shape[1],
                0:streamer_frame.shape[1]
                      ] = streamer_frame

            out.write(game_frame)
            # cv2.imshow('frame', game_frame)


    def mix_audio(self):
        streamer_audio = videoFileClip('C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\streamer.mp4').audio.subclip(0, self.duration)
        game_audio = videoFileClip('C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\game' + self.id + '.mp4').audio.subclip(0, self.duration)
        #player_audio = videoFileClip('C:\\Python27\\directorconsole-flutter\\'+self.dir+'\\player' + self.id + '.mp4').audio.subclip(0, self.duration)

        output = videoFileClip('C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\output' + self.id + '.avi')
        output_audio = CompositeAudioClip([streamer_audio, game_audio]) #, player_audio

        output.audio = output_audio
        output.write_videofile('C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\new' + self.id + '.avi', codec='mpeg4')


    def mix_audio_ffmpeg(self):
        # s = 'ffmpeg -i C:\\Python27\\directorconsole-flutter\\'+self.dir+'\\output4.avi -i C:\\Python27\\directorconsole-flutter\\'+self.dir+'\\player4.mp4 -i C:\\Python27\\directorconsole-flutter\\'+self.dir+'\\game4.mp4 -i C:\\Python27\\directorconsole-flutter\\'+self.dir+'\\streamer4.mp4 -filter_complex '[1:a][2:a][3:a]amerge=inputs=3[a]' -map 0:v -map '[a]' -c:v copy -c:a libvorbis -ac 2 -shortest C:\\Python27\\directorconsole-flutter\\'+self.dir+'\\new' + self.id + '.avi'
        # print(s)
        subprocess.call([
                        'ffmpeg',
                        '-i','C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\output'+self.id+'.avi',
                        #'-i','C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\player'+self.id+'.mp4',
                        '-i','C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\game'+self.id+'.mp4',
                        '-i','C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\streamer.mp4', 
                        '-filter_complex', '[1:a][2:a]amerge=inputs=2[a]', 
                        '-map','0:v',
                        '-map','[a]', 
                        '-c:v','copy',
                        '-c:a','libvorbis',
                        '-ac','2',
                        '-shortest','C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\new' + self.id + '.avi'
                        ])


    def upload(self):
        r = subprocess.run([
                        'C:\\Python27\\python.exe', 'upload.py', 
                        '--file=C:\\Python27\\directorconsole-flutter\\video\\'+self.dir+'\\new' + self.id + '.avi', 
                        '--title=' + self.id, 
                        '--description=' + self.id, 
                        '--keywords=1',
                        '--category=22',
                        '--privacyStatus=public'
                    ], stdout=subprocess.PIPE)
        print(r.stdout)
        
        print('https://www.youtube.com/watch?v=' + str(r.stdout).split('\\n')[-2][:-2])
        return 'https://www.youtube.com/watch?v=' + str(r.stdout).split('\\n')[-2][:-2]

        print(str(self.id) + ' complited')