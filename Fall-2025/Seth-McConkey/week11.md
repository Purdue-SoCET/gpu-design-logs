# Design Log Week 11

## Status

Not stuck or blocked.

> Verification of the emulator is ongoing, and implementation of the cycle-accurate simulator is also still in the works

## Emulator Progress

https://github.com/Purdue-SoCET/gpu/tree/main/gpu_sim/emulator/src

- Bugs with JAL instruction have been worked out
  - The assembler, ISA, and emulator are now all in sync with each other for this instruction
- Graphics has created a SAXBY ASM test case, it runs but need to verify correctness still
- We need more test cases to fully verify the emulator
  - I am working with the graphics team to get more test cases from them
- A lot of confusion around CSRs still in regards to threadblock managment and assigning IDs to threads from different threadblocks
  - HW needs to have a meeting with Graphics to basically work this out
    - Also consider making them implement the CSR part of the emulator/funcsim
 
## Cycle-Accurate Simulator Progress

- Work has been slow on the Cycle-Accurate simulator
- Mostly due to the fact that our base classes have been changed so many times :(
- I have the software architecture mostly set up for FUs, just need to figure out how to implement the pipelines of them
  - There are FU abstract class and functional sub unit (FSU) abstract class
  - There are implementations of each FU type that inherit from the FU abstract class
  - Each operation (add/sub, alu, mul, div, sqrt, inv_sqrt, trig) has its own FSU
  - Each FSU implementation is paramterized to either be INT or FLOAT
  - This allows for less code duplication
  - The INT FU will contain a list of INT FSUs, and the FLOAT FU will contain a list of FLOAT FSUs
  - Andrew has just pushed a custom `compact_queue` class that basically acts as a set of latches with stall and NOP handling
    - Loop iterates backwards through the queue to update values
    - Values only advance if the next stage is not stalled
    - If the next stage is stalled, the current stage stalls
    - Loop iterates through all stages
    - This will be much easier to use over the LatchIF class we were using before
    - Will also work for WB buffers as well I believe


  
 
