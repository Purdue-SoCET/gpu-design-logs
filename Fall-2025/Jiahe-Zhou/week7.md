# Week 7
- State: Finished and not encountering any obstacle.
- About this: Summary of week 7

## GPU Meeting 10/5, Sunday
### Finished our design review
Software Questions
- registers needed
  - CSRs✅
  - threadId✅
  - blockId
  - blockDim

Compiler Questions
- Can we handle if graphics team takes OpenGL
- predication for nested if-else statement
- packetization

## Compiler Meeting 10/6, Monday
- How to test our compiler
  - unit test for specific funtionalities
- Consider about `sizeof`, it's a system operator not a function
  - maybe need system call
- Pratical CPU & GPU communication
  - CPU and GPU connect to DRAM and communicate via DRAM.
  - CPU starts with sending GPU a doorbell instruction
  - GPU ends with sending CPU another doorbell instruction.
- In our design, focus on GPU only
  - Have a kernel starting method but don't have to use it
  - Use testbench to send doorbell instructions
  - Need to define 2 distinct doorbell instructions for CPU and GPU to start/end the kernel

## Misc
modulo opertator(%)
- typically needs 2+ instructions to compute the result
- check with graphics team that thay won't heavily use modulo
- calculate modulo with 3 instructions
  - `div` to get integer quotient
  - `mul` divisor and quotient
  - `sub` the result from mul to get remainder

## Goal for Week 7
- Figure out how to add customized function to PPCI
- Finalize ISA Green Card and check instrcutions
- Talk to graphics team with OpenGL
- Discuss more about predication and packetization
