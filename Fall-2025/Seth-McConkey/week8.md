# Design Log Week 8

## Status

Not stuck or blocked.

> Work has been divided for the Functional Simulator and Cycle-Accurate Simulator. Below are details from the Functional Simulator team's progress.

## Functional Simulator Progress

https://github.com/Purdue-SoCET/gpu/tree/main/gpu_sim/funcsim/src

- The team has created the software architecture for the functional simulator
  - Warp Class: Contains the state of each warp, including its masks, register file, and thread IDs
  - Instr Class: Abstract class that all instruction type subclasses inherit from
    - Each instruction class implements an eval() method that modifies the register file of passed to the function by the Warp class's eval() method
  - Reg_File Class: Represents the register file, the Warp class contains myultiple instances of this class to represent the register file for each thread in the warp
  - The ISA is included in the simulator as a set of Enum classes,  one for each specific instruction type (ex: R-type, I-type, etc), and one fir each operation within each instruction type (ex: ADD, SUB, etc)
- Dan is in charge of loading the meminit.hex file, parsing it, and initializing the simulator's memory and CSRs
- Felix is in charge of the Reg_File class
- I am in charge of the Instr subclasses
  - Aditya is helping with this as well
- Andrew is in charge of the Warp class
- So far, we have the skeletons of all the classes set up
  - I am working on implementing the instruction eval() methods
    - So far, R-type instructions are mostly done
- Some challenges and solutions:
  - Handling overflow/underflow in arithmetic operations
    - Python automatically scales int and float sizes to handle values larger than 32 bits (unlike hardware/C/C++)
    - Used bitmasking to make sure overflow is handled like in hardware
    - All values from Reg_File are of type Bits, a class from the bitstring library that allows for conversion between binary, int, float, etc while maintaining a fixed bit width
      - https://pypi.org/project/bitstring/
    - All operations are performed on the Bits objects directly so that behavior matches hardware behavior
    - Added overflow warn print statements to help with debugging

- Next steps:
  - Finish implementing the Instr subclasses
  - Start integrating code
  - Get Aditya GitHub repo access
  - Add a Python virtual environment to the repo with all necessary dependencies and Python version

## Cycle-Accurate Simulator Progress

- I reached out to William Cunningham about using integer operation IP from SoCET, and finding the latencies of the IP implementations
  - Has not responded yet, will follow up tomorrow if he's not at the meeting
- I reach out to Cole Nelson about the FPU IP being developed by the Digital Design senior design team
  - He said the latencies of the FPU are "trivial" at the moment, and we should simply parameterize the cycle count of FP operations and modify them when we discover the actual latencies
