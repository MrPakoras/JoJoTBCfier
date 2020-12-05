import re

a = 'T:/his is/an example/of a random/file.txt'

print(a)
print(re.findall(r'.+(\/.+)$',a)[0][1:])