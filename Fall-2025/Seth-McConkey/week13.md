# Design Log Week 13

## Status

Not stuck or blocked.

## Emulator Progress

- I had to pass ownership of the emulator down to Dan and Felix because I need to focus on the cycle-accurate simulator for the rest of the semester
  - I have a lot of modules that I need to manage for the cycle-accurate simulator
  - I have been answering their questions about the emulator as they come up though

## Cycle-Accurate Simulator Progress

- I was able to finish all portions of the EX stage and WB stage this week
  - The EX stage now has all functional units implemented and tested
    - INT ALU, MUL, DIV
    - FP ADD/SUB, MUL, DIV, SQRT
    - INV_SQRT, TRIG
    - Each functional unit has its own pipeline implemented with the custom `compact_queue` class that Andrew made
    - They are all configurable with number of FSU instances
    - Each FSU is parameterizable to support either INT or FP operations and their pipeline latencies can also be configured
    - The EX stage is configurable to allow for a different number of FU instances as well
  - The WB stage is also fully implemented now
    - It allows for configuration of writeback buffer count, arbitration policy, and writeback buffer size

- Performance counters have been implemented for both stages
  - Jing wants us to work on creating a performance counter framework that can be used across all stages
  - Each stage will have its own performance counter class that inherits from a base performance counter class
  - The base class will have common functionality, and each stage's performance counter class will implement stage-specific counters

- Next up is working on integrating everything:
  - Some specific steps:
    - Get everyone using the updated Instruction class with my modifications
    - Work together to merge all of our individual branches
    - Create our final main loop
    - Create some test cases to verify the code

## Undergraduate Research EXPO

- The HW backend team created our poster this week and presented at the Undergraduate Research EXPO on Tuesday
- It was a good experience and I learned a lot for future presentations
  - This was my first time presenting a research poster at an event like this
- I do wish we had more time to put into our poster. I had a lot going on the week before and wasn't able to polish it as much as I would have liked
