out term +(Entered,DevMode
out term +(Enter,'Exit',To,Complete,Proccess
lbl loop
out term +(Enter,filename:
get @0:AA term
cmp @0:AA $Exit
je %end
exc @0:AA $boot
jmp %loop
lbl end
out term +(Proccess,Complete