def bdf():
    _in = open('unlearne.bdf', 'r')
    dict_ = {}

    while True:
        line = _in.readline().split(' ')
        if line[0] == 'CHARS':
            charnum = int(line[1])
            break

    for i in range(charnum):
        line1 = _in.readline().split(' ')
        if line1[0] == 'STARTCHAR':
            key = line1[1][:-1]
            dict_[key] = {}
            while True:
                ll = _in.readline()
                if ll.startswith('BBX'):
                    dict_[key]['BBX'] = [int(s) for s in ll.split(' ')[1:]]
                    _in.readline()
                    dict_[key]['BITMAP'] = []
                    for _ in range(dict_[key]['BBX'][1]):
                        dict_[key]['BITMAP'].append(_in.readline()[:-1])
                    break
    return dict_


def header():
    return '''49 49 2A 00 08 00 00 00''' + '''05 00''' + '''06 01 03 00 01 00 00 00 02 00 00 00 ''' + '''11 01 04 00 
    01 00 00 00 50 00 00 00'''


def width_and_lenght_and_image():
    dict_ = bdf()
    s = input()
    uni = ['0' * len(hex(ord(a))[2:]) + hex(ord(a))[2:].upper() for a in s]
    min_lower = 100
    max_upper = -100
    sum_ = 0
    for i in uni:
        h = dict_[i]['BBX']
        sum_ += h[0]
        if min_lower > h[3]:
            min_lower = h[3]
        if max_upper < h[3] + h[1]:
            max_upper = h[3] + h[1]
    width = str((hex(sum_)[2:])[::-1]) + '0' * (
            4 - len((hex(sum_)[2:])[::-1]))  # два числа к 16-ричным числам в обратном порядке
    width = width.upper()
    lenght = str((hex(max_upper - min_lower)[2:])[::-1]) + '0' * (4 - len((hex(max_upper - min_lower)[2:])[::-1]))
    lenght = lenght.upper()
    base = ''
    for h in range(min_lower, max_upper):
        for j in uni:
            a = h - dict_[j]['BBX'][3]
            if 0 <= a < dict_[j]['BBX'][1]:
                symbol_binary = (bin(int(dict_[j]['BITMAP'][a], 16))[2:])
                symbol_binary = '0' * (8 - len(symbol_binary)) + symbol_binary
                symbol_binary = symbol_binary[:dict_[j]['BBX'][0]]
                for s in symbol_binary:
                    if s == '0':
                        base += 'FF 00 00'
                    else:
                        base += '00 00 00'

            else:
                for s in range(dict_[j]['BBX'][0]):
                    base += ' FF 00 00'
    return ['''00 01 03 00 01 00 00 00''' + width[:2][::-1] + width[2:][::-1] + '''00 00 01 01 03 00 01 00 00 00''' +
            lenght[:2][::-1] + lenght[2:][::-1] + '''00 00''', base]


def bits_per_sample():
    return ''' 02 01 03 00 03 00 00 00 4A 00 00 00 ''' + '''00 00 00 00''' + '''08 00 08 00 08 00'''


def send():
    base = ''
    base += header()
    base_two_part = width_and_lenght_and_image()
    base += base_two_part[0]
    base += bits_per_sample()
    base += base_two_part[1]
    f = open('6e6173747961207a61696b61.tiff', 'wb')
    f.write(bytes.fromhex(base))


send()
