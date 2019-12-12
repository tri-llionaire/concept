import sys
VERSION = 'concept 1.0.0'
CHARACTER_ID = {
    '`': 'CH_00',
    '~': 'CH_01',
    '!': 'CH_02',
    '@': 'CH_03',
    '#': 'CH_04',
    '$': 'CH_05',
    '%': 'CH_06',
    '^': 'CH_07',
    '&': 'CH_08',
    '*': 'CH_09',
    '(': 'CH_0a',
    ')': 'CH_0b',
    '-': 'CH_0c',
    '_': 'CH_0d',
    '=': 'CH_0e',
    '+': 'CH_0f',
    '[': 'CH_10',
    ']': 'CH_11',
    '{': 'CH_12',
    '}': 'CH_13',
    '|': 'CH_14',
    ';': 'CH_15',
    ':': 'CH_16',
    ',': 'CH_17',
    '<': 'CH_18',
    '.': 'CH_19',
    '>': 'CH_1a',
    '/': 'CH_1b',
    '?': 'CH_1c',
    '\'': 'CH_1d',
    '\"': 'CH_1e',
    '\\': 'CH_1f',
}
COMMAND_ID = {
    'exit': 'CM_00',
    'help': 'CM_01',
    'clog': 'CM_02',
    'put': 'CM_03',
    'get': 'CM_04',
    'var': 'CM_05',
}
STRING_PREFIX = 'ST_'
INTEGER_PREFIX = 'IN_'
FLOAT_PREFIX = 'FL_'
NEGATIVE_INTEGER_PREFIX = 'NI_'
NEGATIVE_FLOAT_PREFIX = 'NF_'
VARIABLE_PREFIX = 'VR_'
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ENDINGS = [' ', '#']
INTERNAL_STRING_PREFIX = 'IS_'

line = 0
ids = []
last = 0
current = ''
passer = 0
y = ''
recent = 0
z = -1

def err():
    print('something went wrong')

def parse(line, ids, last, current, passer, y):
    ids = []
    line = line + '#'
    for x in line:
        if x not in ENDINGS:
            if last == 'str':
                current = current + x
            elif last == 'num':
                current = current + x
                if x not in NUMBERS:
                    last = 'str'
                if x == '.':
                    last = 'float'
            elif last == 'float':
                current = current + x
                if x not in NUMBERS:
                    last = 'str'
            elif last == 'intstr':
                current = current + x
                if x == '\'':
                    ids.append(INTERNAL_STRING_PREFIX + current[1:-1])
                    last = 0
                    current = ''
            elif x == '\'':
                last = 'intstr'
                current = current + x
            else:
                if x in CHARACTER_ID:
                    ids.append(CHARACTER_ID[x])
                elif x in NUMBERS:
                    last = 'num'
                    current = current + x
                else:
                    last = 'str'
                    current = current + x
        else:
            if last == 'str':
                for x in COMMAND_ID:
                    if current.startswith(x + '('):
                        ids.append(COMMAND_ID[x])
                        if x == 'var' or x == 'get':
                            y = VARIABLE_PREFIX
                        elif x == 'put':
                            y = STRING_PREFIX
                        if y == STRING_PREFIX:
                            if current[-2] == '\'' and current[current.index('(') + 1] == '\'':
                                ids.append(y + current[current.index('(') + 2:-2])
                            else:
                                err()
                                ids = []
                        else:
                            if current[-2] != '\'' and current[current.index('(') + 1] != '\'':
                                ids.append(y + str(current[current.index('(') + 1:-1]))
                            else:
                                err()
                                ids = []
                        passer = 1
                if current in COMMAND_ID:
                    ids.append(COMMAND_ID[current])
                else:
                    if passer == 0:
                        ids.append(STRING_PREFIX + current)
                    passer = 0
            elif last == 'num':
                ids.append(INTEGER_PREFIX + current)
            elif last == 'float':
                ids.append(FLOAT_PREFIX + current)
            else:
                if x != ' ' and x != '#':
                    err()
                    ids = []
            last = 0
            current = ''
            if x == '#':
                break
    return ids

def excte(ids, recent, z):
    for x in ids:
        z += 1
        if x.startswith('CM_'):
            if x == 'CM_00':
                sys.exit()
            elif x == 'CM_01':
                with open('INFO.txt', 'r') as q:
                    print(q.read())
            elif x == 'CM_02':
                with open('CHANGELOG.txt', 'r') as q:
                    print(q.read())
            elif x == 'CM_03':
                exec('print(\'{}\')'.format(ids[z + 1][3:]))
            elif x == 'CM_04':
                exec('{} = input(\'{}\')'.format(ids[z + 1][3:], ids[z + 3][3:]))
            elif x == 'CM_05':
                exec('{} = {}'.format(ids[z + 1][3:], ids[z + 3][3:]))

print('{} on python3; type exit to leave, help for help, clog for changelog'.format(VERSION))
while line != 'exit':
    if line != 0:
        ids = parse(line, ids, last, current, passer, y)
        excte(ids, recent, z)
    line = input('>>> ')