import moviepy
import moviepy.editor as mp
# import moviepy.video.fx.all as vfx
from moviepy.editor import *
import os, math
from PIL import Image, ImageOps

v = mp.VideoFileClip('test.mp4')
# arrow = mp.ImageClip('tbcarrow.png')
# arrow = arrow.resize(width=(v.w*0.4))

arrow = Image.open('tbcarrow.png').convert('RGBA')
arrow_size = int(math.floor(v.w*0.4)), int(math.floor(v.h*0.4))
arrow = arrow.resize(arrow_size)
# print(arrow_size)


arrow_frame = Image.new('RGBA', (v.w, v.h), (0,0,0,0)) # Blank image with dimensions of video
arrow_frame.save('./newarrow.png', 'PNG')

arrow_posx, arrow_posy = int(math.floor(v.w*0.1)), int(math.floor(v.h*0.5)) # Pastes arrow 10% across x axis, and 90% down y axis of video
area = (arrow_posx, arrow_posy, arrow_size[0]+arrow_posx, arrow_size[1]+arrow_posy)

print(area)
print(arrow_frame.size)


arrow_frame = arrow_frame.paste(arrow, area)
# Image.Image.paste(arrow_frame, arrow, arrow_pos)
arrow_frame.save('./arrow_frame.png', 'PNG')

arrow_frame = mp.ImageClip('arrow_frame.png')




slide = mp.CompositeVideoClip([arrow_frame.fx(mp.transfx.slide_in, 1, 'right').set_duration(v.duration)]) # Slides in from set position (width of image)
# https://github.com/Zulko/moviepy/blob/master/moviepy/video/compositing/transitions.py
# Clip needs to be same size as video


# slide = arrow.fx(vfx.scroll, x_speed=10, x_start=v.w).set_duration(v.duration)
# slide = moviepy.video.fx.all.scroll(arrow, h=200, w=300, x_speed=10, y_speed=20, x_start=30, y_start=40).set_duration(v.duration)


# slide = arrow.set_position(lambda t: (int(1000 * t), 100)).set_duration(v.duration)









fv = mp.CompositeVideoClip([v, slide])
fv.set_fps(fps=144)
path = './arrowtest.mp4'
fv.write_videofile(path)
os.startfile(os.path.realpath(path))