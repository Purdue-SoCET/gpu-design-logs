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
- GPUs have multiple memory spaces - local (per thread) & global (shared across all threads) & scratchpad/shared memory (shared in threadblock)
- scratchpad reduces dram latency by staging data on-chip (cache)
- helps with overlap communication with memory access
- dram bandwidth is a bottleneck, GPUs can execute far more instructions than the rate data can be supplied
- this is also more energy efficient

### 4.1
- shared memory has low latency, implemented with single ported sram banks
- bank conflicts occur when multiple threads in a warp try to access different addresses in the same bank
- Conflicts handled by splitting request: conflict-free subset ran & conflicted subset replayed
- replays can be buffered
- L1 cache stores a subset of global memory
- Coalescing is if all threads in a warp access the same global memory cache block
- Unified shared + L1 cache is introduced in Fermi, it has same sram array partly direct mapped for shared and partly set-associative with L1
- Sequence: Load/store unit computes addresses & coalescing, arbiter accepts/rejects based on resources, tag unit checks hit/miss, data returned on hit and misses sent to pending request table
- PRT tracks outstanding misses, merge requests into the same block and signals replay
- cache organization is virtually indexed and virtually tagged
- global memory does not have write-through (bad locality), local memory (register spills) write-back and write-allocate (good locality)
- L1 texture cache used mainly in graphics but gives insight for throughput design of GPU
- exploit locality in texel accesses (adjacent pixels)
- tag array runs ahead of dram array w/ a Q to hide dram latency
- both hits & misses have similar latency
- Optimized for high miss tolerance not low latency
- You can unify the texture and data caches but only read only data can use it then to maintain coherence

### 4.2
- GPUs need high bandwidth for SIMT cores
- DRAM is split into multiple memory partitions with traffic distributed by address interleaving (NVIDIA crossbar)

### 4.3
- L2 cache slice, memory access scheduler (frame buffer), and raster operations (ROP) unit is included in each memory parition
- L2 cache sliced into 2 for tag & data arrays
- coalesced writes overwrite entire sectors (skip read before write) while uncoalesced need valid bits or bypass L2
- the memory access scheduler is needed because dram access is slow and complex
- dram has multiple banks but switching rows is costly
- schedulers reorder memory requests to reduce row switches
- each l2 slice may have its own scheduler
- scheduler design: separates read & write, multiple reads mapped to same row are grouped and stores individual read requests to group
