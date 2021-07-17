ldr @0:AA $
out term +(Enter,'Exit',To,Exit
exc doc.x !0
lbl loop

get @0:AA term

cmp @0:AA Exit
j e %exit

out !0 @0:AA

j mp %loop
lbl exit