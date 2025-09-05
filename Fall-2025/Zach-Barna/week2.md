# Explicit Statement: I am not stuck or blocked
# MIT Coursework Chapter 7: Performance Metrics
<u>Latency</u>: the delay from wen an input is established until the output associated with that input becomes valid.

<u>Throughput</u>: the rate at which inputs or outputs are processed

__Section: Pipelined Circuits__
- For combinational circuits:
  - latency = t_PD
  - throughput = 1/t_PD
- We as engineers are bottlenecked by latency of hardware components. However, we can alter the system's throughput
- Throughput is determined by t_PD, latency is determined by t_PD AND number of stages between input to output
- Pipelining typically increases latency, but will also increase throughput!
- A pipelined circuit can never have lower latency than a non-pipelined circuit

__Section: Pipeline Conventions__
- Def: A well-formed k-stage pipeline (k-pipeline) is an acyclic circuit having exactly k regs on <u>every</u> path from input to output
- Composition convention: every pipeline stage has a register on its <u>output</u>
- ALWAYS: the clock common to all regs must have a period sufficient enough to cover propogation over combinational paths + (input) register t_PD + (output) register t_setup
- Latency of k-pipeline: k * (period of system clock)
- Throughput of k-pipeline: frequency of system clock

__Section: Pipeline Methods__
- Question: why does it matter if we fail at making a k-pipeline? (e.g., we have three paths that are supposed to make a 2-pipeline, two paths have 2 regs, but one path has only 1 reg)
  - Ans: successive inputs get mixed, causing false outputs to beproduced, and differing in operation/correctness from unpipelined circuit
- Pipeline pro: increased throughput
- Pipeline cons: increased latency, "bottleneck" issue
- So once we have isolated the longest component, we cannot improve throughput any futher using just a pipeline. So how do we continue to improve performance?
  - Ans: pipelined systems can be hierarchical
  - Replacing a slow combinational component with a k-pipe version may let us decrease clock period -> decrease latency
  - But if we do this, we must account for new pipeline stages in the entire design

__Section: Circuit Interleaving__
- We can simulate a pipelined version of a slow component by replicating the critical element and alternate inputs between the various inputs between the various copies
- N-way interleaving is equivalent to N pipeline stages
- By combining interleaving and pipelining with parallelism, we can significantly improve the throughput of our systems

__Section: Control Structure Taxonomy__
- Globally timed, synchronous: most straightfoward approach, pipeline with system clock chosen to accomodate worst-case processing time. Easy to design, but can't produce high throughputs if processing stages run more quickly for some data values
- Locally timed, synchronous: can use simple handshake protocol to move data through the system, problem is that specific clock edge used to transfer data is determined by the delay of the stages themselves
- Globally timed, asynchronous: asynchronous communication at the system level for large systems leads to very complicated timing generators, and so the effort it takes to design is typically not worthwhile
- Locally timed, asynchronous: usually proves too difficult to produce a reliable design for large systems, such as modern CPUs. However, it is extremely effective for smaller use cases, such as integer division units

__Summary of k-pipes__
- Always have registers on outputs
- k regs on <u>every</u> path from input to output
- Inputs available shortly after clock i, outputs available shortly after clock i + k
- t_clk = t_PDreg + t_PD of slowest pipeline stage + t_setup
- T (Throughput) = 1/t_clk
  - more throughput -> split slowest pipeline stages
  - use replication/interleaving if no further splits possible
- L (Latency) = k/T
  - pipelined latency >= combinational latency

# MIT Coursework Chapter 15: Pipelining the Beta
__Section: Single-Cycle Performance__
- Time/Program = Instructions/Program + Cycles/Instruction + Time/Cycle
  - Instructions/Program: total count of instructions executed by program
  - Cycles/Instruction: average number of clock cycles to execute a single instruction (CPI)
  - Time/Cycle: duration of single clock cycle (t_clk)
