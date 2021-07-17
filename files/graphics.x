out term +(Graphics,Boot,Loop,Started
ldr @0:AA #0
lbl bootLoop
    dsp draw rect #0 #0 @-2:DISP @-1:DISP @0:AA
    add @0:AA
    ldr @0:BRT @0:AA
    div @0:BRT #255
    mul @0:BRT #255
    ldr @0:RES [@0:AA,-,@0:BRT
    ldr @0:TXTBRT #255
    > if @0:RES > 127
    cmp @0:RES #127
    j le %notTrue
    ldr @0:TXTBRT #0
    lbl notTrue
    dsp draw text @0:TXTBRT +(Brightness:,$@0:RES #0 #0 #12
    dsp update
    dsp key @0:KEY esc #1 #0
    cmp @0:KEY #1
    j e %exit
j mp %bootLoop
lbl exit
dsp draw rect #0 #0 @-2:DISP @-1:DISP #0
dsp update
out term +(Exited,Graphics,Boot,Loop