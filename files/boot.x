lbl mainLoop

    > load user input into @0
    get @0 term

    > One-word command checks
    > Help
    cmp @0 $Help
    jne %cmdNotHelp
        exc doc.x help.doc
    lbl cmdNotHelp

    > DevMode
    cmp @0 $DevMode
    jne %cmdNotDevMode
        exc devBoot.x
    lbl cmdNotDevMode

    > init for command seperation
    > clear memory up to @5
    > @-1 current iteration
    > @-2 max iteration
    ldr @-1 #1
    ldr @-2 #5
    lbl clearMem
        ldr @@-1 $
        add @-1
    cmp @-1 @-2
    jle %clearMem

    > if empty command skip
    cmp @0 #0
    je %skip
        > @0 input
        > @-1 current index
        > @-2 item
        > @-3 last word
        > @-4 current word index
        > @-5 space

        > init @-5 as ' '
        ldr @-5 +(,
        spl @-5 @-5 #0

        ldr @-1 #1
        spl @-3 @0 #0
        ldr @-4 #1
        lbl cmdSep
            > set @-2 to the current char
            spl @-2 @0 @-1
            > if current char is a space
            cmp @-2 @-5
            jne %crntChrNotSpace
                ldr @@-4 @-3
                add @-4
                add @-1
                spl @-3 @0 @-1
                jmp %crntChrWasSpace
            lbl crntChrNotSpace
            > add current char to @-3
            add @-3 @-2
            lbl crntChrWasSpace
            > increment current index
            add @-1
        cmp @-1 @0
        jl %cmdSep
        ldr @@-4 @-3
    lbl skip
jmp %mainLoop