- In single-cycle CPU: 
  - CPI = 1
  - t_clk = longest path for any instruction
  - worst case/longest path is lw instruction
  - t_clk = (roughly) t_ifetch + t_idecode + t_alu + t_mem + t_wb
  - slow
  - inflexible: instructions with smaller critical path cannot execute faster, bottlenecked by slowest instruction (lw)

__Section: Pipelined Implementation__
- Divide datapath into multiple pipeline stages to reduce t_clk
  - Each instruction executes over multiple cycles
  - Consecutive instructions are overlapped to keep CPI roughly equal to 1.0
- For pipeline CPU stages: 
  - t_clk = max {t_ifetch, t_idecode, t_alu, t_mem, t_wb}
- Ideas to keep in mind for CPU:
  - CPU has a state: PC, RF, Memory
  - There are dependencies that we cannot break
    - ex: compute next PC, write result into RF

__Section: Pipeline Hazards__ 
- Pipelining tries to overlap execution of multiple instructions, but an instruction may depend on something produced by an earlier instruction
  - data value -> Data Hazard
  - PC changes order of execution from branch/jump/exception -> Control Hazard
- Plan of attack: 
  - 1) Design pipelined CPU (ignore hazards for you)
  - 2) Handle data hazards
  - 3) Handle control hazards

__Section: Pipelined CPU__
- Mostly everything is straightforward to me except data memory
  - Data memory reads are now pipelined, not combinational. Data accesses are initiated at beginning of the MEM stage, and are returned just before the end of the WB stage
- Latency for particular instruction: 5 clock cycles
- Throughput: 1 instruction/cycle
- Clock period will be smaller, however, as each stage of pipelined CPU now has fewer hardware components
- Read regfile in RF (ID) stage
- Write to regfile at end of WB stage

__Section: Resolving Hazards__
- Strat 1: Stall instructions in the RF (ID) state until result they need has been written into regfile
  - has negative impact on instruction throughput
- Strat 2: Bypass (Forward). Route data to earlier pipeline stage as soon as it is calculated
- Strat 3: Speculation
  - guess a value and continue executing anyway
  - when actual value is available, do one of two things:
    - 1) correct guess -> continue execution, do nothing
    - 2) guessed incorrectly -> kill and restart with correct value

__Stall Logic for Data Hazards__
- Stalls increase CPI... bad!
- Introduce STALL control signal
  - if STALL
    - disables PC and RF (ID) pipeline regs
    - injects NOP instruction into ALU stage

__Bypass Logic for Data Hazards__ 
- Add bypass muxes to RF (ID) outputs
- Route ALU, MEM, WB outputs to mux inputs
- Bypass value if destination register of instruction in ALU, MEM, or WB matches source register of instruction in RF (ID)
- What to do if multiple matches?
  - No problem, select value from most recent instruction (ALU > MEM > WB)
- Question: So if we have a fully bypassing/forwarding pipeline, do we still need stalls?
  - Ans: Yes, as we have a condition called load-to-use, therefore we need load-to-use stalls in our CPU
    - Bypassing/forwarding from WB stage still saves a cycle
- Summary of Data Hazard Handling:
  - Strat 1, Stall: simple, but wastes cycles -> higher CPI
  - Strat 2, forward/bypass: more expensive, lower CPI
  - more pipeline stages -> more freqeuent data hazards
    - lower t_clk, higher CPI

__Section: Control Hazards__
- What do we need to compute the next PC?
  - for BEQ/BNE: opcode, offset, and Reg[Ra] (also PC+4, but not a big deal)
  - for JMP: opcode, Reg[Ra]
  - all other instructions are just opcode and PC+4
  - Issue: Reg[Ra] is unknown until the RF (ID) stage

__Stall Logic for Control Hazards__
- If branch or jump instruction in IF, stall IF for one cycle
- IRSrc^IF control signal introduced
- If opcode^RF == JMP, BEQ, BNE
  - IRSrc^IF = 1, inject NOP
  - set PCSEL to load branch or jump target

__ISA Issue for Branches__
- Some ISAs have more complex branches that are resolved in the ALU stage, so what?
  - we would need to inject 2 NOPs into pipeline, one into RF (ID) and IF stages

