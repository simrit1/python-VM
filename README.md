# python-VM

A virtual machine that works in python, running it's own version of assembly (likely a very bad version)

##### Dependencies:`python(3+)` `pygame`

---

## Values

#### !

`!name`: returns value of the label `name` labels can be made using the Lbl command

#### @

`@index:reg`: returns the value of the memory address at `self.memory[reg][index]`, `reg` is a string and `index` is an integer. This was an attempt at adding registers to increase functionality but was an incorrect implementation and should not use the term register

#### \#

`#int`: returns an integer of value `int` can be negative

#### $

`$string`: returns a strig of value `string`

---

## Commands

## Ldr

`ldr location value`: loads `value` into `location`

`location` must be a memory address

<br>

## Clr

`clr location`: removes the value at `location`

`location` must be memory address

<br>

## Dsp

- `dsp update`: updates screen
- `dsp draw rect brightness leftX topY rightX bottomY`: draws a rectangle on the screen with `brightness` and given position arguments `leftX`, `topY`, `rightX`, `bottomY`
- `dsp draw text brightness text leftX topY size`: draws `text` with the font size `size` and the given brightness `brightness`, the top left being at `leftX`, `topY`
- `dsp getx text destination text leftX size`: sets the memory at `destination` to the rightX bound of the given text arguments

    `desination` must be a memory address

    This command is not currently implemented
    
- `dsp gety text destination text topY size`: sets the memory at `destination` to the bottomY bound of the given text arguments

    `desination` must be a memory address

    This command is not currently implemented

- `dsp key destination key trueValue falseValue`: if the key `key` is currently being pressed it sets the memory address `destination` to `trueValue`, if not and `falseValue` is passed in it sets the memory address `destination` to `falseValue`

    `falseValue` is an optional argument
    
    `destination` must be a memory address
    
    Documentation for available `key` values can be found in the lower part of this readme

<br>

## Mov

`mov destination source`: moves the memory from `source` to `destination`, leaves `source` as `'empty'`

`destination` and `source` must be memory addresses

<br>

## Cpy

`cpy destination source`: copies the memory from `source` to `destination`

`destination` and `source` must be memory addresses

<br>

## Add

`add destination value`: adds `value` to the memory at `destination`

`destination` must be a memory address

if both `value` and the memory at `destination` are strings `value` will be concatenated onto the memory at `destination`

`value` is optional when the memory at `destination` is an integer, in that case when `value` is not passed in the memory at `destination` will be incremented by `1`

<br>

## Sub

`sub destination value`: subtracts `value` from the memory at `destination`

`destination` must be a memory address

`value` is optional, when `value` is not passed in the memory at `destination` will be decremented by `1`

<br>

## Div

`div destination value`: divides the memory at `destination` by `value`

`destination` must be a memory address

<br>

## Mul

`mul destination value`: multiplies the memory at `destination` by `value`

`destination` must be a memory address

<br>

## Lbl

`lbl name`: stores the line the command is on to be reffered to later by `%name`

Runs once `prog.start()` is called inside main.py

<br>

## Spl

`spl destination string index`: sets the memory at `destination` to `string[index]`

For non-python people: `spl destination $abc #0` will set the memory at `destination` to `a`

`destination` must be a memory address

<br>

## Cmp

`cmp valueOne valueTwo`: stores `valueOne` and `valueTwo` for a j condition cmd later in the code

<br>

## Jmp

`jmp line`: jumps to `line`, `line` is intended to be a label but is parsed and can take in non label values

<br>

## J Conditions

- `je line`: jump to `line` if previous cmp is equal
- `jne line`: jump to `line` if previous cmp is not equal
- `jg line`: jump to `line` if the previous cmp is greater
- `jge line`: jump to `line` if the previous cmp is greater or equal
- `jl line`: jump to `line` if the previous cmp is less
- `jle line`: jump to `line` if the previous cmp is less or equal
- `jdv line`: jump to `line` if the previous cmp is divisible

<br>

## Exc

