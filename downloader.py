from pytube import YouTube
from sys import argv
from pytubemp3 import YouTube as mp3
import os
from pydub import AudioSegment
import pdb

link = argv[1]
filter = argv[2]
yt = YouTube(link)
print("Title: ", yt.title)
print("Views: ", yt.views)

#pdb.set_trace()
if filter == ("video" or "mp4"):
    yd = yt.streams.get_highest_resolution()
    yd.download(r"C:\Users\Thorwarth\Downloads\YT-Videos")
    print("Download video successful!")
elif filter == ("audio" or "mp3"):
    video = yt.streams.filter(only_audio=True).first()
    downloaded_file = video.download(r"C:\Users\Thorwarth\Downloads\YT-Videos")

    base, ext = os.path.splitext(downloaded_file)
    new_file = base + '.mp3'
    audio = AudioSegment.from_file(downloaded_file)
    audio.export(new_file, format="mp3")
    #os.rename(downloaded_file, new_file)
    os.remove(downloaded_file)
    print("Download audio successful!")
