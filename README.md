# python-VM

A virtual machine that works in python, running it's own version of assembly

Dependencies: `python(3+)` `pygame`

```
=Doc Syntax=
-...: Necesary value
/...: Optional value
*...: More than one value
<...>: Allowed types
'...': Literal

-Types-
<INT>: Integer
<STR>: String
<LITERAL>: Takes value without proccessing
<LITERAL?>: Allows literal

=Syntax=
-Examples-
ldr @4 #5: loads '5' into RAM location 4


-Arithmetic-
GOES LEFT TO RIGHT, NO BEDMAS
ARGS MUST BE <INT>
Prefaced by '['
[@1,+,@2,-,@3,/,@4,*,@5,^,@6: returns ((((@1 + @2) - @3) / @4) * @5) ** @6

-Bracket Operators-
ALL ARGS MUST BE SAME TYPE
<INT>
    +(@1,@2: sums all values
    *(@1,@2: multiplies all values
<STR>
    +(@1,@2: joins all values together with a space between them
    -(@1,@2: concatenates all values together without a space

-Values-
!<INT>: Arguments passed in during execution
@<INT>:<LITERAL>: Memory address and corresponding register
@<LITERAL>: Returns dict of that register
#<INT/!/@>: Integer, if passed a memory address or exec arg returns int version
$<STR/!/@>: String, if passed a memory address or exec arg returns string version
%<LABEL>: Gets value of a label
%: Gets all labels seperated by commas
-Keys-
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


=Memory=
-Storing Values-
empty: no assigned value, defaults to 0 and '' depending on context
#: integer
$: string

-Memory Example-
{
    0: 'empty',
    1: '#2',
    2: '$Hello_World!'
}

=Commands=
-List-
ldr -@location -value: load -value into memory at -location
clr -@location: delete memory value
-Dsp-
    dsp update: update display
    dsp draw rect -brightness -topX -topY -bottomX -bottomY: draw a rect at the given location
    dsp key -@destination -key<LITERAL> -trueValue /falsevalue: if the key[-key] is pressed set -@destination to -trueValue, if not and /falseValue is passed in set -@destination to /falseValue
mov -@destination -@source: move memory at location -source to -destination, sets -source to empty
cpy -@destination -@source: copy memory at location -source to -destination
-Operators-
    add -@destination /source: add to -destination by /source, if /source is not passed in -location is incremented by 1
    sub -@destination /source: subtract -destination by /source, if /source is not passed in -location is decremented by 1
    div -@destination -source: divide -destination by -source
    mul -@destination -source: multiply -destination by -source
lbl -name<LITERAL?>: Add instruction location lbl to be referenced later (Using % prefix). Stores the current line executing as a value, and -name as a key
spl -@destination -string<STR> -index<INT>: sets -@destination to -string[-index]
cmp *values: load *values for a jcondition, <STR> values are loaded as their length
jmp -location: Go to -location in the current executing program
-jcondition-
    je -location: Jump when previous cmp is equal
    jne -location: Jump when previous cmp is not equal
    jg -location: Jump when previous cmp is greater
    jge -location: Jump when previous cmp is greater or equal
    jl -location: Jump when previous cmp is less
    jle -location: Jump when previous cmp is less or equal
    jdv -location: Jump when previous cmp is divisible (1st arg divisible by 2nd arg)

-File And Terminal-
    exc -file<LITERAL?> *args: execute -file and pass in *args
    thr -file<LITERAL?> *args: execute -file and pass in *args on a new thread
    out -destination -source: if -source is 'term' print -source to the python console, if -source is '@' print memory, else append to file -destination
    get -@destination -source<LITERAL?>: set -@destination to the value of the file -source, if -source is 'term' get user input CANNOT USE # IN USER INPUT
    set -destination -source<LITERAL?>: set the file -destination to -source

-Comments-
    Comment line is preceded by '>'
```