__Section: Resolving Hazards with Speculation__
- Question: What is a good next guess for the PC?
  - Ans: PC+4, as this will be the case for all instructions other than branches and jumps
    - if this guess is correct, do nothing, we are all good
    - but if this guess is wrong, meaning we have either a branch or a jump instruction, then inject NOP into the instructions that came after the incorrect guess once the branch/jump instruction is resolved
- Logic for implementing speculation:
  - IRSrc^IF control signal isimplemented/used once again
    - if opcode^RF == JMP or taken BEQ/BNE
      - IRSrc^IF = 1, inject NOP to annul the fetched instruction
      - set PCSEL to load jump/branch target

__Section: Branch Prediction__
- Always guessing PC+4 wastes a cycle on take branches/jumps, which increases CPI roughly 10%
- With deeper pipelines, taken branches waste even more cycles
- To avoid this, modern CPUs predict <u>both</u> branch condition and the target
  - This works well because branches have repeated behavior (e.g., in a loop, typically the condition will be taken multiple times before you jump out of the loop)

# GPU Textbook Chapter 3: The SIMT Core: Instruction and Register Data Flow
- Today's GPUs execute tens of thousands of threads concurrently, so if we have lots of loads/stores, it is difficult to exploit locality -> really difficult to build cache
  - But they can still be effective in reducing a sizable number of off-chip memory accesses
- But for graphics workloads, there is significant spatial locality between adjacent pixel operations, so on-chip caches are useful in this regard
- A single SIMT core is divided into a SIMT front-end and a SIMD back-end
  - The GPU pipeline/SIMT Core also consist of three main scheduling loops: an instruction fetch loop, and instruction issue loop, and a register access scheduling loop
    - Instruction fetch loop: includes blocks labeled Fetch, I-Cache, Decode, I-Buffer
    - Instruction issue loop: includes blocks labeled I-Buffer, Scoreboard, Issue, and SIMT Stack
    - Register access loop: includes blocks labeled Operand Collector, ALU, Memory (will not explore Memory in this chapter)

__Section 3.1: One-Loop Approximation__
- recap: warps are 32 threads, wavefronts are 64 threads. These will all be given a single instruction to run on many threads
- The unit of scheduling is a warp
- The hardware will select a warp for scheduling in each cycle
- In the one loop approximation, the warp's PC accesses the instruction memory to find the next instruction to execute for the warp
- After fetching instruction, we must decode it and the source operand regs are fetch from regfile
- In parallel with these tasks, we have to determine the values for the SIMT execution mask
- Each thread could potentially go down a different control path; not all threads should have the exact same execution, and the SIMT execution mask is how we accomplish this
- After execution masks and source regs are ready, execution can proceed in a SIMD manner
- Each thread executes on the function unit associated with a lane, provided the SIMT execution mask is set
- Side note: <u>function units</u> typically only support a subset of instructions, called <u>heterogeneous</u>
- All function units typically contain as many lanes as there are threads within a warp (32 threads in a warp, so 32 lanes in a function unit)

__Section 3.1.1: SIMT Execution Masking__
- We have an abstraction of individual threads which can be competely independent, but this is not how it is implemented today
- Today, this is done via a combination of traditional prediction (true/false, set/not set), along with a stack of predicate masks, known as the <u>SIMT Stack</u> 
- This helps us handle two key issues when all threads execute independently: 1) nested control flow and 2) skipping computation entirely while all threads in a warp avoid a control flow path
- The SIMT stack is at least partly managed by special instructions
- Detailing a thread running on the code in Figure 3.2 (assuming the GPU can run the C code, just for my understanding):
  - Say we have 4 threads, how would the execution look like?
  - All four threads are going to run the program similar at the start (they will all load/set variables t1-t4 in a similar fashion)
  - We run into problems when we start hitting if/else statements
  - If only three threads take the if statement, and the other thread takes the else statement, how do we ensure the threads can reconverge for correct execution?
