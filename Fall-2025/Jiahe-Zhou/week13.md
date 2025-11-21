# Week 13
- State: Finished and not encountering any obstacle.
- About this: Summary of week 13

## Compiler Meeting 11/15, Saturday
- Fill poster content
- Decide presentation order

## GPU Meeting 11/16, Sunday
- Complete predications
- Finalize content of final design review
- Print the compiler poster for Research Expo

## Compiler Meeting 11/17, Monday
- How to evaluate a compiler?
  - Not sure if compiler can be evaluated, or use instr/program
- Should next steps cover the whole next semester?
  - Cover packetization, branch target, linker, emulator
- Where is location for wensday presentation?
  - MSEE Rice Design Studio

## Fall Research Expo 11/18, Tuesday
- Most of judges are not CmpE major
  - We need to explain our compiler in a easier way
- A judge said our compiler is a great work

## Final Design Review 11/19, Wednesday
- Presenting Proposal, PPCI, frontend&backend, and Preprocessor
- Which languages does PPCI support?
  - Frontend: Python, Java, etc.
  - Backend: x86_64, arm, etc.
- sizeof is not a system call, and we should implement it
- We cannot do malloc() because of no memory on GPU

## Compiler
- Issue: Assembler cannot merge into PPCI right now
  - Predications are generated in IR level
  - Need to insert predication nodes
  - Didn't figure out how to do it
- Bug: float (float)3.14/2; need to be casted
  - Because default is 64 bits floating points
  - Try to set default to 32 bits
- Bug: not support for B-type for floating point yet
  - Assume all comparisions are integers right now
  - instruction.py needs to be updated for this

## Goal for Week 13
- Dig in packetization implementation
