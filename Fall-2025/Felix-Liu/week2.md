State: No problems so far

## Pipelining the Beta
**Resolving data hazards (RAW, etc)**
Strategy 1: Stall. Wait for results to be written into registers by freezing (fill with NOP or "bubbles") earlier pipeline stages. 
Con: decreases throughput.

Strategy 2: Bypass. Directly route data to earlier pipeline stages as soon as it is calculated. Move ALU_Out to RF stage instead of register values.

Strategy 3: Speculation. Guess a value and continue executing anyway. When the actual value is available: 
Guess correctly: do nothing.
Guess incorrectly: kill/flush and restart with correct values. 
Note: this strategy is used specifically for control hazards. 

## The SIMT Core: Instruction and Register Data Flow
Three loops within the GPU pipeline: instruction fetch, instruction issue, and register access scheduling.
Approximation: good-enough picture of an implementation.
**3.1.1: One Loop Approximation**  
The unit of scheduling is a warp. Warps are selected by hardware for scheduling during each cycle. Their PC is used to access instruction memory to find the next instruction for warp. After fetch and decode, source operand registers are fetched from the register file. Simultaneously, SIMT execution mask values are determined (parallel with source operand register fetch). 

Next, SIMD execution proceeds. If the SIMD execution mask is set, the thread executes on the function unit associated with a lane. Like CPUs, function units are heterogeneous: only supports a subset of functions. In name only, function units contain as many lanes as there are threads in a loop. However, several GPUs execute a single warp in several clk cycles. This is done with a higher clk, resulting in higher performance/unit area but increased energy consumption. Higher clk can be achieved via pipelining execution or increasing pipeline depth. 
**SIMT Execution Masking**
Functionally, SIMT provides the programmer with the abstraction that individual threads execute completely individually (not in performance). This can potentially be achieved via prediction alone (how??). In reality, this is done via a combination of traditional predication and a stack of predicate masks: the SIMT Stack.
The SIMT stack handles two issues that emerge from independent thread execution: nested control flow and skipping computation (from trying to avoid control path). Nested control flow is when one branch is control dependent upon another. 
Divergence: branch instruction causes threads to execute different instructions. Threads are split so that each takes a "divergent" path and reconverge after instructions are executed. While divergences occur, the execution of threads are serialized such that different paths with a warp can occur and others are stalled/masked off. 
To do this, each entry on the stack has 3 values: reconvergence program counter (RPC), address of next instruction (Next PC), and an active mask. Each clk cycle, divergent threads iterate and change while other threads stall and wait. This is done by new entries being added to top of stack (TOS). The next instructions the warp executes is determined by Next PC in TOS entry.
Note how diverging points turn into multiple entries, and how reconvergence occurs after said entries are executed. 
Reconvergence point: when divergent threads can continue in lock-step. 
Note: it is best to pick the most active/diverging threads on TOS to execute first. 
**3.1.2 SIMT Deadlock and Stackless SIMT Architectures**
Dead-lock condition: "SIMT Deadlock", a problem for stack-based implementations. 
**SIMT Deadlock**
Basically, this can occurs with atomic instructions that act on multiple dependent registers/operands, like a compare-and-swap instruction. When multiple threads try to access a single location, these accesses are serialized rather than executing in parallel (does this happen because the active mask needs to turn on and off several threads?). Thus, one thread will exit the loop while the others stay. The thread outside the loop will be unable to execute the instruction to free the other threads, leaving them to "spin" and loop indefinitely. 
Solution: replace stack with per warp convergence barriers. 

