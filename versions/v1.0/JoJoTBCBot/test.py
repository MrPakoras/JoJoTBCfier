import moviepy.editor as mpe
import numpy as np

clip = mpe.VideoFileClip('sample.mp4')
x = 1
logo = (mpe.ImageClip('tbcarrow.png').set_pos((x,0.9), relative=True))

while x != 0.05:
    x -= 0.05
    x = round(x,2)
    print('>> '+str(x))
    logo = logo.set_pos((x,0.9), relative=True)


audio_bg = mpe.AudioFileClip('./songs/roundabout_short.mp3').set_start(t=10)


final_audio = mpe.CompositeAudioClip([audio_bg, clip.audio])
final_clip = mpe.CompositeVideoClip([clip, logo.set_start(10).set_duration(5)])
fca = final_clip.set_audio(final_audio)
fca.write_videofile('editedsample.mp4')
