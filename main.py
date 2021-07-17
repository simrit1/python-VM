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

def textBounds(text, size, font='courier'):
    myfont = pygame.font.SysFont(font, size)
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
    def keyDo(self, boolean, args, address):
        if boolean:
            self.setMem(address, self.parse(args[0]))
        else:
            if len(args) >= 2:
                self.setMem(address, self.parse(args[1]))

    # Commands
    def ldr(self, args):
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
    
    def clr(self, args):
        if args[0][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>clr: {args[0]} is not a memory address')
        location = args[0][1:]
        reg = location.split(':')[-1]
        index = self.parse(':'.join(location.split(':')[:-1]))
        if index in self.memory[reg]:
            self.memory[reg].pop(index)
    
    def dsp(self, args):
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
                self.keyDo(keys[pygame.key.K_BACKSPACE], args[3:], destination)
            elif key == 'tab':
                self.keyDo(keys[pygame.key.K_TAB], args[3:], destination)
            elif key == 'clear':
                self.keyDo(keys[pygame.key.K_CLEAR], args[3:], destination)
            elif key == 'return':
                self.keyDo(keys[pygame.key.K_RETURN], args[3:], destination)
            elif key == 'pause':
                self.keyDo(keys[pygame.key.K_PAUSE], args[3:], destination)
            elif key == 'esc':
                self.keyDo(keys[pygame.constants.K_ESCAPE], args[3:], destination)
            elif key == 'space':
                self.keyDo(keys[pygame.key.K_SPACE], args[3:], destination)
            elif key == '!':
                self.keyDo(keys[pygame.key.K_EXCLAIM], args[3:], destination)
            elif key == '"':
                self.keyDo(keys[pygame.key.K_QUOTEDBL], args[3:], destination)
            elif key == '#':
                self.keyDo(keys[pygame.key.K_HASH], args[3:], destination)
            elif key == '$':
                self.keyDo(keys[pygame.key.K_DOLLAR], args[3:], destination)
            elif key == '&':
                self.keyDo(keys[pygame.key.K_AMPERSAND], args[3:], destination)
            elif key == "'":
                # This one might not be right
                self.keyDo(keys[pygame.key.K_QUOTE], args[3:], destination)
            elif key == '(':
                self.keyDo(keys[pygame.key.K_LEFTPAREN], args[3:], destination)
            elif key == ')':
                self.keyDo(keys[pygame.key.K_RIGHTPAREN], args[3:], destination)
            elif key == '*':
                self.keyDo(keys[pygame.key.K_ASTERIX], args[3:], destination)
            elif key == '+':
                self.keyDo(keys[pygame.key.K_PLUS], args[3:], destination)
            elif key == ',':
                self.keyDo(keys[pygame.key.K_COMMA], args[3:], destination)
            elif key == '-':
                self.keyDo(keys[pygame.key.K_MINUS], args[3:], destination)
            elif key == '.':
                self.keyDo(keys[pygame.key.K_PERIOD], args[3:], destination)
            elif key == '/':
                self.keyDo(keys[pygame.key.K_SLASH], args[3:], destination)
            elif key == '0':
                self.keyDo(keys[pygame.key.K_0], args[3:], destination)
            elif key == '1':
                self.keyDo(keys[pygame.key.K_1], args[3:], destination)
            elif key == '2':
                self.keyDo(keys[pygame.key.K_2], args[3:], destination)
            elif key == '3':
                self.keyDo(keys[pygame.key.K_3], args[3:], destination)
            elif key == '4':
                self.keyDo(keys[pygame.key.K_4], args[3:], destination)
            elif key == '5':
                self.keyDo(keys[pygame.key.K_5], args[3:], destination)
            elif key == '6':
                self.keyDo(keys[pygame.key.K_6], args[3:], destination)
            elif key == '7':
                self.keyDo(keys[pygame.key.K_7], args[3:], destination)
            elif key == '8':
                self.keyDo(keys[pygame.key.K_8], args[3:], destination)
            elif key == '9':
                self.keyDo(keys[pygame.key.K_9], args[3:], destination)
            elif key == ':':
                self.keyDo(keys[pygame.key.K_COLON], args[3:], destination)
            elif key == ';':
                self.keyDo(keys[pygame.key.K_SEMICOLON], args[3:], destination)
            elif key == '<':
                self.keyDo(keys[pygame.key.K_LESS], args[3:], destination)
            elif key == '=':
                self.keyDo(keys[pygame.key.K_EQUALS], args[3:], destination)
            elif key == '>':
                self.keyDo(keys[pygame.key.K_GREATER], args[3:], destination)
            elif key == '?':
                self.keyDo(keys[pygame.key.K_QUESTION], args[3:], destination)
            elif key == '@':
                self.keyDo(keys[pygame.key.K_AT], args[3:], destination)
            elif key == '[':
                self.keyDo(keys[pygame.key.K_LEFTBRACKET], args[3:], destination)
            elif key == '\\':
                self.keyDo(keys[pygame.key.K_BACKSLASH], args[3:], destination)
            elif key == ']':
                self.keyDo(keys[pygame.key.K_RIGHTBRACKET], args[3:], destination)
            elif key == '^':
                self.keyDo(keys[pygame.key.K_CARET], args[3:], destination)
            elif key == '_':
                self.keyDo(keys[pygame.key.K_UNDERSCORE], args[3:], destination)
            elif key == '`':
                self.keyDo(keys[pygame.key.K_BACKQUOTE], args[3:], destination)
            elif key == 'a':
                self.keyDo(keys[pygame.key.K_a], args[3:], destination)
            elif key == 'b':
                self.keyDo(keys[pygame.key.K_b], args[3:], destination)
            elif key == 'c':
                self.keyDo(keys[pygame.key.K_c], args[3:], destination)
            elif key == 'd':
                self.keyDo(keys[pygame.key.K_d], args[3:], destination)
            elif key == 'e':
                self.keyDo(keys[pygame.key.K_e], args[3:], destination)
            elif key == 'f':
                self.keyDo(keys[pygame.key.K_f], args[3:], destination)
            elif key == 'g':
                self.keyDo(keys[pygame.key.K_g], args[3:], destination)
            elif key == 'h':
                self.keyDo(keys[pygame.key.K_h], args[3:], destination)
            elif key == 'i':
                self.keyDo(keys[pygame.key.K_i], args[3:], destination)
            elif key == 'j':
                self.keyDo(keys[pygame.key.K_j], args[3:], destination)
            elif key == 'k':
                self.keyDo(keys[pygame.key.K_k], args[3:], destination)
            elif key == 'l':
                self.keyDo(keys[pygame.key.K_l], args[3:], destination)
            elif key == 'm':
                self.keyDo(keys[pygame.key.K_m], args[3:], destination)
            elif key == 'n':
                self.keyDo(keys[pygame.key.K_n], args[3:], destination)
            elif key == 'o':
                self.keyDo(keys[pygame.key.K_o], args[3:], destination)
            elif key == 'p':
                self.keyDo(keys[pygame.key.K_p], args[3:], destination)
            elif key == 'q':
                self.keyDo(keys[pygame.key.K_q], args[3:], destination)
            elif key == 'r':
                self.keyDo(keys[pygame.key.K_r], args[3:], destination)
            elif key == 's':
                self.keyDo(keys[pygame.key.K_s], args[3:], destination)
            elif key == 't':
                self.keyDo(keys[pygame.key.K_t], args[3:], destination)
            elif key == 'u':
                self.keyDo(keys[pygame.key.K_u], args[3:], destination)
            elif key == 'v':
                self.keyDo(keys[pygame.key.K_v], args[3:], destination)
            elif key == 'w':
                self.keyDo(keys[pygame.key.K_w], args[3:], destination)
            elif key == 'x':
                self.keyDo(keys[pygame.key.K_x], args[3:], destination)
            elif key == 'y':
                self.keyDo(keys[pygame.key.K_y], args[3:], destination)
            elif key == 'z':
                self.keyDo(keys[pygame.key.K_z], args[3:], destination)
            elif key == 'del':
                self.keyDo(keys[pygame.key.K_DELETE], args[3:], destination)
            elif key == 'kp0':
                self.keyDo(keys[pygame.key.K_KP0], args[3:], destination)
            elif key == 'kp1':
                self.keyDo(keys[pygame.key.K_KP1], args[3:], destination)
            elif key == 'kp2':
                self.keyDo(keys[pygame.key.K_KP2], args[3:], destination)
            elif key == 'kp3':
                self.keyDo(keys[pygame.key.K_KP3], args[3:], destination)
            elif key == 'kp4':
                self.keyDo(keys[pygame.key.K_KP4], args[3:], destination)
            elif key == 'kp5':
                self.keyDo(keys[pygame.key.K_KP5], args[3:], destination)
            elif key == 'kp6':
                self.keyDo(keys[pygame.key.K_KP6], args[3:], destination)
            elif key == 'kp7':
                self.keyDo(keys[pygame.key.K_KP7], args[3:], destination)
            elif key == 'kp8':
                self.keyDo(keys[pygame.key.K_KP8], args[3:], destination)
            elif key == 'kp9':
                self.keyDo(keys[pygame.key.K_KP9], args[3:], destination)
            elif key == 'kp.':
                self.keyDo(keys[pygame.key.K_KP_PERIOD], args[3:], destination)
            elif key == 'kp/':
                self.keyDo(keys[pygame.key.K_KP_DIVIDE], args[3:], destination)
            elif key == 'kp*':
                self.keyDo(keys[pygame.key.K_KP_MULTIPLY], args[3:], destination)
            elif key == 'kp-':
                self.keyDo(keys[pygame.key.K_KP_MINUS], args[3:], destination)
            elif key == 'kp+':
                self.keyDo(keys[pygame.key.K_KP_PLUS], args[3:], destination)
            elif key == 'kpEnter':
                self.keyDo(keys[pygame.key.K_KP_ENTER], args[3:], destination)
            elif key == 'kp=':
                self.keyDo(keys[pygame.key.K_KP_EQUALS], args[3:], destination)
            elif key == 'up':
                self.keyDo(keys[pygame.key.K_UP], args[3:], destination)
            elif key == 'down':
                self.keyDo(keys[pygame.key.K_DOWN], args[3:], destination)
            elif key == 'right':
                self.keyDo(keys[pygame.key.K_RIGHT], args[3:], destination)
            elif key == 'left':
                self.keyDo(keys[pygame.key.K_LEFT], args[3:], destination)
            elif key == 'insert':
                self.keyDo(keys[pygame.key.K_INSERT], args[3:], destination)
            elif key == 'home':
                self.keyDo(keys[pygame.key.K_HOME], args[3:], destination)
            elif key == 'end':
                self.keyDo(keys[pygame.key.K_END], args[3:], destination)
            elif key == 'pageup':
                self.keyDo(keys[pygame.key.K_PAGEUP], args[3:], destination)
            elif key == 'pagedown':
                self.keyDo(keys[pygame.key.K_PAGEDOWN], args[3:], destination)
            elif key == 'f1':
                self.keyDo(keys[pygame.key.K_F1], args[3:], destination)
            elif key == 'f2':
                self.keyDo(keys[pygame.key.K_F2], args[3:], destination)
            elif key == 'f3':
                self.keyDo(keys[pygame.key.K_F3], args[3:], destination)
            elif key == 'f4':
                self.keyDo(keys[pygame.key.K_F4], args[3:], destination)
            elif key == 'f5':
                self.keyDo(keys[pygame.key.K_F5], args[3:], destination)
            elif key == 'f6':
                self.keyDo(keys[pygame.key.K_F6], args[3:], destination)
            elif key == 'f7':
                self.keyDo(keys[pygame.key.K_F7], args[3:], destination)
            elif key == 'f8':
                self.keyDo(keys[pygame.key.K_F8], args[3:], destination)
            elif key == 'f9':
                self.keyDo(keys[pygame.key.K_F9], args[3:], destination)
            elif key == 'f10':
                self.keyDo(keys[pygame.key.K_F10], args[3:], destination)
            elif key == 'f11':
                self.keyDo(keys[pygame.key.K_F11], args[3:], destination)
            elif key == 'f12':
                self.keyDo(keys[pygame.key.K_F12], args[3:], destination)
            elif key == 'f13':
                self.keyDo(keys[pygame.key.K_F13], args[3:], destination)
            elif key == 'f14':
                self.keyDo(keys[pygame.key.K_F14], args[3:], destination)
            elif key == 'f15':
                self.keyDo(keys[pygame.key.K_F15], args[3:], destination)
            elif key == 'numlock':
                self.keyDo(keys[pygame.key.K_NUMLOCK], args[3:], destination)
            elif key == 'capslock':
                self.keyDo(keys[pygame.key.K_CAPSLOCK], args[3:], destination)
            elif key == 'scrollock':
                self.keyDo(keys[pygame.key.K_SCROLLOCK], args[3:], destination)
            elif key == 'rShift':
                self.keyDo(keys[pygame.key.K_RSHIFT], args[3:], destination)
            elif key == 'lShift':
                self.keyDo(keys[pygame.key.K_LSHIFT], args[3:], destination)
            elif key == 'rCtrl':
                self.keyDo(keys[pygame.key.K_RCTRL], args[3:], destination)
            elif key == 'lCtrl':
                self.keyDo(keys[pygame.key.K_LCTRL], args[3:], destination)
            elif key == 'rAlt':
                self.keyDo(keys[pygame.key.K_RALT], args[3:], destination)
            elif key == 'lAlt':
                self.keyDo(keys[pygame.key.K_LA], args[3:], destination)
            elif key == 'rMeta':
                self.keyDo(keys[pygame.key.K_RMETA], args[3:], destination)
            elif key == 'lMeta':
                self.keyDo(keys[pygame.key.K_LMETA], args[3:], destination)
            elif key == 'rOS':
                self.keyDo(keys[pygame.key.K_RSUPER], args[3:], destination)
            elif key == 'lOS':
                self.keyDo(keys[pygame.key.K_LSUPER], args[3:], destination)
            elif key == 'mode':
                self.keyDo(keys[pygame.key.K_MODE], args[3:], destination)
            elif key == 'help':
                self.keyDo(keys[pygame.key.K_HELP], args[3:], destination)
            elif key == 'sysreq':
                self.keyDo(keys[pygame.key.K_SYSREQ], args[3:], destination)
            elif key == 'break':
                self.keyDo(keys[pygame.key.K_BREAK], args[3:], destination)
            elif key == 'menu':
                self.keyDo(keys[pygame.key.K_MENU], args[3:], destination)
            elif key == 'power':
                self.keyDo(keys[pygame.key.K_POWER], args[3:], destination)
            elif key == 'euro':
                self.keyDo(keys[pygame.key.K_EURO], args[3:], destination)
    
    def mov(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>mov>destination: {args[0]} is not a memory address')
        if args[1][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>mov>source: {args[1]} is not a memory address')
        self.setMem(destination, source)
    
    def cpy(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        if args[1][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>source: {args[1]} is not a memory address')
        self.setMem(destination, source)
    
    def add(self, args):
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
    def sub(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        if len(args) < 2:
            source = self.parse(args[1])
            self.setMem(destination, render(unrender(self.getmem(destination)) - source))
        else:
            self.setMem(destination, render(unrender(self.getMemdestination)) - 1)
        
    def div(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        self.setMem(destination, render(unrender(self.getMem(destination)) // source))

    def mul(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        self.setMem(destination, render(unrender(self.getMem(destination)) * source))
    
    def spl(self, args):
        destination = self.parse(args[0][1:])
        string = str(self.parse(args[1]))
        index = int(self.parse(args[2]))
        if args[0][0] != '@':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        self.setMem(destination, string[index])

    def cmp(self, args):
        self.cmp = []
        for arg in args:
            if arg[0] == '@':
                self.cmp += [unrender(self.getMem(arg[1:]))]
            else:
                self.cmp += [unrender(self.parse(arg))]

    def j(self, args):
        condition = args[0]
        if type(self.cmp[0]) == int:
            if type(self.cmp[1]) != int:
                self.cmp[1] = len(self.cmp[1])
        else:
            if type(self.cmp[1]) == int:
                self.cmp[0] = len(self.cmp[0])
        if condition == 'mp':
            self.instruction = self.parse(args[1])
        elif condition == 'e':
            if self.cmp[0] == self.cmp[1]:
                self.instruction = self.parse(args[1])
        elif condition == 'ne':
            if self.cmp[0] != self.cmp[1]:
                self.instruction = self.parse(args[1])
        elif condition == 'g':
            if self.cmp[0] > self.cmp[1]:
                self.instruction = self.parse(args[1])
        elif condition == 'ge':
            if self.cmp[0] >= self.cmp[1]:
                self.instruction = self.parse(args[1])
        elif condition == 'l':
            if self.cmp[0] < self.cmp[1]:
                self.instruction = self.parse(args[1])
        elif condition == 'le':
            if self.cmp[0] <= self.cmp[1]:
                self.instruction = self.parse(args[1])
        elif condition == 'dv':
            if self.cmp[0] % self.cmp[1] == 0:
                self.instruction = self.parse(args[1])
    #exc
    def exc(self, args):
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
    def thr(self, args):
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
    def out(self, args):
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
    def get(self, args):
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
    def set(self, args):
        destination = self.parse(args[0])
        source = self.parse(args[1])
        filePath = f'files/{source}'
        with open(filePath, 'w')as file:
            file.write(str(source))

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
        self.commands = {
            'ldr': self.ldr,
            'clr': self.clr,
            'dsp': self.dsp,
            'mov': self.mov,
            'cpy': self.cpy,
            'add': self.add,
            'sub': self.sub,
            'div': self.div,
            'mul': self.mul,
            'spl': self.spl,
            'cmp': self.cmp,
            'j': self.j,
            'exc': self.exc,
            'thr': self.thr,
            'out': self.out,
            'get': self.get,
            'set': self.set
        }
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
        line = self.program[self.instruction]
        for index, char in enumerate(line):
            if char != ' ':
                line = line[index:]
                break
        cmd = line.split(' ')[0]
        args = line.split(' ')[1:]

        if line == '' or line[0] == '>' or cmd == 'lbl':
            self.instruction += 1
            return

        # print(f'{self.fileName}>{self.instruction+1}>{line}')

        self.commands[cmd](args)

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