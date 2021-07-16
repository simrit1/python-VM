thr graphics.x boot
out term +(Boot,Complete
out term +(Enter,'Help',To,Get,A,List,Of,Commands
out term ====================

lbl mainLoop

    > load user input into @0:AA
    get @0:AA term

    > One-word command checks
    > Help
    cmp @0:AA $Help
    jne %cmdNotHelp
        exc doc.x help.doc
        out term ====================
    lbl cmdNotHelp

    > DevMode
    cmp @0:AA $DevMode
    jne %cmdNotDevMode
        exc devBoot.x
        out term ====================
    lbl cmdNotDevMode

    > Mem
    cmp @0:AA $Mem
    jne %cmdNotMem
        out term @
    lbl cmdNotMem

    > Exit
    cmp @0:AA $Exit
    je %end

    > init for command seperation
    > clear memory up to @5:AA
    > @-1:AA current iteration
    > @-2:AA max iteration
    ldr @-1:AA #1
    ldr @-2:AA #5
    lbl clearMem
        clr @@-1:AA:AA
        add @-1:AA
    cmp @-1:AA @-2:AA
    jle %clearMem

    > if empty command skip
    cmp @0:AA #2
    jle %skip
        > @0:AA input
        > @-1:AA current index
        > @-2:AA item
        > @-3:AA last word
        > @-5:AA space

        > init @-5:AA as ' '
        ldr @-5:AA +(,
        spl @-5:AA @-5:AA #0

        ldr @-1:AA #1
        spl @-3:AA @0:AA #0
        lbl cmdSep
            > set @-2:AA to the current char
            spl @-2:AA @0:AA @-1:AA
            > if current char is a space
            cmp @-2:AA @-5:AA
            jne %crntChrNotSpace
                add @AA @-3:AA
                add @-1:AA
                spl @-3:AA @0:AA @-1:AA
                jmp %crntChrWasSpace
            lbl crntChrNotSpace
            > add current char to @-3:AA
            add @-3:AA @-2:AA
            lbl crntChrWasSpace
            > increment current index
            add @-1:AA
        cmp @-1:AA @0:AA
        jl %cmdSep
        add @AA @-3:AA

    > Run
    cmp @1:AA $Run
    jne %cmdNotRun
        > allows 3 params
        exc @2:AA @3:AA @4:AA @5:AA
        out term ====================
    lbl cmdNotRun

    > Start
    cmp @1:AA $Start
    jne %cmdNotStart
        > allows 3 params
        thr @2:AA @3:AA @4:AA @5:AA
        out term ====================
    lbl cmdNotStart

    > Print
    cmp @1:AA $Print
    jne %cmdNotPrint
        exc doc.x @2:AA
        out term ====================
    lbl cmdNotPrint

    > WriteTo
    cmp @1:AA $WriteTo
    jne %cmdNotWrite
        exc writeTo.x @2:AA
        out term ====================
    lbl cmdNotWrite

    lbl skip
jmp %mainLoop
lbl end