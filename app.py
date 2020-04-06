#!/usr/bin/env python

# importing the modules
from pytube import YouTube
import os
from moviepy.editor import *
import eyed3
import requests
from huepy import *


# a path to store the downloaded music files
path1 = input(run("Enter Download Path or press . to download in current directory : "))

# open txt file with links, remove newlines and download each link
print("Reading link in list.txt...")
with open('list.txt') as f:
    alist = [line.rstrip() for line in f]
    for line in alist:
        print(line)

        #--------- Downloading video from YT to extract audio later--------
        yt_link = line
        yt = YouTube(yt_link)
        # setting the artist field to the first word in the video title
        # or else cover art won't show up on some android phones
        artist_name = yt.title.partition(' ')[0]
        song_name = yt.title
        # terminal output to confirm download has started
        print("Starting download for... " + song_name)
        print("Artist field set to: " + artist_name)
        img_id = yt.thumbnail_url

        yt.streams.all()
        # see available video formats
        # and get the first stream option
        stream = yt.streams.first()
        # downloading video to a new path which will get deleted later
        path2 = stream.download(path1)
        mp4_file = path2
        # creating a path for mp3 file
        path3 = path1 + "/" +  song_name + ".mp3"
        mp3_file = path3

        # conversion from mp4 to mp3
        print("Extracting audio from the video clip...")
        videoclip = VideoFileClip(mp4_file) # creating a videoclip object
        audioclip = videoclip.audio # get the audio object from mp4 file
        print("Writing audio file...")
        audioclip.write_audiofile(mp3_file) # save the audio of mp4 into the specified mp3 file
        audioclip.close()
        videoclip.close()
        # deleting the mp4 file
        os.remove(path2)

        #--------- DOWNLOADING YOUTUBE THUMBNAIL IMAGE -----------------

        # message confirming that the img download process has started
        print('Importing youtube thumbnail...')

        url = img_id
        r = requests.get(url)

        # assigning a path for the temporary image file
        # (it's going to get deleted after embed onto mp3 has finished)
        path4 = path1 + "/img" + ".jpg"

        with open(path4, 'wb') as f:
            f.write(r.content)

        print("Thumbnail image downloaded!")

        # # retrieving HTTP meta-data
        # print(r.status_code)
        # print(r.headers['content-type'])
        # print(r.encoding)

        #--------- EMBEDDING THUMBNAIL IMG ONTO MP3 FILE -----------------

        audiofile = eyed3.load(mp3_file)
        if (audiofile.tag == None):
            audiofile.initTag()

        audiofile.tag.images.set(3, open(path4,'rb').read(), 'image/jpeg')
        # embedding artist name onto mp3 file
        audiofile.tag.album_artist = artist_name
        audiofile.tag.save()

        # deleting the thumbnail as it's not needed anymore
        os.remove(path4)
        print(good(green(song_name + " created :) -----------------------------------\n")))
