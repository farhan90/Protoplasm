.text
jal main 
li $v0 10
syscall
main:
subu $sp,$sp,4
sw $ra 0($sp)
Label2 : li $s6, 10
Label3 : move $t8, $s6
Label4 : li $s5, 3
Label5 : li $s4 4
mult $s4 $s5
mflo $s4
move $a0, $s4
li $v0, 9
Syscall
move $t3, $v0
Label6 : li $s3, 2
Label7 : li $s2 4
mult $s2 $s3
mflo $s2
move $a0, $s2
li $v0, 9
Syscall
move $t0, $v0
Label8 : li $s1, 0
Label9 : add $s1,$s1,$s1
add $s1,$s1,$s1
add $s0, $s1 $t3 
Label10 : li $a2, 4
Label11 : sw $a2 0($s0)
Label12 : li $t4, 1
Label13 : add $t4,$t4,$t4
add $t4,$t4,$t4
add $a3, $t4 $t0 
Label14 : li $t6, 0
Label15 : add $t6,$t6,$t6
add $t6,$t6,$t6
add $v1, $t6 $t3 
lw $t5 0($v1)
Label16 : sw $t5 0($a3)
Label17 : li $t1, 2
Label18 : add $t1,$t1,$t1
add $t1,$t1,$t1
add $t7, $t1 $t0 
Label19 : sw $t8 0($t7)
Label20 : li $t2, 1
Label21 : add $t2,$t2,$t2
add $t2,$t2,$t2
add $v1, $t2 $t0 
lw $a0 0($v1)
Label22 : li $v0 1
move $a0, $a0
syscall
Label23 : li $v0 1
move $a0, $t8
syscall
Label24 : li $t9, 2
Label25 : add $t9,$t9,$t9
add $t9,$t9,$t9
add $v1, $t9 $t0 
lw $a1 0($v1)
Label26 : li $v0 1
move $a0, $a1
syscall
Label27 : lw $ra 0($sp)
addu $sp,$sp,4
jr $ra
