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


