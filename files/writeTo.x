ldr @0:AA $
out term +(Enter,'Exit',To,Exit
exc doc.x !0
lbl loop

get @0:AA term

cmp @0:AA Exit
je %exit

out !0:AA @0

jmp %loop
lbl exit
out term +(Exited,WriteTo,Call