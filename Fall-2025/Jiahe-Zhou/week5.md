# Week 5
- State: Finished and not encountering any obstacle.
- About this: 

## GPU Meeting 9/21, Sunday
48 bits definition for instruction in ISA
- 7: opcode
- 6: rd
- 6: r1
- 6: r2
- 4: mask
- 5: control
  - 1: packet start
  - 1: packet depedency
  - 3: register file cache for rd, r1, and r2
- 3: location
- 11: imm

Hardware
- 32 areas per kernel
- 64 registers per threads
- 1024 threads max per threadblock
  - Arbitary number of threadblocks per kernel

Bits usage
- Use mask to determine usable threads for branch
  - mask bits -> find predicate reg id -> get mask
    - 4 bits to maintain 16 predicate register id in predicate table
    - Predicate table for each warp
    - Each predicate register has 32 bits masking
  - example: if {add} else {sub}
    - add: 0011000011001111
    - sub: 1100111100110000
      - masking for else will be negation of if
- Use control + location to indicate which register should be cached, and which entry it belongs to.
  - register file cache has 6 entries
  - Problem: cache eviction
  - Solve: first 8 registers will be cached(reg0~reg7)

## Compiler Meeting 9/22, Monday
Problems need to solve
- Threads ID: software needs this (To assign data after computing)
- Kernel
- Register File Cache

GPU block is arbitrary, and will be assigned by software

## SoCET Project Presentation 9/22, Monday
Feedback
- Name our compiler
  - Do not call it CUDA
- Add packages on timeline

## Personal Thought on PPCI 9/25, Thursday

### Features of PPCI
<img width="617" height="653" alt="image" src="https://github.com/user-attachments/assets/5b7b843a-b911-4f5a-b287-a412bb7023aa" />

Use add_instruction() to add ISA instructions.

Can separate different type of ISA and merge them by '+' operator
e.g.
```python
    from ppci.arch.data_instructions import data_isa
    my_complete_isa = my_isa + data_isa
 ```

### could be done in the future
- Help command like `GPUasm -h`, list all supported commands and instructions
- Need a test program for GPUasm to check compiling correctness (Like 437)
  - Don't know how to test our compiler so far
- Use dependency to change the order of GPUasm execution, preventing hazards like using `nop`

## Goal for Week 5
- Compile C language first
  - Figure out how AI hardware compile their ISA
  - Change frontend for new instructions/functions
    - Needs to update lexer/parser to recognize specific token
  - Replace backend with our ISA
    - Do simple test first
  - Compare the differences with C asm file
  - Reuse same C asm logic if possible
- Check what instructions/functions need to be added in C frontend
  - which kinds of special syntaxs will be used
  - <<<>>> for kernel
- More reading on the book
