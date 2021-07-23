# python-VM

A virtual machine that works in python, running it's own version of assembly (a very bad version)

##### Dependencies:`python(3+)` `pygame`

<br>

---

## Examples

#### Fibbonacci Sequence

```
ldr @0:AA #0
ldr @1:AA #1
ldr @2:AA #0
ldr @3:AA #10
cmp !0 $boot
j e %end
out term +(Enter,Iteration,Max:
get @3:AA term
ldr @3:AA #@3:AA
lbl end
out term @1
lbl loop
add @2:AA
ldr @-1:AA @1:AA
ldr @1:AA [@0:AA,+,@1:AA
ldr @0:AA @-1:AA
out term @1:AA
cmp @2:AA @3:AA
j le %loop
out term +(Prog,Complete
```

#### Hello World!

```
out term +(Hello,World!
```

---

## Values

#### !

`!name`: returns value of the label `name` labels can be made using the Lbl command

#### @

`@index:reg`: returns the value of the memory address at `self.memory[reg][index]`, `reg` is a string and `index` is an integer

#### *

`*index:reg`: a central memory address, one program changing this value will change for all programs

#### \#

`#int`: returns an integer of value `int`. Can be negative

#### $

`$string`: returns a strig of value `string`

---

## Arithmetic

#### [`value`,`op`,`value`

Using `[` allows you to make statements like `[#1,+,#1` (which returns `2`)

`[` takes in comma seperated values and every odd value is an operator: `[val,op,val,op,val,op`

Supported operators are: `+` `-` `/` `*` `^`

Operators take place ___LEFT TO RIGHT___, `[#1,+,#2,*,#3` returns `9`

<br>

#### `op`(`value`,`value`

Comma seperated values

##### `+(` String & Int

Integer: Sums all values

String: Joins all strings with `' '`

##### `-(` String

Joins all strings without any joining character

##### `*(` Int
Multiplies all integers together

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

## J Conditions

- `j mp line`: jump to `line`
- `j e line`: jump to `line` if previous cmp is equal
- `j ne line`: jump to `line` if previous cmp is not equal
- `j g line`: jump to `line` if the previous cmp is greater
- `j ge line`: jump to `line` if the previous cmp is greater or equal
- `j l line`: jump to `line` if the previous cmp is less
- `j le line`: jump to `line` if the previous cmp is less or equal
- `j dv line`: jump to `line` if the previous cmp is divisible

<br>

## Ret

`ret value`: returns `value` to the upper Exc call

<br>

## Exc

`exc file arg1 arg2 arg3...`: Runs the file `file` passing in all arguments in the same thread as the program that called this command (halts till program is finished)

### Driver Arguments
- `exc 'return' destination file arg1 arg2 arg3...`: sets the memory at the memory location `destination` to the return value of the program

<br>

## Thr

`thr file arg1 arg2 arg3...`: Starts file with the passed in arguments in a different thread (call doesn't halt)

<br>

## Out

`out destination value`: appends `value` to file `destination`

`value` must be string

### Driver Arguments

- `out 'term' value`: prints `value` to the python console
- Display
    - `out 'dispRect' x1 y1 x2 y2 brightness`: draws a rectangle at `(x1, y1), (x2, y2)` with the brightness `brightness`
    - `out 'dispText' text x y size brightness`: draws text at `x, y` with size `size`, the brightness `brightness`, and the size `size`

<br>

## Get

`get destination source`: sets the memory at `destination` to the contents of the file `source`

If `destination` is a register, all empty memory addresses in that register from 0 onwards will be set to each line of the given file

`destination` must be a memory address

If `source` is `term` set the memory at `destination` to user input from the python console

### Driver Arguments

- `get destination 'keys' key`: if the key `key` is currently being pressed down it sets the memory at `destination` to `$True` or `$False` accordingly
- Text
    - `get destination 'textX' text x size`: returns the x bound (the x location of the right side of the text) of a given text argument
    - `get destination 'textY' text y size`: returns the y bound (the y location of the bottom of the text) of a given text argument

<br>

## Ext

`ext`: exits the current program

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