**Convergence Barrier Participation Mask**
Consists on Thread State, Thread rPC (reconvergence PC), Thread Active, Barrier Participation Mask (BPM), and Barrier State, all held in registers accessed by hardware warp scheduler. Each BPM is used to track which threads in a given warp participates in the convergence barrier. There may be more than one BPM per given warp.
Common case: threads will wait for each other to reach a common point (reconvergence point?) following a diverging path to reconverge together. 
Barrier State tracks which threads have arrived at a given convergence barrier.
Thread state tracks whether each warp is: ready to execute, blocked at convergence barrier, or has yielded. Yielded state can be used to enable other threads to move on past the convergence barrier during otherwise a SIMT-deadlock. 
Thread rPC and Active are identical to stack, but for one thread (active field is one bit). For 32 threads/warp, the BPM has 32 bits. Thus, the BPM is used by the warp scheduler to stop threads at a convergence barrier location. For nested loops, multiple BPM may be required. 

To initialize, a special ADD instruction is employed such that all active threads that executes this have their bit set (by the ADD instr) in the convergence barrier. During divergence, the schedulers will select a subset of threads with common PC to update the Thread Active field (warp split). This allows the scheduler to freely switch between groups of diverged threads, allowing for more progress when some threads are locked and others aren't. 
WAIT: instruction that stops a warp split when it reaches a convergence barrier. An operand of this instruction indicates the identity of the barrier. This instruction adds the threads in the warp split to the Barrier State register and changes said state to "blocked". Once wait is executed by all threads, the thread scheduler can switch back threads to active and SIMD efficiency is maintained. 
YIELD: swapping between warp splits. 
**3.1.3 Warp Scheduling**
Approximation: each warp issues only one instruction when it is scheduled. Additionally, it is not allowed to issue another instruction until the first instruction finishes. 
This latency can, in theory, be hidden using multithreading of warps. This assumes ideal memory system with fixed latency.
Thus, with round robin scheduling (fixed scheduling order, say by thread id), equal time is given to each instruction to complete execution. 
If  ***warp-count * issue-time/warp > memory latency***, then execution units in core will remain busy, increasing throughput/core. 
However, to enable different warps to issue instructions each clk cycle, each thread must have its own registers (to avoid copy/restore between registers and memory). Thus, more warps/core leads to increased chip area for register files, leaving less for execution units. Thus, more warps/core -> less cores/chip.
Additionally, response latency of memory depends on app locality properties and the resulting contention by off-chip accesses. Said locality property can encourage and/or discourage round robin scheduling. 
Pro-round robin
\- Shared data between different threads at similar points. It is good for threads to make equal progress to have more on-chip cache hits (encouraged by round robin).
\- DRAM access is also encouraged.
Anti-round robin
\- When threads access disjoint/different data, threads should be scheduled repeatedly to maximize locality. (Rogers 2012!) 

**3.2 Two-Loop Approximation**

Flaw of one-loop: scheduler only has access to thread id and next instruction address, no knowledge on earlier instruction dependency and if it has completed execution.
To do so, you must fetch the next instruction and determine if there's data and/or structural hazards. GPU does this via instruction buffer, where instruction is placed after cache access. A separate scheduler then decides which instruction of the buffer to issue to pipeline.

Instruction memory is implemented via L1 icache with more secondary caches. It can also help with cache miss with instruction miss-status holding registers (MSHRs).

To determine instruction dependencies, there are two traditional approaches: scoreboard and reservation status. We will focus on scoreboard and simple in-order execution. Within a CPU, each register is represented in the scoreboard by 1 bit, set when another instruction writes to that register. Thus, the instruction that writes to a set register is stalled until the bit is cleared (by prior instruction writing to register). This prevents RAW and WAR hazards. 

The challenge for GPUs come when supporting multiple warps. First, there's too many registers: 8291 bits/core required (128 reg \* 64 warps). Second, instructions with dependency must constantly lookup its operands in scoreboard until prior instruction (that it depends on) writes to register. With multithreading, additional read-ports are required if all instructions are waiting. For instance, 64 warps/core \* 4 op = 256 read ports, too expensive. If you restrict the number of warps allowed to probe scoreboard, less warps can be considered for scheduling. If all instruction have dependencies, no instructions are issued, even if other unchecked instructions don't have dependencies. 

**Proposed Solution by Coon et al**

