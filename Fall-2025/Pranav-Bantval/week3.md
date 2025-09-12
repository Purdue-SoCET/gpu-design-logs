# Week 3

State: I am not stuck with anything, don't need help right now. 

Progress: Read chapter 4 & go to the supplemental lecture for pipelining and caching

## Supplemental Notes
- Amdahl's law is used to compare increase in performance between two variables, taking the percentage run and time saved as a ratio
- Iron law states that time per program is related to instructions/program * cycles/instruction * time/cycle
- Most optimization comes from cycles/instruction & time/cycle
- Pipelining saves time per cycle by giving higher throughput
- By saving state during the operation of an instruction, we can reduce the clock speed while also bringing multiple instructions into the processor, one for each state
- This means adding registers after each stage (fetch decode execute writeback memory)
- There can be structural hazards (dual write) and data hazards (read after write)
- Solutions: stall, guess (data hazard), look ahead (data hazard)
- Control hazards - stall / guess
- Caching puts memory near the CPU so that it's closer & takes less cycles to access
- Cache uses locality (space & time). Locality is like a predicitive optimization that data most relevant (closest in space/time) will be used more frequently.
- E.g. if a variable is just created, it will be used almost immediately rather than 100+ lines later.
- AMAT: average memory access time. hitrate, missrate, miss-penalty: cache lookup time, % frequency data is not in cache, ram lookup time
- Cache uses a hash to store data, don't need hash if you can store everything in cache

## Chapter 4

  
## Chapter 3 - SIMT core instruction & register data flow

### 3.1 - one loop approximation
