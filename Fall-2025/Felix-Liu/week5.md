
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

Nvidia doesn't have an OC, due to latency needing to be known at compile time. Thus, port conflicts do not impact the stall counter. (This is probably not feasible for our GPU).
A result queue allows for no delays when there is a conflict between two fixed-latency instructions. This is done by bypassing to forward the results to consumer BEFORE being written to reg file. 
Having two source registers in one bank creates a 1-cycle bubble, while no conflict results in no bubble (obvious). 

Interesting area for research: this hierarchical register file should perform close to a register file with unbounded ports, but is not the case for certain benchmarks.
 -> figure out why, what kind of bench marks, and do some research. Make said ideal register file to compare the actual register file with (in terms of performance). 

 Dependency handling would require ~5% of the register file size. 

# A Compile-Time Managed Multi-Level Register File Hierarchy [Gebhart et al.]
## Key takeaways
"The processor experiences no performance penalty for accessing values from the MRF vs the LRF or ORF." 
"... a value's allocation location dictates the access energy"
"Compared to the MRF, the wire energy for the private datapath [ALU] is reduced by a factor of 5 for ... ORF and a factor of 20 for ... LRF"
Hardware-software results in 54% decrease in power vs hardware-RFC only with 44%.
**Compiler-centric**
These problems exist for the compiler, I'm considering looking into hardware solutions/alternatives from the more recent research.
"Rather than simply consider a value's lifetime, ... , a compiler must consider the number of times a value is read and the location of these reads in relation to scheduling events" 
### Main Register Files (MRF)
Stores context for all threads. 32 registers per thread. 
### Operand Buffering/Collecter
Figure out how this is different from operand collectors and how we may need to modify the usage here vs Malekeh (OCs as cache).
Fetches operands (over several cycles) and delivers to correct FUs. Serves to deal with bank conflicts, latching and collecting them in this buffer. 
  - Each entry is 128 bits wide and stores a register of 4 threads. This entry is split into word-size values and distributed to the 4 SIMT lanes, which is energy intensive.
  - SIMT lane has private ALU, but more expensive execution units (SFU, FPU?) are shared between lanes. MEM port and TEX (texture unit) is also shared.
      - This paper has 8 of these 4-wide SIMT lane clusters to form a 32-wide SM.
  - hold and serialize read/write (genofog ex.)
Malekeh: would it turn these op buffers into caches?

## Prior work: Register File Cache
### RFC
Caches operands directly from ALU and evicts to MRF (FIFO). Allocates only to active threads.
Reduces MRF accesses by 40-70%, saving 36% of register file energy with no performance penalty.

### (Two-Level) Scheduler
Long latencies are tolerated via lots of warps. Short latencies can be tolerated with much less threads. 
Masks threads into active (issues instr) and pending (waiting long latency). 
Active warps that encounter dependence on long latency is swapped out with a ready warp from pending. Its RFC entry is flushed to MRF. 
SM is normal performing with at least 8 active warps.
ORF and LRF are temporarily shared across threads (how? because the values are cached, so it can theoretically be access by any thread?), thus **must be stored in MRF upon descheduling.** Thus, allocation also forces scheduling decisions. 


## Operand Register File (ORF)
Problems that arise from hardware-only:
- Eviction from RFC consume energy (from read) before written to MRF.
- RFC must track MRF reg names with tags + lookup in RFC.
**Solution**: compiler tells (scheduler? OC?) where to allocate values/operands. Frequent/soon to be read values to ORF and less temporal locality to MRF.
Segments of the register file namespace(?) is assigned to different levels of the hierarchy. This results in no increase of energy from larger instr or more decode (how?).
Removes having to tag or check tags.
Namespace is under-utilized, thus using it to represent LRF and ORF doesn't diminish using MRF.
<img width="1061" height="261" alt="image" src="https://github.com/user-attachments/assets/a6a3127d-43dc-47c7-b081-7a92af8247a2" />

## Last Result File (LRF)
Use with the three-level register file hierarchy, consisting of LRF, ORF, MRF. 
LRF would optimize instr with only next instr as consumer. Each ORF + LRF entry would have 3 read 1 write ports.
Compiler encodes which level to store operands of instruction. 
Shared datapath (SFU, MEM, TEX) only takes up 7% of execution, with 70% of its inputs (consumed by shared datapath) from private datapath (ALU/instr).
This reduces opportunity to store values produced and stored by shared datapath near said datapath. 
-> Thus, shared datapath only needs to access ORF and not LRF, minimizing ALU to LRF wire and energy.  
**Split LRF**: separate banks for each operand slot. Rather than a single LRF bank per SIMT, it would be 3 banks. Increases size of LRF while keeping access energy minimal. This results in 20% increase in LRF usage, which is great! Optimal register file would have every access to LRF. 
