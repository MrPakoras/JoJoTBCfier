import subprocess


n = 1

def exportingtext():
	global n
	e = ['>> Please wait.', '>> Please wait..', '>> Please wait...']
	if n%3 == 0:
		# print(f'>> {n} mod 3 = {n%3}')
		print(e[2])
		n = 1
	if n%2 == 0:
		# print(f'>> {n} mod 2 = {n%2}')
		print(e[1])
	else:
		# print(f'>> {n}')
		print(e[0])
	n += 1


# while True:
# 	exportingtext()


