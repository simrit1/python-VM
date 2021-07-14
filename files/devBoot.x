out term +(Entered,DevMode
out term +(Enter,'Exit',To,Complete,Proccess
lbl loop
out term +(Enter,filename:
get @0 term
cmp @0 $Exit
je %end
exc @0 $boot
jmp %loop
lbl end
out term +(Proccess,Complete