- Each thread is given a bit for its execution/active mask for the number of possible branches it could've taken. If the thread did take that branch/control path, its mask for that path would be 1, and its mask would be 0 for the paths that it did not take.
- The current approach for GPUs is to serialize execution of threads following different paths within a given warp
- A reconvergence point is a location in the program where threads that diverge can be forced to continue executing in lock-step
- We want to reconverge ASAP to keep leveraging the parallelism of GPUs
- The SIMT Stack entries hold the Reconvergence PC for a given thread, the Next PC for the given thread, and the Active Mask of the given thread
- The earliest point in a given program execution where it can be guaranteed at compile time that threads which diverge can execute in lock-step again (reconverge) is called the <u>immediate post-dominator</u> of the branch that caused the divergence
- Question: What order should be used to add the entries to the stack following a divergent branch? 
  - Ans: To reduce the maximum depth of the reconvergence stack to be logarithmic in the number of threads in a warp, it is best to put the entry with the most active threads on the stack first and then the entry with fewer active threads. __But why? I will ask soon__

__Section 3.1.2: SIMT Deadlock and Stackless SIMT Architectures__
- We have a single warp that initializes a shared variable, a mutex, to zero, indicating that the lock is free
- Every thread will also do a atomicCAS operation on line B of figure 3.5
- The CAS first reads the contents of mutex, then it compares it to the second input, 0. If the current value of mutex is 0, then the CAS operation updates the value of the mutex to the third input, 1
- Multiple accesses by atomicCAS to any single location, made by different threads within the same warp, are serialized
- With this configuration, only one thread can have the lock at a time
- The deadlock occurs when all of the other threads need the lock to execute their share of the program, but the thread that has the lock is waiting for the other threads to provide it with something. Since neither the single thread, nor the other threads can make any progress, we are at a <u>deadlock</u>
- The fields in Figure 3.6 are used by the hardware warp scheduler and are known as <u>Barrier Participation Masks</u>. They are used to track which threads within a given warp participate in a given convergence barrier
- There is also something called a <u>Barrier State</u> that is a common point in the program following a divergent branch where the threads tracked by the barrier participation masks will reconverge
- And there is the <u>Thread State</u>, which tracks for each thread in the warp, whether the thread is ready to execute, blocked at a convergence barrier, or has yielded
- At any given time, each warp may require multiple barrier participation masks to support nested control flow
- To initialize the convergence barrier participation mask, a special "ADD" instruction is employed. All threads that are active when the warp executes this  ADD instruction have their bit set in the convergence barrier indicated by the ADD instruction
- A special "WAIT" instruction is used to stop a warp split when it reaches a convergence barrier. The WAIT instruction includes an operand to indicate the identity of the convergence barrier. The WAIT instruction is used to add the threads in the warp split to the Barrier State register for the barrier and change the threads' state to blocked. Once all threads in the barrier participation mask have executed the corresponding WAIT instruction, the thread scheduler can switch all the threads from the warp split to activate, and the SIMD flow is restored

__Section 3.1.3: Warp Scheduling__
- Each SIMT Core contains many warps, so how do we schedule them?
- To simplify this, we will assume that each warp issues a single instruction when it is scheduled, and that it cannot issue another instruction until the first completes
- One property of the scheduling order is that it allows roughly equal time to each issued instruction to complete execution (fairness)
- If the number of warps in a core multiplied by the issue time of each warp exceeds the memory latency, then the execution units in the core will always be busy
- So, by increasing the number of warps up to this point can (in principle) increase the throughput of the SIMT Core
- To enable a <u>different</u> warp to issue an instruction each cycle, it is necessary that each thread have its own registers. So, by increasing the number of warps per core will cause the register file to be very very large. So by increasing the number of warps per core, it will in turn reduce the number of cores per GPU.
- Sometimes, round-robin scheduling can be pretty good at finding locality and increase performance (great for texture maps and graphics pixel shaders). However, this scheduling is not good when threads mostly access disjoint data, such as complex data structures. It may be more beneficial for a given thread to be scheduled repeatedly to maximize locality in these scenarios (good throttling)

