import re

flist = ['one.mp3','two.jpeg','3.txt']

while True:
    fileinp = int(input("Enter number of video clip you'd like to edit:   "))

    if re.match(r'^[0-9]+$',fileinp):
		try:
			file = flist[(fileinp-1)]
			break
	except IndexError:
		print('Error 404. Please try again.')

    else:
    	print('Error 404. Please try again.')