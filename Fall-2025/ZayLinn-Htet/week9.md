# Week 9 Design Log
## 10/17/25 - 10/23/25
I am not currently stuck or blocked

## Sunday (10/19/25) - GPU Weekly Meeting
- Started looking through Pure Python Compiler Infrastructure files and how to dig deep through them
- Looked through the assembler Pranav has created for our ISA (Assembly to Binary Code encoder)

Teal Card
- Updated I-Type by shifting around opcode of some instructions
- Added new instruction type called "F Type", known as the function type for special instructions like float to int, int to float, sin/cos, invsqrt
- Informed hardware about update, should implement a better updating system soon

Graphics Interrogation
- Received a bunch of questions from graphics to answer
- Having a special keyword to denote our custom-functions would definitely make it easier during the preprocessing stage of the compiler
- For anything that'd use general C code (for loops, if-else, cases, etc...), do it usually the way you do in C
- Anything that'd be call from libraries (math, quicksort) should be manually written by them
- Regarding printf, that'd be a discussion that'll need to be done with hardware
- Different files linking will be done automatically by PPCI's preprocessor
- Packet dependency tracking should already done by our work

Special Nested For Loop Case Dillehma
- If there is a nested if-else statements with the same function calls within, how would their predicates be differentiated?
- Raw solution is to make everything in line (will suffer in performance)
- Will there be enough predication entries? How will eviction processes work?
- How will predications be updated upon branching and function calls?
    - Will copy predication mask of branching function and AND new predication onto it
- Function loops will be based on jumps, not branch checking
- Will have to discuss the issue with Sooraj

## Monday (10/20/25) - Weekly Meeting with Sooraj
- Decided jumps will be done on one thread only
- The purpose of a jump instruction is just to change the PC, so no point having all threads change PC since they all run on the same PC
- Hardcoded predicate mask could possibly be implemented by hardware?
    - Since jump is its on instruction type, instead of passing and wasting a predicate mask, warp scheduler could possibly just assign one thread based on J type?

- Informed of update on halt instruction as it will be utilized by hardware's emulator for running unit tests
- Added halt and updated Teal Card

## Thursday (10/23/25) - Weekly SoCET Meeting
- Simple Problems Require Simple Solutions
- Matrix Multiplication; Systolic Array 
- Systolic Array demonstration; operation with input, partial sum, weight, and gives result
- Buses through inputs. and buses though partial sums; one goes down, one goes through horizontally
- GPUs: Single Instruction Multiple Data
- Warps have 32 threads and all threads run on same PC
- HUGE register file needed for modern GPUs (size of L1 cache)
- Banks are utilized for multiiple reads and writes simultaneously
- Bank conflicts if operands needed to live in the same bank
- Banks allow you to have the bandwidth you need for cheap
- 16,000 wires that's routing data around even when unused; crossbar too big, we gotta do something about it
- Read first operand in C0, read second operand in C1 and read first operand for Warp 1 in C1; use of "operand collector"; now a NYC apartment
- "You don't solve non-problems; you don't solve problems with non-solutions"
- Complex solution for complex problems; Usage of the RFC will be based on the compiler