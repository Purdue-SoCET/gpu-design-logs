I am not currently stuck or blocked

Week 2: 8/31/25 - 9/4/25
Tuesday (8/26/25): 
- Started reading Chapter 3.1
- Reading Notes:
    - SIMIT core has SIMT front-end and SIMD back-end
    - instr fetch loop: instr fetch, icache, decode, i buffer
    - instr issue loop: i-buffer, scoreboard, issue, SIMT Stack
    - reg access scheduling loop: operand collector, ALU, memory

    - Warp: Unit of Scheduling
    - In each cycle, hardware selects warp for scheduling
    - Fetch source ops on reg file simulataneously with SIMT execution mask
    - Execution in SIMD
    - Each thread executes on the function unit associated with a lane provided the SIMT execution mask is set
    - Function units heterogeneous
    - GPUs can pipeline to take multiple clk cycles for execution

    - SIMT Stack: combination of traditional prediction along with a stack of predicate mask
    - Nested control flow can have dependency; skip computation to avoid control flow path
    - Prediction used to negate this
    - How does hardware enable threads to follow different parts through code while SIMD datapath allows on instr per cycle? Serialize execution of threads of dif paths
    - Threads that pick other path will be masked (paused) until later in time
    - Threads will eventually reconverge after completing their paths
    - Uses a stack for divergent code paths
    - Reconvergence Program Counter (RPC)
    - Active Mask shows which threads will be running with a "1"
    - Put entry with most active threads on stack first

    - Deadlock: when thread executions depend on each other and won't run until the other runs at the same time
    - C&S(a, b, c) checks if a=b, if so, a <= c
    - C&S returns a
    - C&S performed atomically for each thread
    - Atomically: done without interuption
    - All threads access same mem location of a, so only one thread will see 0 (unlocked) to change it to 1 (lock); others will see it as locked
    - Only one thread exits loop while others continue to loop; one exiting will be done so won't alter mutex anymore, leaving all others in loop => deadlock

    - Stackless Branch Reconvergence: replace stack with per warp convergence barriers
    - Barreir Participation Mask and Barrier State and Thread State are stored in register
    - Barreir Participation Mask: track which threads are running in a given convergence barrier
    - Can be more than one Barrier Participation Mast for warp
    - Wait until common point to reconverge before continuing
    - Barrier State Field: tracks which threads arrived at convergence barrier
    - Thread State: for each thread in warp: ready to execute, blocked at convergence barrier (which one), or yielded (dependency to other thread that'd lead to deadlock)
    - Thread rPC: inactve thread addr to next instr for execution
    - Thread Active: indicates active warp
    - 32 threads mean 32-bit mask; 1 = participate
    - Special ADD instr to set bit in convergence barrier
    - Scheduler updates PC differently for threads who diverge(warp split)
    - WAIT instr stops warp split when reach convergence barrier
    - YIELD isntr: enable switching between warp splits

    - Warp Scheduling
    - warp issues one instr at a time
    - Ideal mem system has round robin scheduling with equal time per instr
    - Increasing warp count can increase throughput per core
    - However, to have dif instr per dif warp, each thread must have own regs, meaning more chip area, thus decrease in number of cores
    - Response latency of mem depends on locality properties
    - Round-robin scheduling good for graphics with equal progress
    - Not good for complex data structs that access disjoint data; so better schedule repeatedly


Thursday (8/28/25):
- Started reading Chapter 3.2, 3.3, and 3.6
- Reading Notes:
    - To hide long execution latencies, issue a subsequent instr from warp (aka pipelining)
    - Issue with one loop because doesn't know about dependency
    - GPUs have instr buffer placed after cache access
    - Instr mem as first-level i-cache, with secondary/unified cache; help with cache miss latencies with miss-status holding registers (MSHRs)
    - Store one or more instr per warp

    - Detect Dependencies: scoreboard and reservation stations
    - Reservation station: eliminate name dependencies, associative logic (expensive in area and energy)
    - Scoreboards: in-order or out-of-order execution
    - Scoreboard in CPU: each reg represented by bit that is set when instr uses a write to it; next instr checks board and stalled until bit is cleared by instr
    - Prevents RAW (read-after-write) and WAW (write-after-write) hazards
    - Issue is GPUs have A LOT of registers
    - Instr with dependency must repeatedly lookup in scoreboard due to multiple threads
    - Alternatively, restrict number of warps that can probe scoreboard each cycle. if instr not free of dependencies, then cant issue any other instr
    - Solution, rather hold single bit per reg per warp, design contains 3-4 entries per warp; each entry identifies register that will be written by an instr that is issued but not completed
    - Usually scoreboard accessed when issued and write back; now accessed when instr in buffer and instr writes to reg file
    - Short bit vector; bit set if corresponding entry in scoreboard matched any operands in instr
    - Bit vector copied alongside instr to instr buffer
    - Instr not eligible until all bits cleared (NOR gate); bits cleared when instr writes to reg file
    - If all entries used for given warp; fetch stalls or instr discarded and fetched later
    - Two-Loop Architecture: first loop selects warp with space in instr buffer, looks PC, performs i-cache access for next instr; second loops selects instr in instr buffer without dependencies and issues execution

    - Many warps to hide latency; large register file; regs for warp execution
    - Reg File requires one port per operand per instr; reduce by simulate large number of porst using multiple banks of single-ported memories
    - Operand Collector: forms third scheduling loop
    - Logical banks can have logical banks
    - Logical banks connected via a crossbar to staging registers, buffers operands before passing them to execution
    - Arbiter controls access to banks and routes to crossbar
    - Bank is essentially d-cache for GPUs?
    - Only one value from one bank can be read at a time; delayed if conflict; a lot of delays due to conflicts and recalls of instr

    - Operand Collector Microarchitecture: staging registers have been replaced by collector units
    - Each isntr has a collector unit upon reg read
    - Collector Unit contians buffering space for data; uses scheduling to tolerate bank conflicts
    - Allocate equivalent regs from different warps in different banks; individual warps in fetch group are scheduled in round robin
    - Different warps access different banks which help reduce conflicts between writeback and read of warp
    - Operand Collector doesn't impose order between different instr are ready to issue; may allow WAR (write-after-read) hazards; if two instr from same warp are present in an operand collector; If first instr has bank conflicts, second instr can write new value to reg before first instr has read older value
    - Prevent WAR by req instr from same warp to leave operand collector to execution units in program order
    - Release-on-commit warpboard: one instr per warp
    - Release-on-read warpboard: one instr at time per warp to collect operand in operand collector
    - Bloomboard: instr level parallelism; small bloom filter to track outstanding reg reads
    - Read Dependecy Barrier: special ctrl instr used to avoid WAR

    - Struct Hazards in GPU pipelines; reg read may run out of operand collector units; mem system
    - In CPU, when struct haz encountered; stall younger instr until resolved
    - Can't do in Pipelined GPU may stall multiple warps
    - Solution is implement instr replay; recovery mech in CPU for dependent instrs
    - Instr Replay: GPU holds instr in instr buffer until completed

    - Research Direction on Reg File Architecture
    - GPU uses hardware warp schedulers to store regs of all thread in on-chip reg files
    - Reg files can be very big and take up too much space
    - To minimize area, SRAM bank accessed parallel to supply the operand bandwidth to run pipelined SIMD; uses operand collector to access multiple instr to minimize bank-conflict => consumes high amount of energy and ower

    - Hierarchical Register File: register file cache (RFC) because 70% values only read once, and only 10% read more than twice
    - RFC with FIFO for destination of instr
    - Source operand missed not loaded into RFC
    - Val evicted from RFC WB to reg_file
    - Hardware-only RFC with compile time generated static liveness info; extra bit added to instr encoding to indicate last instr consuming reg val
    - Reg read for last time marked dead in RFC
    - Combine RFC with two-level warp scheduler; restricts execution to pool of active warps, consit of small subset of warps in SIMT core; 4-8 warps
    - RFC holds only from active warps; warp removed if too long latency => flushed

    - Compile-Time Managed Register Hierarchy: Last Result File (LRF) - buffers reg value produced by last instr of active warp
    - Replaces Hard-ware managed RFC with Compile-Time Managed Operand Register File (ORF); compiler work
    - Compiler has more holistic view and can make better decision; compilter also does two-level warp scheduler

    - Drowsy State Register File: tri-modal reg file each entry can ON, OFF, Drowsy; ON normal operation; OFF doesnt retain reg value; Drowsy retains but need to be awake ON for access
    - Drowsy after each access

    - Register File Virtualization: while waiting for mem, number of live register in GPU tends to be small; 60% regs go unused; propose reg file shrinkage or double thread size;
    - Thread starts with no regs, and physical regs allocated to destination regs as instr decoded
    - Deallocation of physical reg can be enhanced by compiler analysis to determine last read of reg
    - "final read annotations"; add bit to indicate last read
    - Can spill reg to mem to save GPU reg file size
    - "metadata instr" efficiently encodes when phys regs can be reclaimed with reg lifetime liveness analysis
    - use branch divergence to account if safe to reclaim phys regs
    - rename regs instead of reclaim

    - Partitioned Register File/ Pilot Register File: partitions GPU reg_file into fast and slow register file (FRF SRF)
    - RFR: regular SRAM; SRF: near-threshold voltage (NTV) SRAMs
    - NTV SRAMs has low access energy, lower leakage power; but slower (several cycles); SRF significantly larger than FRF
    - Every warp 4 entries to FRF
    - Additional latency for SRF is handled by operand collector
    - FRF of inactive switch to low power mode with FinFET's back gate control
    - Employ pilot CTA at each kernel launch to profile most-freq-use regs for FRF

    - RegLess: no more reg file; operand staging buffer
    - Reg accessed is small fraction of total reg file capacity
    - Use compiler algo to divide kernel execution into regions
    - Regions: contiguous instr within single basic block
    - Boundary between region to limit number of live regs
    - Capacity Manager (CM): determines which warp for scheduling
    - Operand Staging Unit (OSU) - reg used in instr stored here from global mem or L1 d-cache; OSU has enough for 2 instr per cycle
    - CM maintains FSM to see if regs needed are already present