__Section 3.2: Two-Loop Approximation__
- One big problem with the one-loop approximation is that it only has access to the thread identifier and the address of the next instruction to issue, but does not have any knowledge of whether the next instruction to issue for the warp has a dependency upon an earlier instruction
- This is an issue because if we want to hide a long latency instruction, and we don't have the dependency information, then we would need a large number of warps on a single core to select between and pick one instruction from (see why this is an issue near the end of last section)
- To reduce the number of warps needed by ensuring we have dependency access, we have what is called an <u>instruction buffer</u> (I-Buffer) where instructions are placed after cache access
- The most straightfoward approach to an I-Buffer is to have storage for one or more instructions per warp
- To detect these dependencies, there are two traditional approaches (found in CPU archs): <u>scoreboard</u> and <u>reservation stations</u> 
- Each register is represented in the scoreboard with a single bit that is set whenever an instruction issues that will write to the register
- Any instruction that wants to read/write to a reg that has its scoreboard bit set is stalled until the scoreboard bit is cleared by the instruction writing to the reg
  - This will prevent both RAW and WAW hazards
- When combined with in-order instruction issue, the scoreboard can prevent WAR hazards as well (considering reading from the regfile is also in-order)
- To implement the scoreboard for up to 128 regs per warp  and up to 64 warps per core, we need a total of 8192 bits per core
- In newer models, however, rather than holding a single bit per reg per warp, the design contains a small number (3 or 4ish) of entries per warp, where each entry is the identifier of a reg that will be written by an instruction that has been issued but has not completed executing 
- An instruction is only eligible to be considered for scheduling once all of its bits in the scoreboard are 0 (no dependencies!)
  - Implemented with a simple n-input NOR gate (I don't know the size)

__Section 3.3: Three-Loop Approximation__
- With the three-loop approximation, we need to move past dependencies and start asking how we are going to schedule accesses to the register file within a warp 
- Naive register file implementation: reduce the size of the register file by using multiple banks of single ported memory
- If registers map to different banks, then this implementation can work, where execution can run in parallel
- However, if registers are mapped to the same bank, we may be forced to stall the pipeline to wait for some register to be read from, which will negatively impact the throughput of our SIMT core. This is where the <u>operand collector</u> comes into play

__Section 3.3.1: Operand Collector__
- In the operand collector, the staging registers have been replaced with collector units. Each instruction is allocated a collector unit when it enters the register read stage. There are multiple
collector units so that multiple instructions can overlap reading of source operands, which can
help improve throughput in the presence of bank conflicts between the source operands of individual instructions
- The operand collector uses scheduling to tolerate bank conflicts when they occur
- Warps are often in similar locations within execution, which means these warps may end up reading the same registers
- (I will need to review this later, not really understanding)

__Section 3.3.2: Instruction Replay: Handling Structural Hazards__
- Many causes of structural hazards in GPU pipelines, e.g., may run out of operand collector units in the register read stage
- Many of these hazards relate to the memory system
- What happens when an instruction encounters a structural hazard in a GPU pipeline?
- In a single-threaded in-order CPU pipeline, we can simply stall younger instructions until the instruction encountering the stall can proceed
- This is fine in the CPU apparoach, but is less desirable in a highly multithreaded throughput arch for a minimum of two reasons:
  - 1) Large regfile size along with many pipeline stages required to support a full pipeline and stall signal may (and likely will) impact critical path (negatively)
  - 2) Stalling an instruction from one warp may cause instructions from other warps to stall behind it -> will negatively impact throughput of our GPU
- To avoid these issues, GPUs implement a form of <u>instruction replay</u>, which is used as a recovery mechanism when speculatively scheduling a dependent instruction upon an earlier instruction that has variable latency
- To implement instruction replay in a GPU, instructions are held in the I-Buffer either until they have completed execution or all individual portions of the instruction have executed

