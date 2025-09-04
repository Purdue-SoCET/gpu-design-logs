Pipelining Review:

| Understood | Throughput and latency |
|---|---|
| Pipelined circuits




Example | Divide processing of a unit into a processing the inputs, and processing/holding stable for the future stages.

Clock period is set to the maximum clock period of a stage to allow the stage to ‘see’ the values needed for an input and process it in time (before it gets overwritten)


Clock period of the system = 25 ns (from the longest processing block)
Takes two clock cycles (50 ns) to get the answer.
COMBINATIONAL CIRCUIT is a 0-stage pipeline  |
| K PIPELINE | Registered at the output of every PE stage  |
| Good vs. Bad Job of Pipelining | Idea ‘well-formed’ k pipeline circuit

BAD K-PIPELINE

Ex. B processes previous value of Y but the current value of X…and that is not good.
 |
| Technique for pipelining a circuit | 

THEN SYSTEM CLOCK PERIOD: section with a PE with the largest delay (8NS)
‘C’ component (pipeline registers on its inputs and outputs)

 |
| After isolating the most slowest element | Cannot pipeline any more than this |
| Can individually pipeline components as well | Replace slow combinational component with ‘k-pipe version’ -> decrease clock period


 |
| EMULATING A PIPELINE |  |
| INTERLEAVING MULTIPLE 
COPIES OF C | 

TLDR: the inputs are divided and grouped into even and odd, where a copy of C processes those inputs individually the output is  generated at the end, two clock cycles after it becomes available as an output.  The register at the end captures the output available to it, and holds it. Interleaving it back together. |
| N-way interleaving = N stage pipeline | 
In this case, the latency is 8 ns (8 ns before the first output), but eahc subsequent output comes 4 ns after. Thus it can be clocked at 8ns. Largest component, the is F with 5ns.

Thus T = ⅕ ns (i output every 5 ns)

L = 5 * 5 contours = 25 ns for the first output

Combine interleaving and parallelism (x2 the component and see it scale  linearly) |
| Synchronous, globally vs locally timed circuits | Handshake protocol for upstream (here’s x) and downstream (got x)



When heres x = got x are 1: data transfer is initiated (because we confirmed that we can send and receive the data)

Or can be edge dependent (without a clock)
 |
|  |  |

Pipelining the BETA notes:

|  |  |
|---|---|
|  |  |

Chapter 31.-3.3 Notes

| Concept | SIMT cores of implementation  |
|---|---|
| Why do we want high perf programmability in GPUs? | Make verif easier (if easier to program and effective, then we can more easily verify it)
Nee: large off chip bandwidths? |
| How to manage the size of the chip bandwidths? | Caching to reduce # off chip memory access (power, energy constraints) |
| Division of the pipeline | SIMT (multiple thread) front-end, SIMD back-end |
| Scheduling loops | Instruction fetch: fetch -> idecode -> ibuffer 
Instruction issue: ibuffer -> scoreboard -> issue, SIMT stack
Register access scheduling loop: operand collector, alu, memory |
| Loop diagrams | 	 |
| ONE LOOP APPROXIMATION | ‘single scheduler’ – task scheduling dedicated hardware 
Unit: warp – org of threads 

Flow:

Select warp to schedule 
Warp PC to access memory to find next IS to execute 
Decode IS, get source operands from reg file, SIMT execution mask values are determined
 |
| Why do need execution masks? | Manage flow to execution, handling interrupts. Mask executions of things, until we need to. |
| After execution mask + source registers  | Single instruction multiple data
IF SIMT EXECUTION MASK SET:
Each thread executes on a function unit associated with a lane 
 LANE: slot in the warp 
FUNCTION UNIT: artihmetic/logic pipeline for executing the instruction
EXECUTION MASK: bitmask telling which threads are active for the curr instruction
Each thread in warp is given a fixed lane tied to a  functional unit 

If not masked, the instruction in that lane is executed, else result ignored 

