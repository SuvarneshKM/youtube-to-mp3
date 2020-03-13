#!/usr/bin/env python

from pytube import YouTube
import os
from moviepy.editor import *

link = input("Enter The YouTube Link { with https } : ")
path1 = input("Enter The Download Path : ")
name = input("Enter The Name Of Music You Want To Given : ")

yt = YouTube(link)
print(yt.title + "\n") 
yt.streams.all()
stream = yt.streams.first()
path2 = stream.download(path1)
path3 = path1 + "/" +  name + ".mp3"

mp4_file = path2
mp3_file = path3

videoclip = VideoFileClip(mp4_file)
audioclip = videoclip.audio
audioclip.write_audiofile(mp3_file)
audioclip.close()
videoclip.close()

os.remove(path2)
