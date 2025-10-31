# Week 10
- State: Finished and not encountering any obstacle.
- About this: Summary of week 10

## GPU Meeting 10/26, Sunday
### Pred Table and Reconvergence point
<img width="4000" height="2252" alt="image" src="https://github.com/user-attachments/assets/5095beff-cbeb-415e-8fab-4d13d69bd5aa" />

- How to find reconvergence point
  - Need an algorithm for this
  - If (next_blknum\<current_blknum) jump to block where pred was altered
- Need more verification for this algorithm

### Access Warps and Threads
<img width="2252" height="4000" alt="image" src="https://github.com/user-attachments/assets/2f967f58-81ef-42d9-8855-303afdffcf45" />

- Stack will run on RAM
- To access a thread
- stackStart - warpId * stackSize + threadId * 4
  - stackStart will be given
  - stackSize = warpSize
- warpId = globalId / 32
- threadId = globalId % 32

### Twig
- Try to delete unecessary files in directories
- Still need to debug and implement the call path for IR
  - ISA definition is not completed

## Compiler Meeting 10/27, Monday
- How IR generator in Twig work
- How to change the IR generator for our architecture
- Especially for AST to IR conversion

## Compiler Chat 10/21, Tuesday
- Floating points comparison
  - We don't have it right now
  - Not sure if graphics need it

## Compiler thoughts
- To analyze control flow, we can find a graphic tool to generate control flow
- In ECE468 Compiler, basic blocks are defined as:
  - Find leaders in assembly
  - 1st command is a leader
  - If branch, branch target and next command are leaders
  - If jump, jump target is leader
  - Basic blocks start from leader and end before next leader
- Maybe we could use these definitions to analyze predicate mask, reconvergence points, and control flow

## Goal for Week 10
- Define a general memory behavior for graphics and hardware teams
  - Endianess
  - csrs
- Keep Minimize Twig
- Define folder path structure
- Improve assembler
- Merge assembler to twig if possible