THE FUNCTION UNIT CAPABILITIES ARE LIMITED – heterogenous, they vary depending on the lane |
|  | All fnctio units contain lanes = threads in a warp 
We want the function units to be fast(er) in by clcking at a higher frequency (pipeline execution or depth) |
| What’s the difference between pipelining the execution vs. pipelining the depth? | EXECUTION:
Overlap diff stages of instruction (don’t just sit idle)
DEPTH: 
Number of stages the pipeline has 
Less: (shorter latency, less overhead)
More: each stage does less work (higher clock frequency), but more branch misprediction penalties 
(DEPTH IS THE DESIGN PARAMETER OF THE EXECUTION)
 |
| 
SIMT EXECUTION FORMAT |  |
| What is the SIMT stack? | Predicate masks  |
| What is predication? | Instead of taking branches, execute regardless but we ignore the output of the branch not taken |
| What does the stack do? | When all threads can execute independently…
One nested control flow is dependent on the parent control flow branch being taken
What if we skip computation entirely when all hreads in a warp avoid a path?
 |
| DEFINE | ‘CPUs supporting predication have handled nested control flow by using multiple predicate registers and supporting across lane predicate tests…’
Predicate registers (hold condition bits)
They guard predication
Ex. If(a) { if (B) {} }
= p1 && p2 – just optimization?
Across lane predicate tests: testing the predicate values across the whole warp/vector 
Ex. If any threads predicate is true – exec this, or skip divergence handling if all threads predicates are true
 |
|  | How does GPU hardware enable threads within a warp to follow different paths through the code while employing a SIMD datapath that allows only one instruction to execute per cycle?

SERIALIZE execution of threads following different paths 
DIAGRAM below: imagine the ‘missing threads’ to be masked in the even vs odd thread 
 |
| EXAMPLE ANALYSIS: | WE HAVE:

Can be further modeled as

With tracking the Return PC, next PC and active masks 	


What this means (1)
I added F and B to the TOS for the next possible branchines/addresses the program can take (if, else)
NEXT PC: next instruction that the warp executes 
Active mask< only the first three threads (three threads branch into block B)should execute this instruction
What this means (2)
Reach the branch on line 9, then diverge 
Next PC becomes the reconvergence address (B) in this case, not E 		 |
| What is the reconvergence point? | Point in the program where split divergent threads come back together so they can together again
Usually the nearest guaranteed meeting spot (the post–denominator), but this is runtime dependent. 


 |
| What is the best way to add entires to the stack following a divergent branch? | Dont want depth of the stack more than log(N), n = # threads in a warp…
Put the entry with the most active threads on stack first, then fewer ones and so on 																									 |
|  | SIMT DEADLOCK AND STACKLESS SIMT ARCHITECTURES |
| SIMT deadlock and how does it happen? | Threads are waiting for each other in a way such that none of them can ever progress
Ex. for 32 threads in a warp:
Half take path A and call some func()
Other half takes path B and doesn’t call some func()	
Path a threads wait for path B, but those threads dont hit that ‘barrier’ in the function , thus deadlock. 
THUS: all threads in a block most reach a barrier 
SIMT deadlock is like when half your friends stop at a meeting point waiting for everyone, but the others took a different path and never arrive. Everyone ends up stuck. |
| What alternatives are there to address branch reconvergence without a stack?















‘Barrier participation mask’

‘Barrier state’

‘Thread state’

‘Thread rPC’ | Replace the stack with per warp convergence barrier mechanisms 

Fields above are stored in registers (can be general purpose) and used by the ‘hardware warp scheduler’.

Track threads within a given warp which participate in a given convergence barrier

Track threads that have arrived at a given convergence barrier  
Tracks whether a thread is ready to execute, blocked at the barrier, or has yielded (yield = enable other threads to continue making progress past the barrier)

The next instruction to execute for each inactive thread (through the thread active field)
 |
| Example flow | Each mask is 32 bits wide (branch taken, thread - 1, branch not taken thread = 0)
Threads diverge when when executing a branch instruction
There can be multiple barrier participation masks at any point for nested control flow statement 
All threads bits = 1 at the reco vergence point (all threads can now continue in lockstep)
ENTIRE WARP Keeps ONE MASK per branch split
Example with one branch (2 masks, one for each branch)

