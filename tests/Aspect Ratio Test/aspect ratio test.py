## ~ v1.3 - Fixing aspect ratio issues ~ ##

# Bot that edits video and adds To Be Continued to it

import moviepy, os
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps
from datetime import datetime
import time, re, ffmpeg
from converter import Converter


## Choosing file to edit

file = 'cupdash.MOV'

start_time = time.time() # Timing Program

## Editing video

# ~ Using Converter to convert to .mp4 ~

'''
ffmpegvid = ffmpeg.input('./videos/'+file)
ffmpegout = ffmpeg.output(ffmpegvid, file)
'''

conv = Converter()
info = conv.probe('./videos/'+file)

# ~ v1.2 edit - Converting to .mp4 ~
extindex = file.rfind('.') # finding final . for extension
filemp3 = str(file[0:extindex])+'.mp4' # replacing extension with .mp4

convert = conv.convert('./videos/'+file, './videos/'+filemp3, {'format':'mp4'})

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')



# ~ Video clip ~
v = mp.VideoFileClip('./videos/'+filemp3)
final = v.duration-0.1 # Removes 0.1s from end of clip so that freeze frame doesnt loop to 1st frame

# ~ v1.3 edit - Aspect Ratio ~
def aspect():
    vidwid = v.w
    vidhei = v.h
    print('\n\n>> WidthxHeight = '+str(vidwid)+'x'+str(vidhei))

aspect()
quit()