Rather than registers, the design would have a small number of entries (3-4) per warp. They would identify register dependency: written by register that has been issued, but not completed execution. Thus, this scoreboard is accessed when instruction is placed in buffer and when instruction writes to register.

When instruction is fetched and placed in buffer, scoreboard entries are compared against source and destination registers of that instruction. This creates a 3-4 bit vector, with 1 bit/entry in scoreboard for that warp. A bit is set if that entry in scoreboard matched instruction operands. This bit vector is then copied alongside the instruction in instruction buffer. Thus, instructions are only considered by scheduler when bits are cleared (via NOR gate). Said dependencies are cleared as instruction finishes and writes to register. If all entries are used up for a given warp, fetch stalls for all warps or instruction is discarded (must be fetched again).

Takeaway: First loop (fetch) selects a warp with space in ibuffer, looks up PC and performs icache access to obtain next instruction. Second loop (issue) selects instruction in buffer with no dependency and issues to execution units. 

**3.3 Three-Loop Approximation**

The 3rd loop consists of operand collector, which simulates the large number of ports using "multiple banks of single-ported memories". 
The problem with the naive approach is when instructions have multiple/all operands linked at one bank. This results in only 1 instruction being fetched, due to limited read ports (on banks). Additionally, there is competition between different instruction priorities. In summary, it takes 6 clks for 3 instructions to finish reading source registers (due to said single-port), leaving unaccessed/inactive banks.

**3.3.1 Operand Collector**

Key change: replace staging registers with collector units. This unit is allocated to each instruction's read stage. Multiple units allow for multiple instructions to overlap source operands, increasing throughput during conflict (data hazard?) between source of individual instructions. Due to more instruction and source operands, the arbiter can achieve increased bank-level parallelism.

Operand collector uses scheduling to tolerate bank conflicts, and we want less of them. One way to do this is to put equivalent registers (from different warps) into different banks. While this doesn't help singular instructions, it reduces conflicts between different warps (particularly during "even progress" warps). Thus, ports on these banks aren't overwhelmed by competing registers.

However, this implementation has WAR hazards. If first instruction's source encounters repeated bank conflicts (and stalls), the second write can write prior to first instruction reading the correct older value. A simple solution is FIFO instruction. Best implementation: bloom board. Small bloom filter to track ongoing register reads, leading to only a few % slower to correct WAR hazards.

**3.3.2 Instruction Replay: Handling Structural Hazards**

Potential causes: register read stage ran out of operand collector units. Memory system related -> thus, 1 memory instruction breaks down into multiple operations. These operations may fully take up the pipeline in a cycle. 

Traditional stall (CPU) not desirable for two reasons: 
1. Bigger register files along many more pipeline stages can lead to stall signal impacting critical path. Thus, more buffering needed, leading to more chip area.
2. Stalls also stall instructions behind in other warps.

The solution: Instruction Replay. CPUs use speculation, leading to pipeline filled with cached instruction or "wake up" instruction on loads.
GPU's don't use speculation (higher energy, less throughput). Instruction replay avoids clogging pipeline and circuit area and/or timing overheads.

**3.6 Research Directions on Register File Architecture**

Register file capacity is huge, sometimes greater than last level (L3?) cache. Thus, register files are implemented via low-port count SRAM banks. These SRAM banks are accessed in parallel (to support SIMD). This is energy intensive: GTX280 has ~10% power consumed by register file.

**3.6.1 Hierarchical Register File**

70% values produced by instruction are read once, 10% more than once. To pair with short lifetime, extend main register file with register file cache (RFC). Creates said hierarchy and reduces access frequency to main register file.

A new entry (FIFO) is allocated by RFC, for destination operand of every instruction. Source operands that miss RFC are not loaded to RFC. Evicted values from RFC go back into main register file.
Solution: Since many of these values aren't read again, the RFC is extended with "compile time-generated static liveness information". An extra bit is added to instruction, noting last instruction consuming a register value. Thus, register is marked dead in RFC after last read. At eviction, it will not go back to main register file. 