Example with nested branches:



Stack progression in this model:
Stage 1
Base (empty stack

Stage 2: Push B, while A runs
Path B 
Base

Stage 3: Pop B, after A is finished
Base




Stage 4:  Push B2, while B1 runs
Path B2
Base

Stage 5: Pop B2, after B1 is done running
Base

Stage 6: Reconverge to path B, and then reconverge to the larger outer branch. |
| Use of the ‘ADD’ instruction | When thread splitting occurs, each group has a different PC (own mask, warp split)
Stack based (see previous examples) requires execution and finishing of one group at a time–slow.
Barrier bases allows the scheduler to switch freely between the subgroups (one group makes progress even if the other is stalled) |
| Use of the ‘WAIT’ instruction | Stop a warp split when it hits a convergence barrier 
Add threads to the barrier state register + change the threads state to be blocked 
 |
| Example of the timing of stack-based convergence |  |
| Example of the timing in NVIDIA Voltage Reconvergence  |  |

3.1.3 - Warp Scheduling

| Okay, we discussed how to pipeline threads…but how to order the warps? |  |
|---|---|
| IDEA:  | Assume ideal memory system with fixed latency → if we increase the number of warps ina core x issue time of each warp > memory latency, all execution units will always be busy and utilized -> more throughput per core |
|  | BUT! W e need more area for registers for each thread  |
| Round-robin scheduling | Each thread/warp is given a fixed time to run the IS. After time is done, the scheduler moves it to the back of the queue. Repeat for everything in the queue… |

```
SUMMARY:

The one loop approximation assumes that the throughput is controlled by one critical loop. For each warp, there is a compute, issue, and wait phase(s). In general, the SIMT core’s performance is approximated that a single loop of stall. Progress repeats for all the warps (instead of heterogenous warps).
```
3.2: [object Object][object Object]TWO LOOP APPROXIMATION, handling dependencies.[object Object][object Object]

| What does one loop not do? | Scheduler only knows the WARP ID and teh address of the next instruction–so we dont know if later instructions are dependent on previous ones.
Thus, we have to wait before issuing new instructions. |
|---|---|
| Solution | If we have a ‘buffer’ of sorts that can precalculate the dependencies, fetch and decode these in the instruction buffer , which is analyzed by another scheduler to determine which can safely be scheduled next +

Analogy: Teacher knows which student is next to answer, but not if thestudent is ready to answer.
Warp -> fetch -> buffer -> smart scheduler -> issue? |
| How is this instruction buffer implemented?  | First level instruction cache backed by more levels of caches.
After a cache hit / fill from a cache miss , instruction information is placed into the instruction buffer.

**CACHE HIT: data i want is already in the cache
**CACHE MISS: data is not in the cache (get it from main memory)
**CACHE FILL: moving data from main memory to cache (next time will be a cache hit)


 |
| How to detect dependencies?  | Scoreboard and reservation stations
-> R.S for removing name dependencies, introduce associative logic
-> S.B for in and out of order execution
 |
| SCOREBOARD IN A SINGLE THREADED CPU | Each register = single bit in board which is set whenever an instruction wants to write to it.
Ex. li x6, 5 (x6 in SB = 1)
Any further read/writes to this register is stalled until the bit is cleared after the instruction

In order scoreboards: 
-> instructions are issued to the pipeline in program order (prevents hazards)


 |
| HOW WILL IT TRANSFER OVER TO A GPU? | Not well–each core has ~128 per warp, 64 warps per core = 8000 bits per core for the scoreboard–not feasible.

For multi-threaded processor instructions from multiple threads might be waiting for earlier instructions to complete–thus need more READ ports.

Will need 64 warps per core, 4 operands = 256 read ports. |
|  | What if we limit the number of warps that can read per cycle? That also means we limit the ones we can schedule. What if the checked ones had no dependencies, but unchecked ones did? We wouldn’t know.  |
| ALTERNATIVE | Change where the scoreboard is accessed. 

Instruction buffer to guess potential hazards
Scoreboard updates when an instruction *WRITES* the result to a register file (more precise?)
IDEA: instead of tracking every register, I just track the ‘active’ registers that are in flight (issuing) and unavailable.


 |
| What if all the registers entries are used up for the warp? | Fetch stalls for ALL warps/INSTRUCTION is discarded, and must be fetched again |

```
SUMMARY:



```
[object Object][object Object]3.3: THREE-LOOP APPROXIMATION: USE OF AN OPERAND COLLECTOR AS  A SCHEDULING LOOP[object Object][object Object]

| NAIVE BANKED REGISTER FILE MICROARCH | 


 |
|---|---|
| EXAMPLE TIMING ISSUE: | 

Prioritized in order of when the instruction is issued (in what cycle). Earlier instructions take priority. |
| OPERAND COLLECTOR MICROARCH | 

Each instruction gets a collector unit (multiple units so multiple instructions can overlap reading of source operands = more throughput when BANK CONFLICTS happen in source operands of instructions) |
| SWIZZLED BANK REGISTER LAYOUT  | 

DOES NOT address bank conflicts within a single instruction
DOES  help reduce bank conflicts between instructions from different warps  |
|  |  |
| CONSTRAINTS: | No order on when different instructions are ready to issue -> CAUSE WAR ISSUES 	
Ex. two instructions (is1 reading a register that is2 will write into)
If is1 source operand meets bank conflicts again and again, is2 can write a new value before is1 can read the correct (older) value
 |
| SOLUTION TO CONSTRAINT: RELEASE ON COMMIT WARPBOARD | AT MOST one instruction per warp executes ..but low performance.																												 |
| SOLUTION TO CONSTRAINT: RELEASE ON READ WARPBOARD  | At most one instruction at a time per warp that can COLLECT operands in the operand collector = most 10% slowdown			 |
| STRUCTURAL HAZARDS IN GPU PIPELINES  |  |
| Why do we not want stalling younger instructions until stall instruction makes progress?  | GPUs have a large register file + pipeline stages, thus stall signal can impact the critical path	
Stalling one instruction might cause instructions from other warps to stall behind it	
 |
| INSTRUCTION REPLAY | Instead of speculating, GPUs use a replay mechanism:
An instruction is issued (e.g., a memory load).
If its operands/data aren’t ready (say the load missed cache), the instruction isn’t permanently stalled in the pipeline.
The GPU scheduler drops it back into the instruction buffer.
Later, when the data is ready, the instruction is replayed (re-issued) into the pipeline.
 |

[object Object][object Object]3.6: REGISTER FILE ARCHITECTURES AND HOW THEY MATTER[object Object][object Object]

| WHY DOES THIS MATTER? | All threads need registers on chip but need a lot of dynamic and static power. |
|---|---|
| Hierarchical Register Files | Add a RFC (reg file cache) to see short lived values
Use compiler hints to determine which values to write back 
Two level warp scheduler to limit the # of active warps in the RFC	 |
| Drowsy State Register File | Trimodal power based model (on, off, drowsy, has data at a lower power mode)
ON -> drowsy after use 
Saving on leakage power 	 |
| Pilot Register File | Split files into fast and slow reg files
Fast is small but services frequent access (like constants)	
Small is larger but slower (operand collectopr works to hide the latency)
Use some sort of profiling mechanism to select high use registers to assign to the RF. 							 |
| Register File Virtualization | Handle idle registers 
Register rename to virtualize the regs and allocate them as needed  |
| RegLess | Replace the reg file with a OSU (smaller, banked buffer)
Regs are loaded regionally under compiler control
Supported with global memory and cache  |

```
Summary

RFC/ORF/LRF = cache hierarchy approach.
Drowsy RF = low-power state approach.
Virtualization = smarter allocation approach.
Partitioned RF = two-tier memory approach.
RegLess = radical redesign (no giant RF).

```
