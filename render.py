import os
import sys
import subprocess
from moviepy.editor import *
from threading import Thread
# -----
import cv2
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
        
        streamer = VideoFileClip('streamer' + id + '.mp4').subclip(0, duration)
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

        clip = VideoFileClip("game" + self.id + ".mp4")
        print( clip.duration )
        self.duration = clip.duration
        clip.close()


    def run(self):
        duration = self.duration

        streamer = cv2.VideoCapture("./streamer" + self.id + ".mp4")
        game = cv2.VideoCapture('./game' + self.id + '.mp4')
        player = cv2.VideoCapture('./player' + self.id + '.mp4')

        fourcc = cv2.VideoWriter_fourcc(*'XVID') # 'M', 'P', 'E', 'G')
        out = cv2.VideoWriter('output' + self.id + '.avi', fourcc, 30.0, (1280, 720))

        while True:
            streamer_flag, streamer_frame = streamer.read()
            game_flag, game_frame = game.read()
            player_flag, player_frame = player.read()


            if not game_flag:
                for cap in [streamer, player, game, out]:
                    cap.release()

                print('writing audio ' + self.id)
                self.mix_audio_ffmpeg()
                print('uploading ' + self.id)
                self.upload()
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
        streamer_audio = VideoFileClip("streamer" + self.id + ".mp4").audio.subclip(0, self.duration)
        game_audio = VideoFileClip("game" + self.id + ".mp4").audio.subclip(0, self.duration)
        player_audio = VideoFileClip("player" + self.id + ".mp4").audio.subclip(0, self.duration)

        output = VideoFileClip("output" + self.id + ".avi")
        output_audio = CompositeAudioClip([streamer_audio, game_audio, player_audio])

        output.audio = output_audio
        output.write_videofile("new" + self.id + ".avi", codec='mpeg4')


    def mix_audio_ffmpeg(self):
        s = 'ffmpeg -i output4.avi -i player4.mp4 -i game4.mp4 -i streamer4.mp4 -filter_complex "[1:a][2:a][3:a]amerge=inputs=3[a]" -map 0:v -map "[a]" -c:v copy -c:a libvorbis -ac 2 -shortest new' + self.id + '.avi'
        print(s)
        print(type(s))
        subprocess.run([s], shell=True, check=True)
        '''
                        'ffmpeg',
                        '-i','output4.avi',
                        '-i','player4.mp4',
                        '-i','game4.mp4',
                        '-i','streamer4.mp4', 
                        '-filter_complex','\"[1:a][2:a][3:a]amerge=inputs=3[a]\"',
                        '-map','0:v',
                        '-map','\"[a]\"',
                        '-c:v','copy',
                        '-c:','libvorbis',
                        '-ac','2',
                        '-shortest','new' + self.id + '.avi'
                        ])
        '''


    def upload(self):
        r = subprocess.run([
                        "python2", "upload.py", 
                        "--file=new" + self.id + ".avi", 
                        "--title=" + self.id, 
                        "--description=" + self.id, 
                        "--keywords=1",
                        "--category=22",
                        "--privacyStatus=public"
                    ], stdout=subprocess.PIPE)
        print(r.stdout)
        print('\n\n')
        print('https://www.youtube.com/watch?v=' + str(r.stdout)[2:-1].split('\\n')[-2])

        print(str(self.id) + ' complited')
