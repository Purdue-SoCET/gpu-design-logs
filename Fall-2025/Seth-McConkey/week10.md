# Design Log Week 10

## Status

Not stuck or blocked.

> Verification of the emulator is ongoing, and implementation of the cycle-accurate simulator is also still in the works

## Emulator Progress

https://github.com/Purdue-SoCET/gpu/tree/main/gpu_sim/emulator/src

- Compilers added float branch instructions, which still need to be implemented
  - [compilers' teal card](https://docs.google.com/spreadsheets/d/1quvfY0Q_mLP5VfUaNGiiruGoqjCMpCyCKM9KlqbujYM/edit?usp=sharing)
- There are some bugs in the emulator with the JAL instruction
  - It has been a little difficult working out kinks in both the assembler, ISA, and emulator at the same time
- Graphics has created a SAXBY ASM test case, it runs but not correctly at the moment
- Our goal is to have the emulator fully verified by the end of next week so that teams can use it to verify their work on the cycle-accurate simulator
- I am also working on simplfiying our Instr classes and Instr_Type and Op enums
  - The way our ISA and opcodes are currently structured makes it difficult to map opcodes to instructions in a clean way
  - For example, there are multiple strings of 4 bits that map to R-type instructions, which means we have to create multiple enums for R-type instructions and simply tack on a incremntenting number to the enum name to differentiate them
  - This makes it difficult to read and maintain the code, so I am working on a solution to this
    - You can use enums with multiple values mapped to the same enum name using a custom class in Python (from aenum import MultiValueEnum), so I am working on implementing that to clean up our class and enum names
 
## Cycle-Accurate Simulator Progress

- I have begun work on the FUs and WB Buffer, but after a convo I had with Jing, I needed more time to implement a few different kinds of WB buffers

### FUs

- Talked to William Cunningham again about latencies of previous SoCET IP
  - The INT multiplier has a latency of 2 CYCLES, not 6 cycles as he previously told me
  - This means that our adder/ALU will probably only have a 1 cycle latency (we won't be getting any CLK gains out of pipelining the ALU if our multiplier is only 2 cycles)
  - NOTE: We need to look into the INT multiplier potentially being the CLK/comb path bottleneck, and if it is, look into pipelining it more

#### Unit Tests

- Overflow
- Underflow
- negative/positive
- negative/negative
- div by zero
- inf and -inf in float instructions
- NaN in float instructions
- 0 in float instructions
- signed and unsigned behavior for INT instructions

### Writeback Buffer

 - One with a buffer per FU that stalls the whole GPU when one of them is full
  - One with a buffer per FU that stalls only that FU when its buffer is full
  - One with a shared buffer per RF bank that stalls only the FUs writing to that bank when the buffer is full
- I think that this will be a major factor in the performance of our arch, so I want to make sure that I test this very throughly

#### Unit Tests

- One buffer filled
- Multiple buffers filled
- All buffers filled
- No buffers filled
- Writeback policy tests
  - Oldest value
  - Fullest buffer
  - LD/ST priority
- Different buffer sizes
- Different buffer types
  - Circular
  - Stack
- Simultaneous writes to same RF bank
- Simultaneous writes to different RF banks
- No writes to RF banks
- Passthrough writes to RF banks



  
 