Further reduction of RFC via two-level warp scheduler. This scheduler restricts execution to pool of "active" warps, only a small subset of SIMT core. Active warp pool ~4-8 warps (of 32). RFC only holds from these warps, thus smaller. A warp is removed during long-latency operations, like global memory load or texture fetches. The RFC entries of said warp are flushed, free for a new warp to be scheduled.

Compile-time managed register file hierarchy: Last result file (LRF), which buffers register value produced by last instruction of active warps. RFC replaced with operand RF (ORF). ORF value movements managed by compiler, removing tag lookup by RFC. More holistic view of register usage, thus more optimal decisions. Compiler indicates when warp can be switched out of active pool. All live data from ORF goes back to main register file before warp switch. 

**3.6.2 Drowsy State Register File**

Registers are trimodal: on, off, and drowsy (to reduce leakage power of register file). On is normal, off doesn't retain register value, drowsy retains, but needs to be awakened (on) before access. 

Non-allocated registers are off, allocated registers are drowsy after each access. Takes advantage of long delays between consecutive access to same register (due to "fine-grained" multithreading) to spend most time in drowsy. Long GPU pipeline means additional latency from waking has no significant performance penalty.

**3.6.3 Register File Virtualization**
While waiting for memory operations, number of live registers tend to be small. Some GPU applications have 60% go unused. Thus, reduce size of register file by up to 50% or double threads by using register renaming to virtualize physical registers.

Threads start with no registers and are allocated more as instructions are decoded. This deallocation of registers can be enhanced by compiler analysis to determine last read of register. This is proposed with "final read annotations" and adding 1 bit/operand to indicate if it's a last read.

Spilling registers to to memory leads to reducing register file by 50%, with execution increased by 73% on average (!!). They reviewed older OoO CPU register renaming. Final read is done by "meta data instruction" that encode when register can be reclaimed and generate via lifetime analysis. 
Note: branch divergence must be considered when determining when it's safe to reclaim register. For example, 128 KB requires 3.8KB of renaming hardware. This can be reduced to 1KB by not renaming registers with long lifetimes. Thus, rename only when register number is larger than compiler-determined threshold. 
Additionally, use renaming to enable power gating (?) of register file subarrays. 50% reduction with no performance loss is obtainable. 

**3.6.4 Partitioned Register File**

Pilot register file: partition register file into fast and slow (FRF, SRF). Fast is normal SRAM, slow is near-threshold voltage (NTV) SRAM. These have lower access power and leakage power, but slower latency (several clks vs 1 clk). Also significantly larger. Every warp has 4 entries in FRF (serviced access most of time). Latency of SRF is handled by operand collector, FRF enhanced via FinFET back gate control (?), allowing switch to low power mode. FRF reaps benefits of two-level scheduler without scheduling warps in and out of active pool.

Rather than compiler, this uses pilot CTA at each kernel launch to profile most frequently used registers, then kept in lookup table accessible to every subsequent warp. 

**3.6.5 Regless (I don't really get this one)**

Replace register file with operand staging buffer. Over short times, number of register files accessed is small fraction of total. For ex, over 100 clks many applications used less than 10% of 2048 KB register file when using GTO (?) or two-level warp scheduler. Regless takes compiler algorithms to divide kernel execution into regions: contiguous instructions within a single basic block (vs bank?). A Capacity Manager (CM) determines which warps are executed, the registers in that region are brought to Operand Staging Unit (OSU) from backing storage area allocated in global memory and potentially cached in L1 dcaches. OSU is 8 banks, a cache to provide 2 instructions/clk. CM preloads register before issuing first instruction to avoid stalling (in new region). CM maintains FSM for each warp, indicating if registers are needed for next region present in OSU. Regless also employs register compression techniques (via affine values??). 

Result: 512 entry OSU achieves slightly better performance vs 2048 KB register file, taking 25% space and reducing overall GPU energy by 11%. (of what GPU??)
