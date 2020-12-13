import moviepy.editor as mp
import moviepy.video.fx.all as vfx

v = mp.VideoFileClip('A:/Users/Anas/Videos/Class Videos/Big 3 Groovin.mp4')
arrow = mp.ImageClip('tbcarrow.png')
arrow = arrow.resize(width=(v.w*0.4))

# def slide(clip):
# 	clip.set_pos(('right','bottom'))
# 	x = clip.pos()
# 	print(x)
# 	while clip.pos()[0] != 'right':
# 		x -= 1
# 		clip.set_pos((x,'bottom'))
# 		return clip




# fv = mp.CompositeVideoClip([v, arrow.set_pos(('left','bottom')).set_duration(v.duration)])
# fv = mp.CompositeVideoClip([v, arrow.set_position(lambda t: (500-t*1000,'bottom')).set_duration(v.duration)])
# fv = mp.CompositeVideoClip([v, slide(arrow).set_duration(v.duration)])

slided_clips = mp.CompositeVideoClip([arrow.fx(mp.transfx.slide_in, v.duration, 'right').set_duration(v.duration)])
fv = mp.CompositeVideoClip([v, slided_clips])




fv.set_fps(fps=144)

fv.write_videofile('./arrowtest.mp4')