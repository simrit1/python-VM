# python-VM
A virtual machine that works in python, running it's own version of assembly
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
@<INT>: Memory address
#<INT/!/@>: Integer, if passed a memory address or exec arg returns int version
$<STR/!/@>: String, if passed a memory address or exec arg returns string version
%<LABEL>: Gets value of a label
%: Gets all labels seperated by commas

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
