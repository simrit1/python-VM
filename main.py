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
    colour = [brightness%256]*3
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

    # Commands
    def ldr(self, args):
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>ldr>destination: {args[0]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        if destinationCentral:
            getMem = self.getGlobalMem
            setMem = self.setGlobalMem
        else:
            getMem = self.getMem
            setMem = self.setMem

        location = args[0][1:]
        value = self.parse(args[1])
        if len(location.split(':')) == 1:
            if value[0] in '@*' and len(value.split(':')) == 1:
                setMem(location[1:], value)
        else:
            index = self.parse(':'.join(location.split(':')[:-1]))
            reg = location.split(':')[-1]
            setMem(location, value)
    
    def clr(self, args):
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>clr>destination: {args[0]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        location = args[0][1:]
        reg = location.split(':')[-1]
        index = self.parse(':'.join(location.split(':')[:-1]))
        if destinationCentral:
            if index in MEMORY[reg]:
                MEMORY[reg].pop(index)
        else:
            if index in self.memory[reg]:
                self.memory[reg].pop(index)
    
    def mov(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>mov>destination: {args[0]} is not a memory address')
        if args[1][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>mov>source: {args[1]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        if destinationCentral:
            self.setMem(destination, source)
        else:
            self.setGlobalMem(destination, source)
    
    def cpy(self, args):
        destination = self.parse(args[0][1:])
        destinationCentral = args[0][0] == '*'
        source = self.parse(args[1])
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        if args[1][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>source: {args[1]} is not a memory address')
        if destinationCentral:
            self.setGlobalMem(destination, source)
        else:
            self.setMem(destination, source)
    
    def add(self, args):
        destination = args[0][1:]
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>add>destination: {args[0]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        if destinationCentral:
            getMem = self.getGlobalMem
            setMem = self.setGlobalMem
        else:
            getMem = self.getMem
            setMem = self.setMem
        if len(args) >= 2:
            source = self.parse(args[1])
            if type(getMem(destination)) == dict:
                i = 0
                while i in getMem(destination):
                    i += 1
                setMem(f'{i}:{destination}', source)
            else:
                setMem(destination, render(unrender(getMem(destination)) + source))
        else:
            setMem(destination, render(unrender(getMem(destination), emptyType='int') + 1))

    def sub(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        if destinationCentral:
            getMem = self.getGlobalMem
            setMem = self.setGlobalMem
        else:
            getMem = self.getMem
            setMem = self.setMem
        if len(args) < 2:
            source = self.parse(args[1])
            setMem(destination, render(unrender(getMem(destination)) - source))
        else:
            setMem(destination, render(unrender(getMem(destination)) - 1))
        
    def div(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        if destinationCentral:
            self.setGlobalMem(destination, render(unrender(self.getGlobalMem(destination)) // source))
        else:
            self.setMem(destination, render(unrender(self.getMem(destination)) // source))

    def mul(self, args):
        destination = self.parse(args[0][1:])
        source = self.parse(args[1])
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        if destinationCentral:
            self.setGlobalMem(destination, render(unrender(self.getGlobalMem(destination)) * source))
        else:
            self.setMem(destination, render(unrender(self.getMem(destination)) * source))
    
    def spl(self, args):
        destination = self.parse(args[0][1:])
        string = str(self.parse(args[1]))
        index = int(self.parse(args[2]))
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>cpy>destination: {args[0]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        if destinationCentral:
            self.setGlobalMem(destination, string[index])
        else:
            self.setMem(destination, string[index])

    def cmp(self, args):
        self.cmp = []
        for arg in args:
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
    #ret
    def ret(self, args):
        self.returnValue = self.parse(args[0])

    #exc
    def exc(self, args):
        if args[0] == 'return':
            excArgs = []
            for argument in args[3:]:
                excArgs += [self.parse(argument)]
            try:
                filePath = 'files/'
                filePath += str(self.parse(args[2]))
                program = prog(filePath, excArgs)
                program.start()
                destination = args[1][1:]
                destinationCentral = args[1][0] == '*'
                if destinationCentral:
                    self.setGlobalMem(destination, program.returnValue)
                else:
                    self.setMem(destination, program.returnValue)
            except FileNotFoundError as err:
                print(f'File Does Not Exist: {self.parse(args[2])}')
                print(err)
                print(filePath)
        else:
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
            else:
                print(unrender(self.parse(args[1])))
        elif destination == 'disp':
            pygame.display.update()
        elif destination == 'dispClose':
            global displayOn
            displayOn=False
        elif destination == 'dispRect':
            pygame.draw.rect(window, [unrender(self.parse(args[5])) % 255]*3, ((self.parse(args[1]), self.parse(args[2])),(self.parse(args[3]), self.parse(args[4]))))
        elif destination == 'dispText':
            text(unrender(self.parse(args[5])), self.parse(args[1]), (self.parse(args[2]), self.parse(args[3])), self.parse(args[4]))
        else:
            filePath = f'files/{destination}'
            with open(filePath, 'a') as file:
                file.write(f'\n{unrender(self.parse(args[1]))}')
    #get
    def get(self, args):
        def keyDo(boolean, address):
            if boolean:
                setMem(address, '$True')
            else:
                setMem(address, '$False')

        destination = args[0][1:]
        source = self.parse(args[1])
        if args[0][0] not in '@*':
            raise TypeError(f'@{self.instruction}: {self.fileName}>get>destination: {args[0]} is not a memory address')
        destinationCentral = args[0][0] == '*'
        if destinationCentral:
            getMem = self.getGlobalMem
            setMem = self.setGlobalMem
        else:
            getMem = self.getMem
            setMem = self.setMem
        if source == 'term':
            user = '#'
            while '#' in user:
                user = input()
                if '#' in user:
                    print('You cannot use that character (#)')
            setMem(destination, render(user))
        elif source == 'keys':
            key = args[2]
            keys = pygame.key.get_pressed()
            if key == 'backspace':
                keyDo(keys[pygame.key.K_BACKSPACE], destination)
            elif key == 'tab':
                keyDo(keys[pygame.key.K_TAB], destination)
            elif key == 'clear':
                keyDo(keys[pygame.key.K_CLEAR], destination)
            elif key == 'return':
                keyDo(keys[pygame.key.K_RETURN], destination)
            elif key == 'pause':
                keyDo(keys[pygame.key.K_PAUSE], destination)
            elif key == 'esc':
                keyDo(keys[pygame.constants.K_ESCAPE], destination)
            elif key == 'space':
                keyDo(keys[pygame.key.K_SPACE], destination)
            elif key == '!':
                keyDo(keys[pygame.key.K_EXCLAIM], destination)
            elif key == '"':
                keyDo(keys[pygame.key.K_QUOTEDBL], destination)
            elif key == '#':
                keyDo(keys[pygame.key.K_HASH], destination)
            elif key == '$':
                keyDo(keys[pygame.key.K_DOLLAR], destination)
            elif key == '&':
                keyDo(keys[pygame.key.K_AMPERSAND], destination)
            elif key == "'":
                # This one might not be right
                keyDo(keys[pygame.key.K_QUOTE], destination)
            elif key == '(':
                keyDo(keys[pygame.key.K_LEFTPAREN], destination)
            elif key == ')':
                keyDo(keys[pygame.key.K_RIGHTPAREN], destination)
            elif key == '*':
                keyDo(keys[pygame.key.K_ASTERIX], destination)
            elif key == '+':
                keyDo(keys[pygame.key.K_PLUS], destination)
            elif key == ',':
                keyDo(keys[pygame.key.K_COMMA], destination)
            elif key == '-':
                keyDo(keys[pygame.key.K_MINUS], destination)
            elif key == '.':
                keyDo(keys[pygame.key.K_PERIOD], destination)
            elif key == '/':
                keyDo(keys[pygame.key.K_SLASH], destination)
            elif key == '0':
                keyDo(keys[pygame.key.K_0], destination)
            elif key == '1':
                keyDo(keys[pygame.key.K_1], destination)
            elif key == '2':
                keyDo(keys[pygame.key.K_2], destination)
            elif key == '3':
                keyDo(keys[pygame.key.K_3], destination)
            elif key == '4':
                keyDo(keys[pygame.key.K_4], destination)
            elif key == '5':
                keyDo(keys[pygame.key.K_5], destination)
            elif key == '6':
                keyDo(keys[pygame.key.K_6], destination)
            elif key == '7':
                keyDo(keys[pygame.key.K_7], destination)
            elif key == '8':
                keyDo(keys[pygame.key.K_8], destination)
            elif key == '9':
                keyDo(keys[pygame.key.K_9], destination)
            elif key == ':':
                keyDo(keys[pygame.key.K_COLON], destination)
            elif key == ';':
                keyDo(keys[pygame.key.K_SEMICOLON], destination)
            elif key == '<':
                keyDo(keys[pygame.key.K_LESS], destination)
            elif key == '=':
                keyDo(keys[pygame.key.K_EQUALS], destination)
            elif key == '>':
                keyDo(keys[pygame.key.K_GREATER], destination)
            elif key == '?':
                keyDo(keys[pygame.key.K_QUESTION], destination)
            elif key == '@':
                keyDo(keys[pygame.key.K_AT], destination)
            elif key == '[':
                keyDo(keys[pygame.key.K_LEFTBRACKET], destination)
            elif key == '\\':
                keyDo(keys[pygame.key.K_BACKSLASH], destination)
            elif key == ']':
                keyDo(keys[pygame.key.K_RIGHTBRACKET], destination)
            elif key == '^':
                keyDo(keys[pygame.key.K_CARET], destination)
            elif key == '_':
                keyDo(keys[pygame.key.K_UNDERSCORE], destination)
            elif key == '`':
                keyDo(keys[pygame.key.K_BACKQUOTE], destination)
            elif key == 'a':
                keyDo(keys[pygame.key.K_a], destination)
            elif key == 'b':
                keyDo(keys[pygame.key.K_b], destination)
            elif key == 'c':
                keyDo(keys[pygame.key.K_c], destination)
            elif key == 'd':
                keyDo(keys[pygame.key.K_d], destination)
            elif key == 'e':
                keyDo(keys[pygame.key.K_e], destination)
            elif key == 'f':
                keyDo(keys[pygame.key.K_f], destination)
            elif key == 'g':
                keyDo(keys[pygame.key.K_g], destination)
            elif key == 'h':
                keyDo(keys[pygame.key.K_h], destination)
            elif key == 'i':
                keyDo(keys[pygame.key.K_i], destination)
            elif key == 'j':
                keyDo(keys[pygame.key.K_j], destination)
            elif key == 'k':
                keyDo(keys[pygame.key.K_k], destination)
            elif key == 'l':
                keyDo(keys[pygame.key.K_l], destination)
            elif key == 'm':
                keyDo(keys[pygame.key.K_m], destination)
            elif key == 'n':
                keyDo(keys[pygame.key.K_n], destination)
            elif key == 'o':
                keyDo(keys[pygame.key.K_o], destination)
            elif key == 'p':
                keyDo(keys[pygame.key.K_p], destination)
            elif key == 'q':
                keyDo(keys[pygame.key.K_q], destination)
            elif key == 'r':
                keyDo(keys[pygame.key.K_r], destination)
            elif key == 's':
                keyDo(keys[pygame.key.K_s], destination)
            elif key == 't':
                keyDo(keys[pygame.key.K_t], destination)
            elif key == 'u':
                keyDo(keys[pygame.key.K_u], destination)
            elif key == 'v':
                keyDo(keys[pygame.key.K_v], destination)
            elif key == 'w':
                keyDo(keys[pygame.key.K_w], destination)
            elif key == 'x':
                keyDo(keys[pygame.key.K_x], destination)
            elif key == 'y':
                keyDo(keys[pygame.key.K_y], destination)
            elif key == 'z':
                keyDo(keys[pygame.key.K_z], destination)
            elif key == 'del':
                keyDo(keys[pygame.key.K_DELETE], destination)
            elif key == 'kp0':
                keyDo(keys[pygame.key.K_KP0], destination)
            elif key == 'kp1':
                keyDo(keys[pygame.key.K_KP1], destination)
            elif key == 'kp2':
                keyDo(keys[pygame.key.K_KP2], destination)
            elif key == 'kp3':
                keyDo(keys[pygame.key.K_KP3], destination)
            elif key == 'kp4':
                keyDo(keys[pygame.key.K_KP4], destination)
            elif key == 'kp5':
                keyDo(keys[pygame.key.K_KP5], destination)
            elif key == 'kp6':
                keyDo(keys[pygame.key.K_KP6], destination)
            elif key == 'kp7':
                keyDo(keys[pygame.key.K_KP7], destination)
            elif key == 'kp8':
                keyDo(keys[pygame.key.K_KP8], destination)
            elif key == 'kp9':
                keyDo(keys[pygame.key.K_KP9], destination)
            elif key == 'kp.':
                keyDo(keys[pygame.key.K_KP_PERIOD], destination)
            elif key == 'kp/':
                keyDo(keys[pygame.key.K_KP_DIVIDE], destination)
            elif key == 'kp*':
                keyDo(keys[pygame.key.K_KP_MULTIPLY], destination)
            elif key == 'kp-':
                keyDo(keys[pygame.key.K_KP_MINUS], destination)
            elif key == 'kp+':
                keyDo(keys[pygame.key.K_KP_PLUS], destination)
            elif key == 'kpEnter':
                keyDo(keys[pygame.key.K_KP_ENTER], destination)
            elif key == 'kp=':
                keyDo(keys[pygame.key.K_KP_EQUALS], destination)
            elif key == 'up':
                keyDo(keys[pygame.key.K_UP], destination)
            elif key == 'down':
                keyDo(keys[pygame.key.K_DOWN], destination)
            elif key == 'right':
                keyDo(keys[pygame.key.K_RIGHT], destination)
            elif key == 'left':
                keyDo(keys[pygame.key.K_LEFT], destination)
            elif key == 'insert':
                keyDo(keys[pygame.key.K_INSERT], destination)
            elif key == 'home':
                keyDo(keys[pygame.key.K_HOME], destination)
            elif key == 'end':
                keyDo(keys[pygame.key.K_END], destination)
            elif key == 'pageup':
                keyDo(keys[pygame.key.K_PAGEUP], destination)
            elif key == 'pagedown':
                keyDo(keys[pygame.key.K_PAGEDOWN], destination)
            elif key == 'f1':
                keyDo(keys[pygame.key.K_F1], destination)
            elif key == 'f2':
                keyDo(keys[pygame.key.K_F2], destination)
            elif key == 'f3':
                keyDo(keys[pygame.key.K_F3], destination)
            elif key == 'f4':
                keyDo(keys[pygame.key.K_F4], destination)
            elif key == 'f5':
                keyDo(keys[pygame.key.K_F5], destination)
            elif key == 'f6':
                keyDo(keys[pygame.key.K_F6], destination)
            elif key == 'f7':
                keyDo(keys[pygame.key.K_F7], destination)
            elif key == 'f8':
                keyDo(keys[pygame.key.K_F8], destination)
            elif key == 'f9':
                keyDo(keys[pygame.key.K_F9], destination)
            elif key == 'f10':
                keyDo(keys[pygame.key.K_F10], destination)
            elif key == 'f11':
                keyDo(keys[pygame.key.K_F11], destination)
            elif key == 'f12':
                keyDo(keys[pygame.key.K_F12], destination)
            elif key == 'f13':
                keyDo(keys[pygame.key.K_F13], destination)
            elif key == 'f14':
                keyDo(keys[pygame.key.K_F14], destination)
            elif key == 'f15':
                keyDo(keys[pygame.key.K_F15], destination)
            elif key == 'numlock':
                keyDo(keys[pygame.key.K_NUMLOCK], destination)
            elif key == 'capslock':
                keyDo(keys[pygame.key.K_CAPSLOCK], destination)
            elif key == 'scrollock':
                keyDo(keys[pygame.key.K_SCROLLOCK], destination)
            elif key == 'rShift':
                keyDo(keys[pygame.key.K_RSHIFT], destination)
            elif key == 'lShift':
                keyDo(keys[pygame.key.K_LSHIFT], destination)
            elif key == 'rCtrl':
                keyDo(keys[pygame.key.K_RCTRL], destination)
            elif key == 'lCtrl':
                keyDo(keys[pygame.key.K_LCTRL], destination)
            elif key == 'rAlt':
                keyDo(keys[pygame.key.K_RALT], destination)
            elif key == 'lAlt':
                keyDo(keys[pygame.key.K_LA], destination)
            elif key == 'rMeta':
                keyDo(keys[pygame.key.K_RMETA], destination)
            elif key == 'lMeta':
                keyDo(keys[pygame.key.K_LMETA], destination)
            elif key == 'rOS':
                keyDo(keys[pygame.key.K_RSUPER], destination)
            elif key == 'lOS':
                keyDo(keys[pygame.key.K_LSUPER], destination)
            elif key == 'mode':
                keyDo(keys[pygame.key.K_MODE], destination)
            elif key == 'help':
                keyDo(keys[pygame.key.K_HELP], destination)
            elif key == 'sysreq':
                keyDo(keys[pygame.key.K_SYSREQ], destination)
            elif key == 'break':
                keyDo(keys[pygame.key.K_BREAK], destination)
            elif key == 'menu':
                keyDo(keys[pygame.key.K_MENU], destination)
            elif key == 'power':
                keyDo(keys[pygame.key.K_POWER], destination)
            elif key == 'euro':
                keyDo(keys[pygame.key.K_EURO], destination)
        elif source == 'textX':
            setMem(destination, textBounds(self.parse(args[2]), self.parse(args[4]))[0] + self.parse(args[3]))
        elif source == 'textY':
            setMem(destination, textBounds(self.parse(args[2]), self.parse(args[4]))[1] + self.parse(args[3]))
        elif source == 'mouseX':
            setMem(destination, render(pygame.mouse.get_pos()[0]))
        elif source == 'mouseX':
            setMem(destination, render(pygame.mouse.get_pos()[1]))
        elif source == 'mousePressed':
            keyDo(pygame.mouse.get_pressed()[0], destination)

        else:
            filePath = f'files/{source}'
            with open(filePath) as file:
                fileContents = file.read()
            if type(getMem(destination)) == dict:
                index = 0
                while fileContents != '':
                    if getMem(str(index) + ':' + destination) == 'empty':
                        setMem(str(index) + ':' + destination, fileContents.split('\n')[-1])
                        fileContents = fileContents.split('\n')[:-1]
                    index += 1
    #ext
    def ext(self, args):
        self.exit = True
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
        elif string[0] == '*':
            if string[1] not in operators:
                return unrender(self.getGlobalMem(string[1:]))
            else:
                if self.parse(string[1:]) in self.memory:
                    return unrender(self.getGlobalMem(string[1:]))
                else:
                    self.setGlobalMem(string[1:], 'empty')
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

    def setGlobalMem(self, location, value):
        global MEMORY
        if ':' not in location:
            reg = location
            if type(value) == dict:
                MEMORY[reg] = value
            else:
                MEMORY[reg][0] = self.parse(value)
        reg = location.split(':')[-1]
        index = int(self.parse(''.join(location.split(':')[:-1])))
        if reg in MEMORY:
            MEMORY[reg][index] = value
        else:
            MEMORY[reg] = {index: value}

    def getGlobalMem(self, location):
        global MEMORY
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
        if reg in MEMORY:
            if index in MEMORY[reg]:
                return MEMORY[reg][index]
            else:
                self.setGlobalMem(location, 'empty')
                return 'empty'
        else:
            self.setGlobalMem(location, 'empty')
            return 'empty'
                
    
    def start(self):
        self.instruction = 0
        self.commands = {
            'ldr': self.ldr,
            'clr': self.clr,
            'mov': self.mov,
            'cpy': self.cpy,
            'add': self.add,
            'sub': self.sub,
            'div': self.div,
            'mul': self.mul,
            'spl': self.spl,
            'cmp': self.cmp,
            'j': self.j,
            'ret': self.ret,
            'exc': self.exc,
            'thr': self.thr,
            'out': self.out,
            'get': self.get,
            'ext': self.ext,
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
        self.exit = False
        while self.instruction < len(self.program):
            self.run()
            if self.exit:
                break
    
    def setMem(self, location, value):
        global DISPLAY
        if ':' not in location:
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
MEMORY = {}
bootProg = prog('files/boot.x', [])
thread = threading.Thread(target=bootProg.start)
thread.start()

displayOn = True
while True:
    for event in pygame.event.get(eventtype=pygame.QUIT):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not displayOn:
        pygame.quit()
        sys.exit()