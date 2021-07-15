ldr @0:AA #0
ldr @1:AA #1
ldr @2:AA #0
ldr @3:AA #10
cmp !0 $boot
je %end
out term +(Enter,Iteration,Max:
get @3:AA term
ldr @3:AA #@3:AA
lbl end
out term @1
lbl loop
add @2:AA
ldr @-1:AA @1:AA
ldr @1:AA [@0:AA,+,@1:AA
ldr @0:AA @-1:AA
out term @1:AA
cmp @2:AA @3:AA
jle %loop
out term +(Prog,Complete