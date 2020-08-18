import os, re

addr = input('Enter file address:   ')

reg = re.match(r'(/|\\).*?\.[\w:]+',addr)
print(reg)

#fname = (reg.pop()).join('')
#path = reg[-1]

#print('>> fname: '+fname)
#print('>> path: '+path)

'''
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result'''


