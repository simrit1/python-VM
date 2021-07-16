import threading
import pygame
import sys

pygame.init()
WIDTH = 500
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY = {-2:WIDTH, -1:HEIGHT}

def text(brightness, text, pos, size, font='courier', antiAlias=True, background=None):
    myfont = pygame.font.SysFont(font, size)
    colour = [brightness]*3
    textsurface = myfont.render(text, antiAlias, colour, background)
    x = pos[0]
    y = pos[1]
    window.blit(textsurface, (x, y))
    return myfont.size(text)

NEWLINE = f'\n'

def unrender(value, emptyType='empty'):
    if value == 'empty':
        if emptyType == 'int':
            return 0
        elif emptyType == 'str':
            return ''
    if type(value) == str:
        if value[0] == '#':
            return int(value[1:])
        elif value[0] == '$':
            return value[1:]
        else:
            return value
    else:
        return value

def render(value):
    if type(value) == int:
        return '#' + str(value)
    elif type(value) == str:
        if value == '':
            return 'empty'
            pass
        else:
            return '$' + value

class prog:
    def __init__(self, file, args=[]):
        with open(file) as f:
            self.program = f.read().split(NEWLINE)
        self.fileName = file
        self.initArgs = args
    
    def getMem(self, location):
        if ':' not in location:
            if location == 'DISP':
                return DISPLAY
            elif location in self.memory:
                return self.memory[location]
            else:
                return {}
        reg = location.split(':')[-1]
        index = int(self.parse(':'.join(location.split(':')[:-1])))
        # print(f'getMem> reg: {reg}, index: {index}')
        if reg == 'DISP':
            return DISPLAY[index]
        elif reg in self.memory:
            if index in self.memory[reg]:
                return self.memory[reg][index]
            else:
                self.setMem(location, 'empty')
                return 'empty'
        else:
            self.setMem(location, 'empty')
            return 'empty'

    def parse(self, string):
        operators = ['!', '@', '#', '$']
        if string[0] == '!':
            if string[1] not in operators:
                return self.initArgs[int(self.parse(string[1:]))]
            else:
                return self.initArgs(self.parse(string[1:]))
        elif string[0] == '@':
            if string[1] not in operators:
                return unrender(self.getMem(string[1:]))
            else:
                if self.parse(string[1:]) in self.memory:
                    return unrender(self.getMem(string[1:]))
                else:
                    self.setMem(string[1:], 'empty')
                    return 'empty'
        elif string[0] == '#':
            if string[1] not in '!@':
                return int(string[1:])
            else:
                return int(self.parse(string[1:]))
        elif string[0] == '$':
            if string == '$':
                return ''
            elif string[1] not in '!@':
                return string[1:]
            else:
                if string[1] == '@':
                    return str(self.parse(string[1:]))
                else:
                    return str(self.parse(string[1:]))
        elif string == '%':
            result = []
            for key in self.labels.keys():
                result += [str(key)]
            return ','.join(result)
        elif string[0] == '%':
            return self.labels[self.parse(string[1:])]
        elif string[:2] == '+(':
            bool = True
            for item in string[2:].split(','):
                try:
                    bool = type(self.parse(item)) == str
                    break
                except:
                    pass
            if bool:
                array = []
                for item in string[2:].split(','):
                    if item != '':
                        array += [self.parse(item)]
                        if type(self.parse(item)) != str:
                            raise TypeError(f'@{self.instruction}: {self.fileName}>parser: {string[2:]} does not have consistent types')
                    else:
                        array += ['']
                return ' '.join(array)
            else:
                total = 0
                for item in string[2:].split(','):
                    total += self.parse(item)
                if type(self.parse(item)) != int:
                    raise TypeError(f'@{self.instruction}: {self.fileName}>parser: {string[2:]} does not have consistent types')
                return total
        elif string[:2] == '-(':
            if type(self.parse(string[2:].split(',')[0])) == str:
                result = ''
                for item in string[2:].split(','):
                    result += self.parse(item)
                if type(self.parse(item)) != str:
                    raise TypeError(f'@{self.instruction}: {self.fileName}>parser: {string[2:]} does not have consistent types')
                return result
        elif string[:2] == '*(':
            total = 0
            if type(self.parse(string[2:].split(',')[0])) == int:
                for index, item in enumerate(string[2:].split(',')):
                    if index == 0:
                        total = self.parse(item)
                    else:
                        total *= self.parse(item)
                if type(self.parse(item)) != int:
                    raise TypeError(f'@{self.instruction}: {self.fileName}>parser: {string[2:]} does not have consistent types')
                return total
        elif string[0] == '[':
            array = []
            for index, arg in enumerate(string[1:].split(',')):
                if type(self.parse(arg)) != int and index % 2 == 0:
                    raise TypeError(f'@{self.instruction}: {self.fileName}>parser: {string} contains non <INT> types')
                array += [self.parse(arg)]
            result = array[0]
            for index, value in enumerate(array[2::2]):
                index *= 2
                if array[index+1] == '+':
                    result += value
                elif array[index+1] == '-':
                    result -= value
                elif array[index+1] == '/':
                    result /= value
                elif array[index+1] == '*':
                    result *= value
                elif array[index+1] == '^':
                    result **= value
            return result

        else:
            return string
                
    
    def start(self):
        self.instruction = 0
        self.memory = {}
        self.labels = {}
        self.cmp = []
        for index, line in enumerate(self.program):
            for index2, char in enumerate(line):
                if char != ' ':
                    line = line[index2:]
                    break
            cmd = line.split(' ')[0]
            args = line.split(' ')[1:]
            if cmd == 'lbl':
                self.labels[self.parse(args[0])] = index
        while self.instruction < len(self.program):
            self.run()
    
    def setMem(self, location, value):
        global DISPLAY
        if len(location.split(':')) == 0:
            reg = location
            if type(value) == dict:
                self.memory[reg] = value
            else:
                self.memory[reg][0] = self.parse(value)
        reg = location.split(':')[-1]
        index = int(self.parse(''.join(location.split(':')[:-1])))
        if reg == 'DISP':
            if index >= 0:
                DISPLAY[index] = value
        elif reg in self.memory:
            self.memory[reg][index] = value
        else:
            self.memory[reg] = {index: value}
        
    
    def run(self):
        def keyDo(boolean, args, address):
            if boolean:
                self.setMem(address, self.parse(args[0]))
            else:
                if len(args) >= 2:
                    self.setMem(address, self.parse(args[1]))
        line = self.program[self.instruction]
        for index, char in enumerate(line):
            if char != ' ':
                line = line[index:]
                break
        cmd = line.split(' ')[0]
        args = line.split(' ')[1:]

        if line == '':
            self.instruction += 1
            return

        # print(f'{self.fileName}>{self.instruction+1}>{line}')

        #ldr
        if cmd == 'ldr':
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>ldr: {args[0]} is not a memory address')
            location = args[0]
            value = render(self.parse(args[1]))
            if len(location.split(':')) == 1:
                if value[0] == '@' and len(value.split(':')) == 1:
                    self.setMem(location[1:], self.getMem(value[1:]))
            else:
                index = self.parse(':'.join(location.split(':')[:-1])[1:])
                reg = location.split(':')[-1]
                self.setMem(':'.join([str(index), reg]), value)
        #clr
        elif cmd == 'clr':
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>clr: {args[0]} is not a memory address')
            location = args[0][1:]
            reg = location.split(':')[-1]
            index = self.parse(':'.join(location.split(':')[:-1]))
            if index in self.memory[reg]:
                self.memory[reg].pop(index)
        #dsp
        elif cmd == 'dsp':
            if args[0] == 'update':
                pygame.display.update()
            elif args[0] == 'draw':
                if args[1] == 'rect':
                    pygame.draw.rect(window, [unrender(self.parse(args[6]))%255]*3, ((self.parse(args[2]), self.parse(args[3])), (self.parse(args[4]), self.parse(args[5]))))
                if args[1] == 'text':
                    if len(args) == 8:
                        font = self.parse(args[7])
                    else:
                        font = 'courier'
                    text(self.parse(args[2]), self.parse(args[3]), (self.parse(args[4]), self.parse(args[5])), self.parse(args[6]), font)
            elif args[0] == 'key':
                if args[1][0] != '@':
                    raise TypeError(f'@{self.instruction}: {self.fileName}>dsp key: {args[0]} is not a memory address')
                actualDestination = args[1][1:]
                reg = actualDestination.split(':')[-1]
                index = self.parse(':'.join(actualDestination.split(':')[:-1]))
                destination = f'{index}:{reg}'
                key = self.parse(args[2])
                keys = pygame.key.get_pressed()
                if key == 'backspace':
                    keyDo(keys[pygame.key.K_BACKSPACE], args[3:], destination)
                elif key == 'tab':
                    keyDo(keys[pygame.key.K_TAB], args[3:], destination)
                elif key == 'clear':
                    keyDo(keys[pygame.key.K_CLEAR], args[3:], destination)
                elif key == 'return':
                    keyDo(keys[pygame.key.K_RETURN], args[3:], destination)
                elif key == 'pause':
                    keyDo(keys[pygame.key.K_PAUSE], args[3:], destination)
                elif key == 'esc':
                    keyDo(keys[pygame.constants.K_ESCAPE], args[3:], destination)
                elif key == 'space':
                    keyDo(keys[pygame.key.K_SPACE], args[3:], destination)
                elif key == '!':
                    keyDo(keys[pygame.key.K_EXCLAIM], args[3:], destination)
                elif key == '"':
                    keyDo(keys[pygame.key.K_QUOTEDBL], args[3:], destination)
                elif key == '#':
                    keyDo(keys[pygame.key.K_HASH], args[3:], destination)
                elif key == '$':
                    keyDo(keys[pygame.key.K_DOLLAR], args[3:], destination)
                elif key == '&':
                    keyDo(keys[pygame.key.K_AMPERSAND], args[3:], destination)
                elif key == "'":
                    # This one might not be right
                    keyDo(keys[pygame.key.K_QUOTE], args[3:], destination)
                elif key == '(':
                    keyDo(keys[pygame.key.K_LEFTPAREN], args[3:], destination)
                elif key == ')':
                    keyDo(keys[pygame.key.K_RIGHTPAREN], args[3:], destination)
                elif key == '*':
                    keyDo(keys[pygame.key.K_ASTERIX], args[3:], destination)
                elif key == '+':
                    keyDo(keys[pygame.key.K_PLUS], args[3:], destination)
                elif key == ',':
                    keyDo(keys[pygame.key.K_COMMA], args[3:], destination)
                elif key == '-':
                    keyDo(keys[pygame.key.K_MINUS], args[3:], destination)
                elif key == '.':
                    keyDo(keys[pygame.key.K_PERIOD], args[3:], destination)
                elif key == '/':
                    keyDo(keys[pygame.key.K_SLASH], args[3:], destination)
                elif key == '0':
                    keyDo(keys[pygame.key.K_0], args[3:], destination)
                elif key == '1':
                    keyDo(keys[pygame.key.K_1], args[3:], destination)
                elif key == '2':
                    keyDo(keys[pygame.key.K_2], args[3:], destination)
                elif key == '3':
                    keyDo(keys[pygame.key.K_3], args[3:], destination)
                elif key == '4':
                    keyDo(keys[pygame.key.K_4], args[3:], destination)
                elif key == '5':
                    keyDo(keys[pygame.key.K_5], args[3:], destination)
                elif key == '6':
                    keyDo(keys[pygame.key.K_6], args[3:], destination)
                elif key == '7':
                    keyDo(keys[pygame.key.K_7], args[3:], destination)
                elif key == '8':
                    keyDo(keys[pygame.key.K_8], args[3:], destination)
                elif key == '9':
                    keyDo(keys[pygame.key.K_9], args[3:], destination)
                elif key == ':':
                    keyDo(keys[pygame.key.K_COLON], args[3:], destination)
                elif key == ';':
                    keyDo(keys[pygame.key.K_SEMICOLON], args[3:], destination)
                elif key == '<':
                    keyDo(keys[pygame.key.K_LESS], args[3:], destination)
                elif key == '=':
                    keyDo(keys[pygame.key.K_EQUALS], args[3:], destination)
                elif key == '>':
                    keyDo(keys[pygame.key.K_GREATER], args[3:], destination)
                elif key == '?':
                    keyDo(keys[pygame.key.K_QUESTION], args[3:], destination)
                elif key == '@':
                    keyDo(keys[pygame.key.K_AT], args[3:], destination)
                elif key == '[':
                    keyDo(keys[pygame.key.K_LEFTBRACKET], args[3:], destination)
                elif key == '\\':
                    keyDo(keys[pygame.key.K_BACKSLASH], args[3:], destination)
                elif key == ']':
                    keyDo(keys[pygame.key.K_RIGHTBRACKET], args[3:], destination)
                elif key == '^':
                    keyDo(keys[pygame.key.K_CARET], args[3:], destination)
                elif key == '_':
                    keyDo(keys[pygame.key.K_UNDERSCORE], args[3:], destination)
                elif key == '`':
                    keyDo(keys[pygame.key.K_BACKQUOTE], args[3:], destination)
                elif key == 'a':
                    keyDo(keys[pygame.key.K_a], args[3:], destination)
                elif key == 'b':
                    keyDo(keys[pygame.key.K_b], args[3:], destination)
                elif key == 'c':
                    keyDo(keys[pygame.key.K_c], args[3:], destination)
                elif key == 'd':
                    keyDo(keys[pygame.key.K_d], args[3:], destination)
                elif key == 'e':
                    keyDo(keys[pygame.key.K_e], args[3:], destination)
                elif key == 'f':
                    keyDo(keys[pygame.key.K_f], args[3:], destination)
                elif key == 'g':
                    keyDo(keys[pygame.key.K_g], args[3:], destination)
                elif key == 'h':
                    keyDo(keys[pygame.key.K_h], args[3:], destination)
                elif key == 'i':
                    keyDo(keys[pygame.key.K_i], args[3:], destination)
                elif key == 'j':
                    keyDo(keys[pygame.key.K_j], args[3:], destination)
                elif key == 'k':
                    keyDo(keys[pygame.key.K_k], args[3:], destination)
                elif key == 'l':
                    keyDo(keys[pygame.key.K_l], args[3:], destination)
                elif key == 'm':
                    keyDo(keys[pygame.key.K_m], args[3:], destination)
                elif key == 'n':
                    keyDo(keys[pygame.key.K_n], args[3:], destination)
                elif key == 'o':
                    keyDo(keys[pygame.key.K_o], args[3:], destination)
                elif key == 'p':
                    keyDo(keys[pygame.key.K_p], args[3:], destination)
                elif key == 'q':
                    keyDo(keys[pygame.key.K_q], args[3:], destination)
                elif key == 'r':
                    keyDo(keys[pygame.key.K_r], args[3:], destination)
                elif key == 's':
                    keyDo(keys[pygame.key.K_s], args[3:], destination)
                elif key == 't':
                    keyDo(keys[pygame.key.K_t], args[3:], destination)
                elif key == 'u':
                    keyDo(keys[pygame.key.K_u], args[3:], destination)
                elif key == 'v':
                    keyDo(keys[pygame.key.K_v], args[3:], destination)
                elif key == 'w':
                    keyDo(keys[pygame.key.K_w], args[3:], destination)
                elif key == 'x':
                    keyDo(keys[pygame.key.K_x], args[3:], destination)
                elif key == 'y':
                    keyDo(keys[pygame.key.K_y], args[3:], destination)
                elif key == 'z':
                    keyDo(keys[pygame.key.K_z], args[3:], destination)
                elif key == 'del':
                    keyDo(keys[pygame.key.K_DELETE], args[3:], destination)
                elif key == 'kp0':
                    keyDo(keys[pygame.key.K_KP0], args[3:], destination)
                elif key == 'kp1':
                    keyDo(keys[pygame.key.K_KP1], args[3:], destination)
                elif key == 'kp2':
                    keyDo(keys[pygame.key.K_KP2], args[3:], destination)
                elif key == 'kp3':
                    keyDo(keys[pygame.key.K_KP3], args[3:], destination)
                elif key == 'kp4':
                    keyDo(keys[pygame.key.K_KP4], args[3:], destination)
                elif key == 'kp5':
                    keyDo(keys[pygame.key.K_KP5], args[3:], destination)
                elif key == 'kp6':
                    keyDo(keys[pygame.key.K_KP6], args[3:], destination)
                elif key == 'kp7':
                    keyDo(keys[pygame.key.K_KP7], args[3:], destination)
                elif key == 'kp8':
                    keyDo(keys[pygame.key.K_KP8], args[3:], destination)
                elif key == 'kp9':
                    keyDo(keys[pygame.key.K_KP9], args[3:], destination)
                elif key == 'kp.':
                    keyDo(keys[pygame.key.K_KP_PERIOD], args[3:], destination)
                elif key == 'kp/':
                    keyDo(keys[pygame.key.K_KP_DIVIDE], args[3:], destination)
                elif key == 'kp*':
                    keyDo(keys[pygame.key.K_KP_MULTIPLY], args[3:], destination)
                elif key == 'kp-':
                    keyDo(keys[pygame.key.K_KP_MINUS], args[3:], destination)
                elif key == 'kp+':
                    keyDo(keys[pygame.key.K_KP_PLUS], args[3:], destination)
                elif key == 'kpEnter':
                    keyDo(keys[pygame.key.K_KP_ENTER], args[3:], destination)
                elif key == 'kp=':
                    keyDo(keys[pygame.key.K_KP_EQUALS], args[3:], destination)
                elif key == 'up':
                    keyDo(keys[pygame.key.K_UP], args[3:], destination)
                elif key == 'down':
                    keyDo(keys[pygame.key.K_DOWN], args[3:], destination)
                elif key == 'right':
                    keyDo(keys[pygame.key.K_RIGHT], args[3:], destination)
                elif key == 'left':
                    keyDo(keys[pygame.key.K_LEFT], args[3:], destination)
                elif key == 'insert':
                    keyDo(keys[pygame.key.K_INSERT], args[3:], destination)
                elif key == 'home':
                    keyDo(keys[pygame.key.K_HOME], args[3:], destination)
                elif key == 'end':
                    keyDo(keys[pygame.key.K_END], args[3:], destination)
                elif key == 'pageup':
                    keyDo(keys[pygame.key.K_PAGEUP], args[3:], destination)
                elif key == 'pagedown':
                    keyDo(keys[pygame.key.K_PAGEDOWN], args[3:], destination)
                elif key == 'f1':
                    keyDo(keys[pygame.key.K_F1], args[3:], destination)
                elif key == 'f2':
                    keyDo(keys[pygame.key.K_F2], args[3:], destination)
                elif key == 'f3':
                    keyDo(keys[pygame.key.K_F3], args[3:], destination)
                elif key == 'f4':
                    keyDo(keys[pygame.key.K_F4], args[3:], destination)
                elif key == 'f5':
                    keyDo(keys[pygame.key.K_F5], args[3:], destination)
                elif key == 'f6':
                    keyDo(keys[pygame.key.K_F6], args[3:], destination)
                elif key == 'f7':
                    keyDo(keys[pygame.key.K_F7], args[3:], destination)
                elif key == 'f8':
                    keyDo(keys[pygame.key.K_F8], args[3:], destination)
                elif key == 'f9':
                    keyDo(keys[pygame.key.K_F9], args[3:], destination)
                elif key == 'f10':
                    keyDo(keys[pygame.key.K_F10], args[3:], destination)
                elif key == 'f11':
                    keyDo(keys[pygame.key.K_F11], args[3:], destination)
                elif key == 'f12':
                    keyDo(keys[pygame.key.K_F12], args[3:], destination)
                elif key == 'f13':
                    keyDo(keys[pygame.key.K_F13], args[3:], destination)
                elif key == 'f14':
                    keyDo(keys[pygame.key.K_F14], args[3:], destination)
                elif key == 'f15':
                    keyDo(keys[pygame.key.K_F15], args[3:], destination)
                elif key == 'numlock':
                    keyDo(keys[pygame.key.K_NUMLOCK], args[3:], destination)
                elif key == 'capslock':
                    keyDo(keys[pygame.key.K_CAPSLOCK], args[3:], destination)
                elif key == 'scrollock':
                    keyDo(keys[pygame.key.K_SCROLLOCK], args[3:], destination)
                elif key == 'rShift':
                    keyDo(keys[pygame.key.K_RSHIFT], args[3:], destination)
                elif key == 'lShift':
                    keyDo(keys[pygame.key.K_LSHIFT], args[3:], destination)
                elif key == 'rCtrl':
                    keyDo(keys[pygame.key.K_RCTRL], args[3:], destination)
                elif key == 'lCtrl':
                    keyDo(keys[pygame.key.K_LCTRL], args[3:], destination)
                elif key == 'rAlt':
                    keyDo(keys[pygame.key.K_RALT], args[3:], destination)
                elif key == 'lAlt':
                    keyDo(keys[pygame.key.K_LA], args[3:], destination)
                elif key == 'rMeta':
                    keyDo(keys[pygame.key.K_RMETA], args[3:], destination)
                elif key == 'lMeta':
                    keyDo(keys[pygame.key.K_LMETA], args[3:], destination)
                elif key == 'rOS':
                    keyDo(keys[pygame.key.K_RSUPER], args[3:], destination)
                elif key == 'lOS':
                    keyDo(keys[pygame.key.K_LSUPER], args[3:], destination)
                elif key == 'mode':
                    keyDo(keys[pygame.key.K_MODE], args[3:], destination)
                elif key == 'help':
                    keyDo(keys[pygame.key.K_HELP], args[3:], destination)
                elif key == 'sysreq':
                    keyDo(keys[pygame.key.K_SYSREQ], args[3:], destination)
                elif key == 'break':
                    keyDo(keys[pygame.key.K_BREAK], args[3:], destination)
                elif key == 'menu':
                    keyDo(keys[pygame.key.K_MENU], args[3:], destination)
                elif key == 'power':
                    keyDo(keys[pygame.key.K_POWER], args[3:], destination)
                elif key == 'euro':
                    keyDo(keys[pygame.key.K_EURO], args[3:], destination)
                
        #mov
        elif cmd == 'mov':
            destination = self.parse(args[0][1:])
            source = self.parse(args[1])
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>mov>destination: {args[0]} is not a memory address')
            if args[1][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>mov>source: {args[1]} is not a memory address')
            self.setMem(destination, source)
        #cpy
        elif cmd == 'cpy':
            destination = self.parse(args[0][1:])
            source = self.parse(args[1])
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
            if args[1][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>source: {args[1]} is not a memory address')
            self.setMem(destination, source)
        #add
        elif cmd == 'add':
            destination = args[0][1:]
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
            if len(args) >= 2:
                source = self.parse(args[1])
                if type(self.getMem(destination)) == dict:
                    i = 0
                    while i in self.getMem(destination):
                        i += 1
                    self.setMem(f'{i}:{destination}', source)
                else:
                    self.setMem(destination, render(unrender(self.getMem(destination)) + source))
            else:
                self.setMem(destination, render(unrender(self.getMem(destination), emptyType='int') + 1))
        #sub
        elif cmd == 'sub':
            destination = self.parse(args[0][1:])
            source = self.parse(args[1])
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
            if len(args) < 2:
                source = self.parse(args[1])
                self.setMem(destination, render(unrender(self.getmem(destination)) - source))
            else:
                self.setMem(destination, render(unrender(self.getMemdestination)) - 1)
        #div
        elif cmd == 'div':
            destination = self.parse(args[0][1:])
            source = self.parse(args[1])
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
            self.setMem(destination, render(unrender(self.getMem(destination)) // source))
        #mul
        elif cmd == 'mul':
            destination = self.parse(args[0][1:])
            source = self.parse(args[1])
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
            self.setMem(destination, render(unrender(self.getMem(destination)) * source))
        #lbl
        elif cmd == 'lbl':
            pass
        #spl
        elif cmd == 'spl':
            destination = self.parse(args[0][1:])
            string = str(self.parse(args[1]))
            index = int(self.parse(args[2]))
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
            self.setMem(destination, string[index])

        #cmp
        elif cmd == 'cmp':
            self.cmp = []
            for arg in args:
                if arg[0] == '@':
                    self.cmp += [unrender(self.getMem(arg[1:]))]
                else:
                    self.cmp += [unrender(self.parse(arg))]

        #jmp
        elif cmd == 'jmp':
            self.instruction = self.parse(args[0])
        elif cmd[0] == 'j':
            condition = cmd[1:]
            if type(self.cmp[0]) == int:
                if type(self.cmp[1]) != int:
                    self.cmp[1] = len(self.cmp[1])
            else:
                if type(self.cmp[1]) == int:
                    self.cmp[0] = len(self.cmp[0])

            if condition == 'e':
                if self.cmp[0] == self.cmp[1]:
                    self.instruction = self.parse(args[0])
            elif condition == 'ne':
                if self.cmp[0] != self.cmp[1]:
                    self.instruction = self.parse(args[0])
            elif condition == 'g':
                if self.cmp[0] > self.cmp[1]:
                    self.instruction = self.parse(args[0])
            elif condition == 'ge':
                if self.cmp[0] >= self.cmp[1]:
                    self.instruction = self.parse(args[0])
            elif condition == 'l':
                if self.cmp[0] < self.cmp[1]:
                    self.instruction = self.parse(args[0])
            elif condition == 'le':
                if self.cmp[0] <= self.cmp[1]:
                    self.instruction = self.parse(args[0])
            elif condition == 'dv':
                if self.cmp[0] % self.cmp[1] == 0:
                    self.instruction = self.parse(args[0])
        #exc
        elif cmd == 'exc':
            excArgs = []
            for argument in args[1:]:
                excArgs += [self.parse(argument)]
            try:
                filePath = 'files/'
                filePath += str(self.parse(args[0]))
                program = prog(filePath, excArgs)
                program.start()
            except FileNotFoundError as err:
                print(f'File Does Not Exist: {self.parse(args[0])}')
                print(err)
                print(filePath)
        #thr
        elif cmd == 'thr':
            excArgs = []
            for argument in args[1:]:
                excArgs += [self.parse(argument)]
            try:
                program = prog('files/' + str(self.parse(args[0])), excArgs)
                thread = threading.Thread(target=program.start)
                thread.start()
            except FileNotFoundError:
                print(f'File Does Not Exist: {self.parse(args[0])}')
        #out
        elif cmd == 'out':
            destination = self.parse(args[0])
            if destination  == 'term':
                if args[1] == '@':
                    print(sorted(self.memory.items()))
                elif args[1] == '@:DISP':
                    print(sorted(DISPLAY.items()))
                else:
                    print(unrender(self.parse(args[1])))
            else:
                filePath = f'files/{destination}'
                with open(filePath, 'a') as file:
                    file.write(f'\n{unrender(self.parse(args[1]))}')
        #get
        elif cmd == 'get':
            destination = args[0][1:]
            source = self.parse(args[1])
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>get>destination: {args[0]} is not a memory address')
            if source == 'term':
                user = '#'
                while '#' in user:
                    user = input()
                    if '#' in user:
                        print('You cannot use that character (#)')
                self.setMem(destination, render(user))
            else:
                filePath = f'files/{source}'
                with open(filePath) as file:
                    self.setMem(destination, file.read())
        #set
        elif cmd == 'set':
            destination = self.parse(args[0])
            source = self.parse(args[1])
            filePath = f'files/{source}'
            with open(filePath, 'w')as file:
                file.write(str(source))
        # Comment
        elif cmd[0] == '>':
            pass
        else:
            print(f'{cmd} does not seem to be a command')
        self.instruction += 1


# Boot
bootProg = prog('files/boot.x', [])
thread = threading.Thread(target=bootProg.start)
thread.start()

while True:
    for event in pygame.event.get(eventtype=pygame.QUIT):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()