out term +(Graphics,Boot,Loop,Started
ldr @0:AA #0
ldr @0:PRS $False
ldr @0:VALID $True
ldr @0:SIZE #22
lbl bootLoop
    get @0:MOUSE mousePressed
    out dispRect #0 #0 @-2:DISP @-1:DISP #0
    cmp @0:MOUSE $True
    get @0:textPos textX $@0:AA #0 @0:SIZE
    mul @0:textPos #-1
    add @0:textPos @-2:DISP
    div @0:textPos #2
    out dispText $@0:AA @0:textPos #10 @0:SIZE #254
    j ne %mouseNotPressed
        out dispRect #225 #225 [@-2:DISP,-,#425 [@-1:DISP,-,#425 #254
        cmp @0:VALID $True
        j ne %mousePressedLastFrame
            add @0:AA
            ldr @0:VALID False
        lbl mousePressedLastFrame
    lbl mouseNotPressed
    get *0:ESC keys esc
    get @0:PRS mousePressed
    cmp @0:PRS $True
    j e %theThing
    ldr @0:VALID $True
    lbl theThing
    cmp *0:EXIT $True
    j ne %notExit
        j mp %end
    lbl notExit
    out disp
j mp %bootLoop
lbl end
out dispClose