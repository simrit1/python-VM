ldr @0 $
out term +(Enter,'Exit',To,Exit
exc doc.x !0
lbl loop

get @0 term

cmp @0 Exit
je %exit

out !0 @0

jmp %loop
lbl exit
out term +(Exited,WriteTo,Call