`exc file arg1 arg2 arg3...`: Runs the file `file` passing in all arguments in the same proccess as the program that called this command

<br>

## Thr

`thr file arg1 arg2 arg3...`: Does the same as Exc but in a different proccess

<br>

## Out

`out destination value`: appends `value` to file `destination`

`value` must be string

If `destination` is `term` then print `value` to the python console, if `value` is `@` print self.memory to the python console

<br>

## Get

`get destination source`: sets the memory at `destination` to the contents of the file `source`

`destination` must be a memory address

If `source` is `term` set the memory at `destination` to user input from the python console

<br>

## Set

`set destination value`: sets the file `destination` to `value`

<br>

## Comments

A comment is prefaced by `>`

<br>

## Keys

A list of key arguments with their corresponding pygame values

```
K_BACKSPACE: backspace
K_TAB: tab
K_CLEAR: clear
K_RETURN: return
K_PAUSE: pause
K_ESCAPE: esc
K_SPACE: space
K_EXCLAIM: !
K_QUOTEDBL: "
K_HASH: #
K_DOLLAR: $
K_AMPERSAND: &
K_QUOTE: ' (might not be right)
K_LEFTPAREN: (
K_RIGHTPAREN: )
K_ASTERIX: *
K_PLUS: +
K_COMMA: ,
K_MINUS: -
K_PERIOD: .
K_SLASH: /
K_0: 0
K_1: 1
K_2: 2
K_3: 3
K_4: 4
K_5: 5
K_6: 6
K_7: 7
K_8: 8
K_9: 9
K_COLON: :
K_SEMICOLON: ;
K_LESS: <
K_EQUALS: =
K_GREATER: >
K_QUESTION: ?
K_AT: @
K_LEFTBRACKET: [
K_BACKSLASH: \
K_RIGHTBRACKET: ]
K_CARET: ^
K_UNDERSCORE: _
K_BACKQUOTE: `
K_a: a
K_b: b
K_c: c
K_d: d
K_e: e
K_f: f
K_g: g
K_h: h
K_i: i
K_j: j
K_k: k
K_l: l
K_m: m
K_n: n
K_o: o
K_p: p
K_q: q
K_r: r
K_s: s
K_t: t
K_u: u
K_v: v
K_w: w
K_x: x
K_y: y
K_z: z
K_DELETE: del
K_KP0: kp0
K_KP1: kp1
K_KP2: kp2
K_KP3: kp3
K_KP4: kp4
K_KP5: kp5
K_KP6: kp6
K_KP7: kp7
K_KP8: kp8
K_KP9: kp9
K_KP_PERIOD: kp.
K_KP_DIVIDE: kp/
K_KP_MULTIPLY: kp*
K_KP_MINUS: kp-
K_KP_PLUS: kp+
K_KP_ENTER: kpEnter
K_KP_EQUALS: kp=
K_UP: up
K_DOWN: down
K_RIGHT: right
K_LEFT: left
K_INSERT: insert
K_HOME: home
K_END: end
K_PAGEUP: pageup
K_PAGEDOWN: pagedown
K_F1: f1
K_F2: f2
K_F3: f3
K_F4: f4
K_F5: f5
K_F6: f6
K_F7: f7
K_F8: f8
K_F9: f9
K_F10: f10
K_F11: f11
K_F12: f12
K_F13: f13
K_F14: f14
K_F15: f15
K_NUMLOCK: numlock
K_CAPSLOCK: capslock
K_SCROLLOCK: scrollock
K_RSHIFT: rShift
K_LSHIFT: lShift
K_RCTRL: rCtrl
K_LCTRL: lCtrl
K_RALT: rAlt
K_LALT: lAlt
K_RMETA: rMeta
K_LMETA: lMeta
K_RSUPER: rOS
K_LSUPER: lOS
K_MODE: mode
K_HELP: help
K_SYSREQ: sysreq
K_BREAK: break
K_MENU: menu
K_POWER: power
K_EURO: euro
```
