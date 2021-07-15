import threading

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
            return self.memory[location]
        reg = location.split(':')[-1]
        index = int(self.parse(':'.join(location.split(':')[:-1])))
        if reg in self.memory:
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
                reg = string[1:].split(':')[-1]
                index = int(self.parse(':'.join(string[1:].split(':')[:-1])))
                if reg in self.memory:
                    if index in self.memory[reg]:
                        return unrender(self.getMem(string[1:]))
                    else:
                        self.setMem(string[1:], 'empty')
                else:
                    self.setMem(string[1:], 'empty')
                    return 'empty'
            else:
                if self.parse(string[1:]) in self.memory:
                    return self.getMem(string[1:])
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
        reg = location.split(':')[-1]
        index = int(self.parse(''.join(location.split(':')[:-1])))
        if reg in self.memory:
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

        if line == '':
            self.instruction += 1
            return

        # print(f'{self.fileName}>{self.instruction+1}>{line}')

        #ldr
        if cmd == 'ldr':
            if args[0][0] != '@':
                raise TypeError(f'@{self.instruction}: {self.fileName}>ldr: {args[0]} is not a memory address')
            location = args[0]
            index = self.parse(':'.join(location.split(':')[:-1])[1:])
            reg = location.split(':')[-1]
            value = render(self.parse(args[1]))
            self.setMem(':'.join([str(index), reg]), value)
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
                excArgs += self.parse(argument)
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
bootProg.start()