__Section 3.6: Research Directions on Register File Architecture__
- On many GPU Architectures, the capacity of register files within warps is substantial and sometimes exceeds the capacity of the last-level cache
- To minimize size of the regfile storage, regfiles on GPUs are generally implemented via low-port count SRAM banks, which are accessed in parallel to supply operand bandwith required to sustain instructions on the pipeline at peak throughput
- Accessing large regfiles is very expensive in terms of energy (accesses take up dynamic energy, shear size leads to static power consumption), where nearly 10% of total GPU power consumed is by the register file on the NVIDIA GTX280
- This is the main motivation for research on regfile architectures to reduce their energy consumption

__Section 3.6.1: Hierarchical Register File__
- Introduces a <u>register file cache</u> (RFC)
- RFC alocates a new entry via FIFO replacement polcy for the destination operand of every instruction
- source operands that miss RFC are not loaded onto RFC
- Every value evicted from RFC is written back to main regfile by default
- However, many of these values are never read again, and so we extend the RFC with compile-time generated static liveness information (huh?)
- An extra bit is added to instruction codingto indicate the last instruction consuming a reg value
- A reg that has been read for the last time (how is this measured) is marked dead in the RFC, and at eviction, it will not be written back to the main reg file
- To further reduce the size of the RFC, we combine it with a two-level warp scheduler
- The two-level warp scheduler restricts execution to a pool of <u>active</u> warps (small subset of warps in each SIMT core)
- RFC only holds values from active warps
- A warp is removed from the active pool at long-latency operations. When this occurs, the RFC entries of the warp are flushed and free up space for a different warp made active by the two-level scheduler

__Section 3.6.2: Drowsy State Register File__
- Tri-modal reg file that reduces leakage of power
- Each entry in the tri-modal reg file can switch between ON, OFF, and Drowsy mode (I am currently in drowsy mode)
- ON is the normal operation mode, OFF does not retain the value of the register, and Drowsy mode retains the value of the register, but the entry itself needs to be awaken to ON mode before access
- All non-allocated regs are in OFF mode, and all allocated regs are placed into drowsy state immediately following an access
- The idea is to keep regs from being in the ON state for as long as possible for long-latency operations where we are waiting a long time between register accesses (no need to have them on if we don't use them at the time)

__Section 3.6.3: Register File Virtualization__
- While waiting for memory operations, the number of live regs in a thread (GPU) is typically small
- This method proposes reducing the physical size of reg file by up to 50% or double the number of concurrently executing threads by using register renaming to virtualize physical regs
  - A thread starts executing with no regs allocated, and physical regs are allocated to destination regs as instructions are decoded
  - There is also a proposal of adding a bit for each operand to indicate whether it is a last read, which may require additional bits in the instruction encoding
  - This proposal makes use of VM, and the reclaiming of physical registers supported by metadata instructions
  - Branch divergence must be taken into account when determining where it is safe to reclaim physical regs

__Section 3.6.4: Partitioned Register File__
- GPU register file is partitioned into a fast and slow register file (FRF, SRF)
  - FRF is implemented using regular SRAMs
  - SRF is implemented using near-threshold voltage (NTV) SRAMs
- Compared to regular SRAMs, NTV SRAMs feature far lower access enegy, as well as much lower leakage power
- But in return, access latency to the  NTV SRAMs are far slower, and often consists of several cycles, as opposed to only one cycle in regular SRAMs
- In this work, the SRF is significantly larger than the FRF
- The main idea here is to use the FRF to service most of the access to compensate for slowness of the SRF
- The additional latency for accessing the SRF is handled by the operand collector
- The FRF is also enhanced with a low-power mode mechanism, which allows the FRF to reap the benefits of a two-level warp scheduler without explicitly scheduling warps in and out of an active pool

__Section 3.6.5: RegLess__
- Aims to eliminate the reg file completely, and replace it with an operand staging buffer
- Over relatively short spans of time, the number of regs accessed is a small portion of the total reg file capacity
- RegLess uses a compiler algorithm to divide up kernel execution into regions, which are contiguous instructions within a single basic block
- The boundary between regions is selected to limit the number of live regs
- RegLess's 512 entry OSU (Operand Staging Unit) saw slightly better performance than a 2048 KB reg file while occupying only 25% of the space (is this relative to the register file or the entire GPU?) and reducing overall GPU energy consumption by 11%