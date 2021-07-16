out term +(Graphics,Boot,Loop,Started
ldr @0:AA #0
ldr @1:AA #240
lbl bootLoop
    dsp draw rect #0 #0 @-2:DISP @-1:DISP #0
    dsp draw rect @1:AA @1:AA [@-2:DISP,-,@1:AA,-,@1:AA [@-1:DISP,-,@1:AA,-,@1:AA @0:AA
    add @0:AA #1
    dsp update
    dsp key @0:KEY esc #1 #0
    cmp @0:KEY #1
    je %exit
jmp %bootLoop
lbl exit
out term +(Exited,Graphics,Boot,Loop