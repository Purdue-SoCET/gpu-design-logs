Status: No help needed YET

We discussed how to approach the functional simulator, which includes:
- Instr class
    - handles everything within a singular instruction and holds instruction information
    - uses Bits, from the bitstring class
    - features classes for every type, which will compare to attributes of said class. 
- Reg_File class
    - holds 64 register files (parameterizable), and methods for reading and writing to them
    - each reg file is initialized as a Bits class (int=0, length=32)
    - expects int or float, returns Bits
- Warp (TBD)
    - will hold instr and reg_file class for each thread
    - will handle predication and masking
However, we don't have anything running yet. Things to do:
- Create testbench/assembly files to run
    - what would be a good testbench for the GPU? Should we test out a "scalar" GPU, consisting of a single thread and warp first?
    - Figure out how compiler team's compiler works, and maybe ask them for some super simple testbenches.  
- take Daniel's initial emulator and extract the proper values for the Instr class
    - is the assembler big or little endian? Can we simply assume that "line[31:29] (little endian)" will always be opcode?
- declare each thread of a warp, with its own individual RF.
    - do we want the RF to be indexed, or another attribute some other class?
      -  can't be Warp, since each thread within a warp uses a different RF
      -  Instr? Would have to pass down the RF for each new Instr
      -  Indexing seems to be simplest: thread_id = RF_id
-  Implement PC somehow for branches, current implementation just reads sequentially through the (nonexistent) assembly file

It feels like this emulator is "too good", I was expecting a lot less complexity. At least this makes funcsim easier (hopefully).
