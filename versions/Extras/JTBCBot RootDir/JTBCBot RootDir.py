# Grabs videos from / outputs to this directory

import moviepy, os
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps
from datetime import datetime
import time

flist = []
rootDir = '.'
nth = 1
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        print('>> '+str(nth)+' - '+fname)
        flist.append(fname)
        nth += 1

while True:
    fileinp = int(input("Enter number of video clip you'd like to edit:   "))
    try:
        file = flist[(fileinp-1)]
        break
    except IndexError:
        print('Error 404. Please try again.')

print('>> File "'+file+'" chosen.')

start_time = time.time()

v = mp.VideoFileClip('./'+file)
final = v.duration-0.1 

song = './jjtbcroundabout.mp3'
riff_time = 44.944

start_song = final-riff_time
audioclip = mp.AudioFileClip(song)
audioclip = audioclip.set_start(t=start_song)  
fa = mp.CompositeAudioClip([audioclip, v.audio])

thumb = v.save_frame('./jjtbcthumbnail.jpg',t=final)
tg = Image.open('./jjtbcthumbnail.jpg').convert('L')
tinted = ImageOps.colorize(tg, black='#1e1a12', white='#bfb196')
tinted.save('./jjtbcthumbnail.jpg')
finalfr = mp.ImageClip('./jjtbcthumbnail.jpg', duration=(audioclip.duration-riff_time)).set_start(final)

bcarrow = mp.ImageClip('./jjtbcarrow.png').set_duration(10).resize(width=50).margin(left=10,bottom=10).set_pos(('left','bottom'))
tbcarrow = mp.ImageClip('./jjtbcarrow.png')
vidwid = v.w
print('>>>> Width = '+str(vidwid))

fv = mp.CompositeVideoClip([v, finalfr, tbcarrow.set_pos(('left','bottom')).set_start(final).set_duration(audioclip.duration-riff_time)])
fva = fv.set_audio(fa).set_end(fv.duration-0.1)
fva = fva.set_fps(fps=30)
fva.write_videofile('./jjtbcbotted_'+file)

now = datetime.now()
dt = now.strftime('%a %d/%m/%y %I:%M:%S %p')

lf = open('log.txt','a+')
lf.write('\n\n'+dt+'\n>> File: '+file+'\n>> Location: -'+'\n>> Video Length: '+str(fva.duration)+'\n>> Time Taken: '+str(time.time()-start_time))
lf.close()
