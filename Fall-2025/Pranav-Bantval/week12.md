# Week 12

State: making progress implementing predication

Progress: implemented branch types

implemented branch types and predicate stack (merged teammates work of predicate stack into the twig arch work I did). I did bjmp for basic if/else statements. Teammate did while loop (pjmp and sjmp) for jpnz and single predicate use.

What's left?

incorporate parent predicate parameter into every instruction (node)

confirm relocation works for jal (pc = pc + imm but it shows as jal, x0, pc+imm).

packetize
