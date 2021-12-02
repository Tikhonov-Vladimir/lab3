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
                dict[key]['BBX'] = [int(s) for s in ll.split(' ')[1:]]
                _in.readline()
                dict[key]['BITMAP'] = []
                for _ in range(dict[key]['BBX'][1]):
                    dict[key]['BITMAP'].append(_in.readline()[:-1])
                break

print(dict)

s = input()

uni = ['0' * len(hex(ord(a))[2:]) + hex(ord(a))[2:].upper() for a in s] #из букв строки делаем массив с кодами этих букв
min_lower = 100
max_upper = -100
sum = 0
for i in uni:
    h = dict[i]['BBX']
    sum += h[0]
    if min_lower > h[3]:
        min_lower = h[3]
    if max_upper < h[3] + h[1]:
        max_upper = h[3] + h[1]
width = str((hex(sum)[2:])[::-1]) + '0' * (4 - len((hex(sum)[2:])[::-1])) # два числа к 16-ричным числам в обратном порядке
width = width.upper()
lenght = str((hex(max_upper - min_lower)[2:])[::-1]) + '0' * (4 - len((hex(max_upper - min_lower)[2:])[::-1]))
lenght = lenght.upper()
#print(width,width[:2] + '0' + width[2:])
base = '''49 49 2A 00 08 00 00 00 0F 00 00 01 03 00 01 00 00 00''' + width[:2][::-1] + width[2:][::-1] + '''00 00 01 01 03 00 01 00 00 00''' + lenght[:2][::-1] + lenght[2:][::-1] +'''00 00 02 01 03 00 03 00 00 00 C2 00 00 00 03 01 03 00 01 00 00 00 01 00 00 00 06 01 03 00 01 00 
00 00 02 00 00 00 0A 01 03 00 01 00 00 00 01 00 00 00 11 01 04 00 07 00 00 00 C8 00 00 00 12 01 
03 00 01 00 00 00 02 00 00 00 15 01 03 00 01 00 00 00 03 00 00 00 16 01 03 00 01 00 00 00 80 00 
00 00 17 01 04 00 07 00 00 00 E4 00 00 00 1C 01 03 00 01 00 00 00 01 00 00 00 29 01 03 00 02 00 
00 00 00 00 01 00 3E 01 05 00 02 00 00 00 00 01 00 00 3F 01 05 00 06 00 00 00 10 01 00 00 00 00 
00 00 08 00 08 00 08 00 40 01 00 00 40 01 0F 00 40 01 1E 00 40 01 2D 00 40 01 3C 00 40 01 4B 00 
40 01 5A 00 00 00 0F 00 00 00 0F 00 00 00 0F 00 00 00 0F 00 00 00 0F 00 00 00 0F 00 00 F6 09 00 
80 1B 0D 50 FF FF FF FF 00 58 39 54 FF FF FF FF 00 0A D7 A3 FF FF FF FF 80 E1 7A 54 FF FF FF FF 
00 CD CC 4C FF FF FF FF 00 9A 99 99 FF FF FF FF 80 66 66 26 FF FF FF FF F0 28 5C 0F FF FF FF FF'''

for h in range(min_lower,max_upper):
    for j in uni:
        a = h - dict[j]['BBX'][3]
        if (a >= 0 and a < dict[j]['BBX'][1]):
            stroka = (bin(int(dict[j]['BITMAP'][a], 16))[2:])
            stroka = '0' * (8 - len(stroka)) + stroka
            stroka = stroka[:dict[j]['BBX'][0]]
            for s in stroka:
                if s == '0':
                    base += (' FF 00 00')
                else:
                    base += (' 00 00 00')

        else:
            for s in range(dict[j]['BBX'][0]):
                base += ' FF 00 00'
f = open('6e6173747961207a61696b61.tiff', 'wb')
f.write(bytes.fromhex((base)))