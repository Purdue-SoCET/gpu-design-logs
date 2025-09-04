# Week 2 Design Log
Explicit Statement: I am not currently stuck or blocked

## Questions: 
1. Actual definition of a set?
2. What is predication?
   - Seems related to determination of branching
3. Figure 4(a) not really sure how basic block E comes into play
   - Kind of like a "temp" reconvergence block?
4. Does "mask off" just mean a thread in a basic block is "turned off" not being executed? Assumes that all threads will be in lockstep then
5. Figure 3.5 -> does moving the exchange into the while loop fix the deadlock? Not sure how code blocks are created, tied to question about code block E in figure 3.4(a)
6. This allows other threads to move forward "past a convergence barrier" in that would otherwise lead to deadlock. 
   - This makes no sense, if they move forward how is the thread(s) deadlocked able to move forward?
     - Unless ur saying the exchange occurs beyond the convergence barrier
7. What are Miss status holding registers for?
8. Scoreboarding says up to 128 registers per warp
   - If each warp has 32 threads, then each thread has 4 registers (why though?)
9. What is figure 3.11 showing
    - Related to busy spinningin 437, but it spins on lock
      - So what?
10. What is a a bloom filter, the ILP solution to WAR hazards in Operand Collector


10. Immediate Post-dominator is the singular exit node in a CFG or sub CFG

# Chapter 3 The SIMT Core: Instruction and Register Data Flow
- SIMT Cores for computation
  - GPUs data sts -> too large to be cached on chip
  - On-chip caches are still able to leverage spatial locality
    - **Adjacent** pixel operations<br><br>
- Overall MicroArch: 
  - ![image](images\fig3_1.png "Figure 3.1")
  - Ins fetch loop
    - Fetch
    - ICache
    - Decode
    - IBuffer
  - Ins issue loop
    - IBuffer
    - Scoreboard
    - Issue
    - SIMT Stack
  - Register access
    - Operand Collector
    - ALU
    - Memory
## 3.1 - One Loop Approximation <u></u>
- **Unit of scheduling** is a <u>warp</u> or <u>thread</u>
- SIMT Execution mask values vs Predication
  - Each set == a thread using a function unit in a lane provided by SIMT execution lane
    - **Note:** a function unit has MULTIPLE lanes
- NVIDIA GPUs have many FUs
  - Special Function Unit
  - Load/store unit
  - Floating point function unit
  - Integer function unit
  - Tensor core (Volta Architecture)
- Some GPUs have wavefront/warp executed over several clocks 
  - Clocking the function units @ higher frequency -> higher performance
    - Done by pipelining/pipe depth
- 3.1.1 SIMT Execution Masking
  - Presented to programmer -> individual threads execute completely independently 
  - Programming model achived wiht 
    - Traditional predication + SIMT stack (stack of predicate masks)
  - SIMT Stack - Handles 2 issues
    - Nested control flow: where one branch is control dependent on another
    - Skipping computation while threads in a warp avoid control flow path
      - Significant saving for complex control flow
    - Traditionally suppourted by CPU w/ predicate regs
  - Assume HW manages SIMT stack
    - ![image](images\fig3_4.png "Figure 3.4")
      - A -> shows the control flow branching
      - B -> shows masking of threads in basic block execution
        - Important for reconvergence upon branching
      - C - E -> Stack to track
        - RPC (reconvergence PC)
        - Next PC
        - Active Mask
    - Reconvergence point: "@ compile, time that threads which diverge can execute in lockstep again"
      - Immediate post-dominator of branch causing divergence
      - @ Runtime, possible to reconverge earlier
    - Typically add entires with most active threads into stack first
- 3.1.2 SIMT Deadlock and Stackless SIMT Architectures
  - SIMT Stack can -> SIMT Deadlock
    - Handled with Independent Thread Scheduling
  - SIMT Deadlock (description)
    - ![image](images\fig3_5.png "Figure 3.5")
    - 0 = lock free
    - atomicCAS == atom.global.cas (in PTX compare and swap)
    - atomicCAS(mutex, compare_val, update_val) -> return og val of mutex
      - serialization of mutex access due to atomicity
    - Since exchange can't be executued, no other thread can access mutex causing the deadlock. 
  - Stackless Branch Reconvergence
    - ![image](images\fig3_6.png "Figure 3.6")
      - Barrier Participation Mask -> Tracks which thread in warp participate in a given convergence barrier
        - So it just saying all threads that are expected at a barrier
      - Barrier State
        - Track which threads have arrived at a convergence barrier
      - Thread State
        - Thread is: 
          - Ready to execute
          - Blocked at a convergence barrier (if so which one)
          - Or has yielded
            - This allows other threads to move forward "past a convergence barrier" in that would otherwise lead to deadlock. 
      - Thread rPC
        - tracks (per thread not active) addr of next ins to execute
      - Thread active
        - Bit to tell if thread in warp is active or not
    - Threads diverge -> executing a branch
    - Special **ADD** ins to identify convergence barrier partificpation mask
    - Special **WAIT** ins to 
      - Add threads to barrier State reg
      - Change Thread state to blocked
      - Once all threads in barrier state reg executes wait, can switch all threads to active
    - Special **Yield** ins to
      - Allow switching betewen warp splits
    - Warp Split
      - When scheduler selects subset of threads with common PC and enable Thread Active Bit
  - (HIGH LEVEL OF STACKLESS) -> Allows scheduler to switch between groups of diverged threads
    - ![image](images\fig3_10.png "Figure 3.10")
      - Interleaving stackless vs Blocked Stacked
