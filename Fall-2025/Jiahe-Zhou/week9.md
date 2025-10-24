# Week 9
- State: Finished and not encountering any obstacle.
- About this: Summary of week 9

## GPU Meeting 10/19, Sunday
```c
foo()
{
  bar()     pred1
  if
    bar()   pred2
  else
    bar()   pred3
}

bar()       pred4(fixed)
{
  ···
}
```
- for multiple function calls, pred number might vary
- but inside the called function, it has fixed pred number
- predication masks cannot be hardcoded in the assembly
- masks should be changed for different pred
  - changing masks will overwrite masks
  - use stack in software to restore mask overwritten
    - software controlled stack is easier
    - hardware controlled stack might have to spill to memory at the end
- to reduce function calls, inline functions to optimize and avoid jalr

## Compiler Meeting 10/20, Monday
- PC is the same for all threads in the warp
- different PC in different threads is a disaster
- for brnach/jump instruction
  - have predication mask: 100···0
  - ensure only one thread yields correct PC
  - otherwise, PC will conflict -> cannot determine next PC

## Compiler Chat 10/21, Tuesday
- Floating points comparison
  - we don't have it right now
  - not sure if graphics need it

## General Meeting 10/23, Thursday
Simple Problems require simple solutions
- systolic array
- GPU Register Files
  - 3 banks for 2 operands and 1 output
  - too many wires: 16K wires
  - issue 1 new instruction every cycle: 2K wires

## Compiler thoughts
- Compiler 468: RISC-V compare floating points by using FEQ, FLT, FLE with BEQ, BNE
  - FEQ rd, rs1, rs2 (rd=(rs1==rs2) ? 1 : 0)
  - BEQ rd, x0, dest
- Use instructions like RISC-V or subtract 2 floating points

## Goal for Week 9
- minimize Twig
- define folder path structure
- improve assembler
