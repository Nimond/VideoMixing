import os
import sys
import subprocess
from moviepy.editor import *
from os import listdir


def mix(video_time, id):
	streamer = VideoFileClip('streamer' + id + '.webm').subclip(0, video_time)
	game = VideoFileClip('game' + id + '.webm').subclip(0, video_time)
	player = VideoFileClip('player' + id + '.webm').subclip(0, video_time)
	streamer.set_pos((0.2, 0.2, 'left', 'top'))
	
	video = CompositeVideoClip([game, streamer.resize(0.3).set_position(('right', 'top'), relative=True), player.resize(0.3).set_position(('left', 'top'), relative=True)])
	video.write_videofile('new' + str(video_time) + '.mp4')
	video.close()
	streamer.close()
	player.close()
	game.close()



if sys.argv:
	print(sys.argv)
	mix(int(sys.argv[2]), sys.argv[4])
	print("cd C:\Python27", "&&", "python.exe", "upload.py", 
														"--file=" + r"C:\Users\Melkor\Desktop\streamervideo" + r"\new10.mp4", 
														"--title=" + sys.argv[4], 
														"--description=" + sys.argv[4], 
														"--keywords='1'",
														"--category=22",
														"--privacyStatus=public")
														
	subprocess.Popen(["python2", "upload.py", 
														"--file=new10.mp4", 
														"--title=" + sys.argv[4], 
														"--description=" + sys.argv[4], 
														"--keywords='1'",
														"--category=22",
														"--privacyStatus=public"],
														shell=True)
	print("complete")
	
	
	
