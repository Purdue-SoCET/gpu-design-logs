
State: Everything is good and I don't need help right now.
My notes might look sparse, but thats because I take a lot of images and annotate them for context. Check onenote.

GOAL: Read Chapter 3.1,3.2,3.3, 3.6 + Videos for Background

| Concept | SIMT cores of implementation |
| Why do we want high perf programmability in GPUs? | Make verif easier (if easier to program and effective, then we can more easily verify it)
Nee: large off chip bandwidths? |
| How to manage the size of the chip bandwidths? | Caching to reduce # off chip memory access (power, energy constraints) |
| Division of the pipeline | SIMT (multiple thread) front-end, SIMD back-end |
| Scheduling loops | Instruction fetch: fetch -> idecode -> ibuffer 
Instruction issue: ibuffer -> scoreboard -> issue, SIMT stack
Register access scheduling loop: operand collector, alu, memory |
| Loop diagrams |  |
| ONE LOOP APPROXIMATION | ‘single scheduler’ – task scheduling dedicated hardware 
Unit: warp – org of threads 

Flow:

Select warp to schedule 
Warp PC to access memory to find next IS to execute 
Decode IS, get source operands from reg file, SIMT execution mask values are determined |
| Why do need execution masks? | Manage flow to execution, handling interrupts. Mask executions of things, until we need to. |
| After execution mask + source registers | Single instruction multiple data
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
(DEPTH IS THE DESIGN PARAMETER OF THE EXECUTION) |
| SIMT EXECUTION FORMAT |  |
| What is the SIMT stack? | Predicate masks |
| What is predication? | Instead of taking branches, execute regardless but we ignore the output of the branch not taken |
| What does the stack do? | When all threads can execute independently…
One nested control flow is dependent on the parent control flow branch being taken
What if we skip computation entirely when all hreads in a warp avoid a path? |
| DEFINE | ‘CPUs supporting predication have handled nested control flow by using multiple predicate registers and supporting across lane predicate tests…’
Predicate registers (hold condition bits)
They guard predication
Ex. If(a) { if (B) {} }
= p1 && p2 – just optimization?
Across lane predicate tests: testing the predicate values across the whole warp/vector 
Ex. If any threads predicate is true – exec this, or skip divergence handling if all threads predicates are true |
|  | How does GPU hardware enable threads within a warp to follow different paths through the code while employing a SIMD datapath that allows only one instruction to execute per cycle?

SERIALIZE execution of threads following different paths 
DIAGRAM below: imagine the ‘missing threads’ to be masked in the even vs odd thread |
| EXAMPLE ANALYSIS: | WE HAVE:

Can be further modeled as

With tracking the Return PC, next PC and active masks 	


What this means (1)
I added F and B to the TOS for the next possible branchines/addresses the program can take (if, else)
NEXT PC: next instruction that the warp executes 
Active mask< only the first three threads (three threads branch into block B)should execute this instruction
What this means (2)
Reach the branch on line 9, then diverge 
Next PC becomes the reconvergence address (B) in this case, not E |
| What is the reconvergence point? | Point in the program where split divergent threads come back together so they can together again
Usually the nearest guaranteed meeting spot (the post–denominator), but this is runtime dependent. |
| What is the best way to add entires to the stack following a divergent branch? | Dont want depth of the stack more than log(N), n = # threads in a warp…
Put the entry with the most active threads on stack first, then fewer ones and so on |
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

The next instruction to execute for each inactive thread (through the thread active field) |
| Example flow | Each mask is 32 bits wide (branch taken, thread - 1, branch not taken thread = 0)
Threads diverge when when executing a branch instruction
There can be multiple barrier participation masks at any point for nested control flow statement 
All threads bits = 1 at the reco vergence point (all threads can now continue in lockstep)
ENTIRE WARP Keeps ONE MASK per branch split
Example with one branch (2 masks, one for each branch)

Example with nested branches:

Stack progression in this model:
Stage 1

Stage 2: Push B, while A runs

Stage 3: Pop B, after A is finished


Stage 4:  Push B2, while B1 runs

Stage 5: Pop B2, after B1 is done running

Stage 6: Reconverge to path B, and then reconverge to the larger outer branch. |
| Use of the ‘ADD’ instruction | When thread splitting occurs, each group has a different PC (own mask, warp split)
Stack based (see previous examples) requires execution and finishing of one group at a time–slow.
Barrier bases allows the scheduler to switch freely between the subgroups (one group makes progress even if the other is stalled) |
| Use of the ‘WAIT’ instruction | Stop a warp split when it hits a convergence barrier 
Add threads to the barrier state register + change the threads state to be blocked |
| Example of the timing of stack-based convergence |  |
| Example of the timing in NVIDIA Voltage Reconvergence |  |


