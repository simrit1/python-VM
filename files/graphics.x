out term +(Graphics,Boot,Loop,Started
ldr @0:AA #0
lbl bootLoop
    out dispRect #0 #0 @-2:DISP @-1:DISP @0:AA
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
    out dispText +(Brightness:,$@0:RES #0 #0 #12 @0:TXTBRT
    get @0:textY textY +(Brightness:,$@0:RES #0 #12
    out dispText +(To,close,window,press,'esc' #0 @0:textY #12 @0:TXTBRT
    out disp
    get @0:KEY keys esc
    cmp @0:KEY $True
    j ne %notExit
    ldr *0:ESC $True
    out dispRect #0 #0 @-2:DISP @-1:DISP #0
    out disp
    out term +(Exited,Graphics,Boot,Loop
    out dispClose
    ext
    lbl notExit
j mp %bootLoop