from pytube import YouTube
from sys import argv
from pytubemp3 import YouTube as mp3
import os

link = argv[1]
filter = argv[2]
yt = YouTube(link)
print("Title: ", yt.title)
print("Views: ", yt.views)
if filter == "video":
    yd = yt.streams.get_highest_resolution()
    yd.download(r"C:\Users\Thorwarth\Downloads\YT-Videos")
    print("Download video successful!")
elif filter == "audio":
    video = yt.streams.filter(only_audio=True).first()
    downloaded_file = video.download(r"C:\Users\Thorwarth\Downloads\YT-Videos")
    base, ext = os.path.splitext(downloaded_file)
    new_file = base + '.mp3'
    os.rename(downloaded_file, new_file)
    print("Download audio successful!")
