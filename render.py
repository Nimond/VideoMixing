import os
import sys
import subprocess
from moviepy.editor import *
from os import listdir
from threading import Thread


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
