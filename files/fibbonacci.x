ldr @0 #0
ldr @1 #1
ldr @2 #0
ldr @3 #10
cmp !0 $boot
je %end
out term +(Enter,Iteration,Max:
get @3 term
ldr @3 #@3
lbl end
out term @1
lbl loop
add @2
ldr @-1 @1
ldr @1 [@0,+,@1
ldr @0 @-1
out term @1
cmp @2 @3
jle %loop
out term +(Prog,Complete