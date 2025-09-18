# Week 4
statement: I am not stuck.
## Progress
Finish reading chapter 5.1

## Learning and key concept

### Chapter 5.1 Thread Scheduling

### Introduction
- Since GPU is more rely on massive parallelism, which means there are thousands of threads working at the same time. GPU has to employ and schedule those threads. The following are the 3 primary ways of threads management:
  - Assignment of Threads to Warps: threads -> warp
  - Dynamic Assignment of Threadblocks to Cores: group of warps -> threadblock. The GPU assigns threadblocks to cores.
  - Cycle-by-cycle Scheduling Decisions: After a threadblock is on a core, the hardware schedulers will decide in every single cycle that which warps should fetch, issue, execute, read/write.
- Scheduling Multiple Kernels
  - run multiple kernels at the same time which is simialr to CPU runs multiple programs   

### 5.1.1 Research on Assignment of Threadblocks to Core
- background
  - round-robin scheduling: threadblocks are continously scheduled until one source in each core is exhausted. This will be a issue when we have more threadblocks than GPU can run.
- solution
  - Throttling at the Threadblock Level throttling:
    - limit the number of threadblocks on a core to reduce contention in memory.
    - An algorithm will assign half of maximum number of threadblocks.
    - Though fewer threadblocks are running, but we improve overal performance since memory management is more efficient.     
  - Dynamically Tuning GPU Resources
    - Equalizer: a hardware that adjust resources to improve performance and power efficiency.
    - Equalizer constantly monitors four key parameters on each core:
      - the number of active warps
      - warps waiting for memory
      - warps ready for arithmetic instructions
      - warps ready for memory instructions.
    - Based on these paraemter, each core will decide how many threadblocks it should be runnig and the best frequency of both the core and memory system
  - two modes:
    - energy-saving mode: scale back the under-utilized resource
    - performance enhancing mode: boosts bottleneck resource

### 5.1.2 Research on Cycle-by-Cycle Scheduling Decisions
- Two-Level Scheduling
  - energy efficiency:
    - warps are split to an active pool and inactive pool. The scheduler consider active pool and moves to inactive pool when have memory operation, then switch back to active pool.
  - performance:
    - group threads to make them access nearby memory locations.
- Cache-Conscious Wavefront Scheduling (CCWS)
  - intra warp: data load in the same warp.  CCWS exploit the locality by throttling numebr of warps schedules absed on system feedback
  - detect useing victim tag: on every eviction from cache, the victim tag will be written to victim tag array.
  - if there is the cache miss, it checks the victim tag array. if tag is here which means a lost locality, where locality score for that warp is increased. It will push other threads, when it reaches a threhold, it will pause the memory request. This give the high locality score warp more chance of using cache. 
    <img width="400" height="680" alt="1 2025-09-18 161522" src="https://github.com/user-attachments/assets/fe129d7f-1098-4f2a-9970-44f576fe4887" />
- Divergence-Aware Warp Scheduling (DAWS)
  - create per-warp cache footprint to esimate for warps in loop.
- Prefetching-Aware Warp Scheduling:
  - groups warps to improve memory bank-level parallelism.
- CTA-Aware Scheduling
  - to avoid DRAM bank conflicts      
- Cache Access Re-execution
  - MAS warp scheduler: prioritize warps doing computation with memory accesses/
  - CAR cache access re-execution: help get data cache hit when memory pipeline is stalled.

### 5.1.3 RESEARCH ON SCHEDULING MULTIPLE KERNELS
- able to switch between different kernel without performance loss
- solution
  - full context save/store
  - wait until threadblock finished
  - stop thradblock wiout saving text and restart safely
 
### 5.1.4 FINE-GRAIN SYNCHRONIZATION AWARE SCHEDULING
- problem: when a thread is locked by another thread (spin), we need to check everytime to see if it is unlocked.
- solution: dynamically detect the loops taht are spin loops, and sheduler reduces its priority, allowing other warps to run. 