- 3.1.3 Warp Scheduling
  - Which order should warps be scheduled in? 
  - Assume lockstep instruction issue and execution (one by one)
  - If memory latency is <u>**IDEAL**</u> 
    - Can implement round robin scheduling
    - If we assume this w/o the overhead of data exchange, each thread needs its own regs
      - if increase warps the core -> fracitonal area to regs relative to execution increases
  - If memory latency is <u>**REALISTIC**</u>
    - Leverage locality to increase on chip cache hits
    - Want to schedule so threads progress at the same time for texture maps etc.
    - Round robin is good for locality of wide net workloads
    - Specific thread scheduling good for disjoint data of a large structure <br><br>

## 3.2 Two Loop Approximation
- How does scheduler know if it there is control dependency?
  - Place an instruction buffer to order instruciton after cache access
    - Seperate scheduler is used to decide which between those in buffer should be sent into the pipe
- Instruction memory first level cache backed by unified L2 cache
  - Instruction buffer helps hide cache miss 
    - (MSHRs) -> miss status holding registers 
    - Typically can hold one or more instructions per warp
- Detecting Dependencies
  - <u>Scoreboard</u>
    - in-order or out-of-order execution
    - each register is represented in the scoreboard
    - a bit is set whenever instruction writes to it
      - Any instruction write/read to register is stalled until bit is cleared
    - prevents RAW & WAW hazards
    - WAR if it is in order execution
  - Reservation stations
    - eliminate name dependencies
    - introduce the need for associative logic
  - <u>Challenges</u> of simple in-order scoreboards
    - Size concern
    - Dependency "hit" need continuous scoreboard lookup until scoreboard is clear
      - This means more readports are needed for the register for all threads to "check" the scoreboard
        - 256 readports, expensive
  - <u>Solution</u> to challenges
    - 3-4 entries per warp
    - Entry holds identifier of reg that will be written by instruction
      - Issued but not yet executed
    - Upon ICACHE fetch into ins buffer, compare source and destination regs
      - If match, set bit in scoreboard
      - Copy these 3-4 bits into buffer
      - Instruction cannot be considered by scheduler until all bits are cleared
        - Bits are cleared as instructions write the result to register file
      - If all bit entries are used, either:
        - Ins fetch stalls
        - Refetch that instruction
- First Loop 
  - selects warp that has space in instruction buffer
  - Lookup PC and access ICACHE
- Second Loop
  - Selects ins in instruction buffer that has no dependencies and sends into pipe

## 3.3 Three Loop Approximation
- Want to suppourt as many warps, but inhibited by read ports
- Problem Cause
  - ![image](images\fig3_12.png "Figure 3.12")
    - Register Read stage of the pipeline
    - Register file is broken in 4 banks, so 4 read/write ports
      - Arbirter can serve 4 instructions and passes infro to the next stage reg/latch
  - ![image](images\fig3_13.png "Figure 3.13")
    - Start bottom left and move right (naive implementation)
  - 3.14 shows us that if access are not spread well across banks, it causes delays in value access
- 3.3.1 Operand Collector
  - ![image](images\fig3_15.png "Figure 3.15")
    - Staging register/latch is replaced with collector units
      - Each intruction is tied to collector unit in read register stage
      - Multiple collector units to overlap reading of source operands
        - Enough to hold all source operands for an instruction
        - Allows for high bank level parallelism 
  - Scheduling to tolerate bank conflicts 
  - Figure 3.16 -> swizzled banked register
    - Helped for conflict between instructions from different warps
  - Problem: No imposed order -> allowing RAW hazard
    - Two instruction from same warp present in operand collector
      - A ins reading reg that B ins writes to
      - If A gets repeat bank conflicts, B can write new val to reg BEFORE A regfile has updated val
    - Just simply require "leaving" in order within same warp. 
    - Three methods: 
      - Release-on-commit warpboard
        - at most on instruction per warp to execute -> bad performance
      - Release-on-read warpboard
        - only instruction per warp to collect operands in operand collector -> capped slowdown @ 10%
      - Bloomboard
        - ILP in OCollector
