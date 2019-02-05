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
        
        streamer = VideoFileClip('streamer.mp4').subclip(0, duration)
        self.clips.append(streamer)
        game = VideoFileClip('game' + id + '.mp4').subclip(0, duration)
        self.clips.append(game)

        video = CompositeVideoClip([game, streamer.resize(0.3).set_position(('right', 'top'), relative=True)])
        self.clips.append(video)
        video.write_videofile('new' + str(id) + '.mp4')
        
        for clip in self.clips:
            clip.close()
        
        upload()
    
    def upload(self):
        subprocess.Popen([
                        "python2", "upload.py", 
                        "--file=new" + self.id + ".mp4", 
                        "--title=" + self.id, 
                        "--description=" + self.id, 
                        "--keywords=1",
                        "--category=22",
                        "--privacyStatus=public"
                    ],
                        shell=True)
        print(str(self.id) + " complited")


class ThreadedMixCV(Thread):
    def __init__(self, id):
        super(ThreadedMixCV, self).__init__()
        self.id = str(id)
        print('its ok')
        clip = VideoFileClip(r"C:\Python27\directorconsole-flutter\video\game" + self.id + ".mp4")
        print( clip.duration )
        self.duration = clip.duration
        clip.close()


    def run(self):
        duration = self.duration

        streamer = cv2.VideoCapture(r"C:\Python27\directorconsole-flutter\video\streamer.mp4")
        game = cv2.VideoCapture(r"C:\Python27\directorconsole-flutter\video\game" + self.id + '.mp4')
        player = cv2.VideoCapture(r"C:\Python27\directorconsole-flutter\video\player" + self.id + '.mp4')

        fourcc = cv2.VideoWriter_fourcc(*'XVID') # 'M', 'P', 'E', 'G')
        out = cv2.VideoWriter(r'C:\Python27\directorconsole-flutter\video\output' + self.id + '.avi', fourcc, 30.0, (1280, 720))

        stime = str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute)
        print('sended')
        params = {
                          'place': 'Kremlin',
                          'point': self.id,
                          'stime': stime,
                          'etime': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                          'date': '{}.{}.{}'.format(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year),
                          'url': 'null'
                          }                         
        requests.post('http://localhost:5000/add', json = json.dumps(params))

        total = int(game.get(cv2.CAP_PROP_FRAME_COUNT))
        while True:
            streamer_flag, streamer_frame = streamer.read()
            game_flag, game_frame = game.read()
            player_flag, player_frame = player.read()

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
                for cap in [streamer, player, game, out]:
                    cap.release()

                print('writing audio ' + self.id)
                self.mix_audio_ffmpeg()
                print('uploading ' + self.id)
                url = self.upload()
                params = {
                          'place': 'Kremlin',
                          'point': self.id,
                          'stime': stime,
                          'etime': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                          'date': '{}.{}.{}'.format(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year),
                          'url': url
                         }
                requests.get('http://127.0.0.1:5000/add', json = json.dumps(params))
                # TODO: delete video files
                break
            
            player_frame = cv2.resize(player_frame, None, fx=0.25, fy=0.25)
            streamer_frame = cv2.resize(streamer_frame, None, fx=0.25, fy=0.25)
            
            game_frame[0:player_frame.shape[0],0:player_frame.shape[1]] = player_frame
            game_frame[
                game_frame.shape[0]-streamer_frame.shape[0]:game_frame.shape[1],
                0:streamer_frame.shape[1]
                      ] = streamer_frame

            out.write(game_frame)
            # cv2.imshow('frame', game_frame)


    def mix_audio(self):
        streamer_audio = VideoFileClip(r"C:\Python27\directorconsole-flutter\video\streamer.mp4").audio.subclip(0, self.duration)
        game_audio = VideoFileClip(r"C:\Python27\directorconsole-flutter\video\game" + self.id + ".mp4").audio.subclip(0, self.duration)
        player_audio = VideoFileClip(r"C:\Python27\directorconsole-flutter\video\player" + self.id + ".mp4").audio.subclip(0, self.duration)

        output = VideoFileClip(r"C:\Python27\directorconsole-flutter\video\output" + self.id + ".avi")
        output_audio = CompositeAudioClip([streamer_audio, game_audio, player_audio])

        output.audio = output_audio
        output.write_videofile(r"C:\Python27\directorconsole-flutter\video\new" + self.id + ".avi", codec='mpeg4')


    def mix_audio_ffmpeg(self):
        # s = 'ffmpeg -i C:\\Python27\\directorconsole-flutter\\video\\output4.avi -i C:\\Python27\\directorconsole-flutter\\video\\player4.mp4 -i C:\\Python27\\directorconsole-flutter\\video\\game4.mp4 -i C:\\Python27\\directorconsole-flutter\\video\\streamer4.mp4 -filter_complex "[1:a][2:a][3:a]amerge=inputs=3[a]" -map 0:v -map "[a]" -c:v copy -c:a libvorbis -ac 2 -shortest C:\\Python27\\directorconsole-flutter\\video\\new' + self.id + '.avi'
        # print(s)
        subprocess.call([
                        'ffmpeg',
                        '-i','C:\\Python27\\directorconsole-flutter\\video\\output'+self.id+'.avi',
                        '-i','C:\\Python27\\directorconsole-flutter\\video\\player'+self.id+'.mp4',
                        '-i','C:\\Python27\\directorconsole-flutter\\video\\game'+self.id+'.mp4',
                        '-i','C:\\Python27\\directorconsole-flutter\\video\\streamer.mp4', 
                        '-filter_complex', '[1:a][2:a][3:a]amerge=inputs=3[a]', 
                        '-map','0:v',
                        '-map','[a]', 
                        '-c:v','copy',
                        '-c:a','libvorbis',
                        '-ac','2',
                        '-shortest','C:\\Python27\\directorconsole-flutter\\video\\new' + self.id + '.avi'
                        ])


    def upload(self):
        r = subprocess.run([
                        "C:\\Python27\\python.exe", "upload.py", 
                        "--file=C:\\Python27\\directorconsole-flutter\\video\\new" + self.id + ".avi", 
                        "--title=" + self.id, 
                        "--description=" + self.id, 
                        "--keywords=1",
                        "--category=22",
                        "--privacyStatus=public"
                    ], stdout=subprocess.PIPE)
        print(r.stdout)
        
        print('https://www.youtube.com/watch?v=' + str(r.stdout).split('\\n')[-2][:-2])
        return 'https://www.youtube.com/watch?v=' + str(r.stdout).split('\\n')[-2][:-2]

        print(str(self.id) + ' complited')