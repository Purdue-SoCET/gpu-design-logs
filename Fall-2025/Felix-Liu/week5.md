Status: Pretty far behind due to missing last Sunday meeting (out of town), flat tire + car damage (all of Monday Tuesday) and most of Thursday meeting (exam). 
Will try to catch up, read all the research, review important microarchitectures (register file, i$, and **access coalescer**)

Highlighted and made extensive notes on a printout of "Analyzing Modern Nvidia GPU Cores", mostly focusing on register file and RFC. 

# Control bits (inside each instruction)
These values are all set by the compiler. 
  Stall counter: stalls a warp for its value, decreasing by 1 for each clk until 0. This is only for fixed-latency producers. 
    -> this paper states that hardware doesn't check for RAW hazards, relying instead on this compiler-set value. 
  Yield: in the next clk cycle, don't issue instruction from same warp. If no other warps are ready for issue, no instruction is issued.
   -> stall would basically yield.
  Dependence counters (SBx): counters are increased at issue and decreased at writeback. The consumer instruction would stall until this value is zero before issueing. 
    -> tracks variable-latency dependencies
  Dependence counters mask: SB0 and SB3 must be zero.
  Reuse: whether to cache or not the contents of a register. 1 bit per source operand. 
Producer sets stall to 2 prior to issueing consumer (RAW and WAW). Values are forwarded back rather than waiting for memory access of a producer instruction.

# Register File
Types of register files
Regular: 65536 32-bit registers per SM. 64 warps * 32 threads = 2048 warp threads. 2048 * 32 reg/thread = 65536. Nvidia has register file virutalization and allocation at compile time. 
Uniform: 64 private registers shared by threads within a warp.
Predicate: 8 registers to indicate which threads must execute an instruction and whether an instruction takes the branch or not. 
Uniform predicate: 8 1-bit registers to store a predicate shared by all threads in a warp. 
SB registers: dependence counters.
B registers: manages control flow reconvergence
Special registers: stores special values like thread or block IDs.

Nvidia doesn't have an OC, due to latency needing to be known at cmopile time. Thus, port conflicts do not impact the stall counter. (This is probably not feasible for our GPU).
A result queue allows for no delays when there is a conflict between two fixed-latency instructions. This is done by bypassing to forward the results to consumer BEFORE being written to reg file. 
Having two source registers in one bank creates a 1-cycle bubble, while no conflict results in no bubble (obvious). 

Interesting area for research: this hierarchical register file should perform close to a register file with unbounded ports, but is not the case for certain benchmarks.
 -> figure out why, what kind of bench marks, and do some research. Make said ideal register file to compare the actual register file with (in terms of performance). 

 Dependency handling would require ~5% of the register file size. 
