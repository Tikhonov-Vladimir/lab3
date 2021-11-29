import struct
import random
_in = open('unlearne.bdf', 'r')

charnum = 0
dict = {}

while True:
    l = _in.readline().split(' ')
    if l[0] == 'CHARS':
        charnum = int(l[1])
        break

for i in range(charnum):
    l = _in.readline().split(' ')
    if l[0] == 'STARTCHAR':
        key = l[1][:-1]
        dict[key] = {}
        while True:
            ll = _in.readline()
            if ll.startswith('BBX'):
                dict[key]['BBX'] = [ int(s) for s in ll.split(' ')[1:] ]
                _in.readline()
                dict[key]['BITMAP'] = []
                for _ in range(dict[key]['BBX'][1]):
                    dict[key]['BITMAP'].append(_in.readline()[:-1])
                break

print(dict)


a = 'e'

uni = hex(ord(a))[2:]

uni = '0' * (4 - len(uni)) + uni

letter = dict[uni]

for h in letter['BITMAP']:
    for s in bin(int(h, 16))[2:]:
        if s == '0':
            print(' ', end='')
        else:
            print('1', end='')
    print()