- 3.3.2 Instruction Replay: Handling Structural Hazards
  - Don't want to stall younger instruction till resource is ready: 
    - Large size of reg file + pipeline stages -> stall signal extends critical path
    - Stalling one instruction from warp stalls other behind that MAY not be hindered by structural hazard
      - Wasted resource, hurts throughput
  - Instruction Replay -> recovery mechanism when speculative scheduling runs into hazard
    - Avoid clogging the pipeline
    - Avoid increasing circuit area
    - Timing overheads (all from stalling)
  - GPU can hold instructions in the instruction buffer until it has been completed/some parts have been executed.

## Refer to 3.4, 3.5 in an addendum

## 3.6 Research Directions on Register File Architecture
- Register Files are WIDE in GPUs due to wide SIMD datapaths
- Warps needed to tolerate/hide hundreds of cycles of memory latency
- Below are methods to optimize energy consumption <br><br>

- 3.6.1 **Hierarchical Register File**
  - Add register file cache (RFC), reduce access freq to main reg
    - FIFO addition of entry
    - Any value evicted from RFC is written back to main RF
    - Extra bit (based on compile generated info)
      - Mark as dead if register will be read for last time -> not written back @ eviction
  - Two level warp scheduler
    - Set a pool of active warps (4-8 warps)
    - RFC only holds values from active warps
    - Warp is removed for long latency operations (global mem loads/texture fetch)
    - RFC entries flush, freeing space for different warp
  - Compile Time Managed Register File Hierarchy
    - Last Result File (LRF)
      - Buffers reg val produced by last ins of each warp
    - Creates compile time managed Operand Register File (ORF)
      - Compiler says when a warp can be switch out of active pool
        - NOTE: Must move all live data out of ORF before switching warps
- 3.6.2 **Drowsy State Register File**
  - Reduce leakage power of the RF 
  - Tri modal
    - On 
      - Normal operation
    - Off
      - Does not retain val in register
    - Drowsy
      - retains value only, needs to go to ON for normal operation
  - Non allocated regs is off
  - Allocated placed into drowsy immediately
  - Long pipeline means that overhead of "waking/ON" reg is not a significant overhead
  - Key idea: Active reg spend most time in drowsy mode
- 3.6.3 **Register File Virtulization**
  - While wating for memory ops, LIVE REGs are small ~60% unused
    - Half the number of registers
    - Double the number of threads
  - Utilize register renaming to virtualize physical regs
  - Use extra "last read instruction" bit
  - Add metadata instructions 
    - Encode when physical registers can be reclaimed
  - Branch divergence must be taken into account when recaliming physical registers
  - Show that halving register file size by ~50% with no performance loss is possible
- 3.6.4 **Partitioned Register File**
  - Partitions RF into slow and fast
    - FRF uses normal speed SRAM
    - SRF uses NTV SRAMS <- lower access energy, lower leakage for slower access
  - Every warp has 4 entries in FRF -> service most of the access
  - SRF additional latency hidden by Operand Collector
  - FRF also has low power mode -> reap benefit of two-level scheduler without  warp moving in/out of active pool
  - (VS Heirarchical) Partition remains constant throughout operation
  - CTA at each kernel launch to analyze most frequently used regs
    - Put in LUT accessible to every subsequent warp form kernel launch
- 3.6.5 **RegLess**
  - Replace register file with iperand staging buffer
    - short time spans -> num regs access is small frac of total cap
      - 100 cycles -> lt 10% of 2048KB RF used
        - Greedy-than-oldest scheduling policy
        - two level warp scheduler
  - Use compiler to divide kernel execution into regions
    - Regions: Contiguous ins within single basic block
      - Region boundry selected to limit live registers
    - Capacity Manager: determines which warps are aligible for scheduling
  - When warp begins executing ins from new region, regs in region -> OSU (Operand Staging Unit)
    - OSU: Cache consisting of 8 banks -> enough BW to service two ins/cycle
  - Avoid stalling, CM preloads regs before issuing first ins in region
    - Preloading: State Machine for each warp -> regs needed for region in ISU
  - 512 entry OSU slightly better performance vs 2048 KB RF
    - Only 25% space & lower energy used by 11%


  

  