# Week 2

## Status

## Progress

### Videos

**Latency and Throughput**

Propagational delay (t_PD): Time from input to output
  
Latency: Time from an input to an associated output
  
Throughput: Rate at which inputs or outputs are 
  
Pipeline:
- Overlap to increase throughput of system
- Stage: each step is a stage

**Pipeline Circuits**

Combinational Circuits:
- Latency == t_PD
- Throughput = 1/(t_PD)
  
Pipeline Circuits:
- latency of each stage is longest delay in that stage -> determines max CLK speed
- Throughput for a stage = 1/(t_PD for that stage)
- Use Registers to store values between stages of pipeline
- Latency of a K-Pipeline = K * peroid of CLK
- Throughput of K-Pipeline = freq of CLK

**Pipeline Methodology**

- Draw lines through ciruit from top to bottom -> registers will be located at intersections
- Goal: Max throughput with fewest possible registers
- Latency = longest path
- Throughput improved by breaking up long combinational path, allowing for a faster CLK
- Too many stages if latency hurt and throughput doesn't improve
- Pipeline components to further decrease bottlenecks

**Circuit Interleaving**

- Add many instances of long stage module switch between uses of each
- Ex: 2 washers and 2 dryers -> if 1 step = 30 minutes then throughput = 2/30 or 1/15 and latency = 60 min

**Control Structure**

- Synchronous, Globally Timed: Easy to design but can be wasteful
- Synchronous, Locally Timed: Best way to build large systems
- Asynchronous, Globally Timed: Large systems can be very complicated
- Asynchronous, Locally Timed: next best idea
- t_CLK = longest stage t_PD + t_setup + t_ PD,REG
- For K pipeline: Throughput = 1/t_CLK ; Latency = K * t_CLK = K / Throughput
   
### Readings
<img width="683" height="244" alt="image" src="https://github.com/user-attachments/assets/587125fb-37af-40b3-8a25-081137b21c33" />

 **3.1 ONE-LOOP APPROXIMATION**
 
 - Each cycle:
   - The hardware selects a warp for scheduling.
   - Warps's pc finds next instruction to execute for the warp
   - After fetching, instruction is decoded and source operand registers are fetched from the register file
   - In paralel with fetching source operand, SIMT execution mask values are determined.


 - SIMT Execution Masking:
   - Presents programmer with abstraction that each thread executes independently.
   - Uses prediction and stack predicate mask (SIMT stack)
   - SIMT stack solves 2 key issues from independent threads: 1.) In nested control flow -> one branch is control dependent upon another 2.) Skipping computation entirly while all threads in a warp avoid control flow path
   - Threads are split to operate on different branches of the program
   - The SIMT stack keeps track of treads operations during split (pushing each threads: reconverge PC, next instruction PC, and active mask to stack)
   -  more active threads pushed to stack first

- SIMT Deadlock and Stackless SIMT:
  - SIMT stack can lead to SIMT deadlock: circular dependence between threads
  - To avoid deadlock, a different approach called Independent Thread Scheduling is used (replace stack with per warp convergence barriers)
  - *Barrier Participation Mask* : tracks whcih threads within a warp particiapte in a given convergence ( could be more then 1 mask for a warp)
  - *Barrier State* : tracks whcih threads have arrived at a given convergence barrier.
  - *Thread State* : tracks if each thread is ready to execute, blocked at convergence barrier (if so which one) or has yielded
  - *Thread rPC* : tracks, for each thread thats inactive, the address of the next instruction
  - *Thread Active* : bit that indicates if thread is active
  - Barrier Participation Mask size = # of threads -> if a bit is set then that corresponding thread particpates in the convergence barrier
  - Warp scheduler uses  Barrier Participation Mask to stop threads at a specific covergence barrier
  - Arbitrary depths of nested convergence -> mutliple Barrier Participation Mask at once -> special registers, general purpose registers, or software manager for storage
  - Special "ADD" instruction employs convergence barrier participation mask, all active threads in warp when this is excutes have their bit set, some diverge 
  - Scheduler is free to switch which common pc threads are active (unlike SIMT stack)
  - “WAIT” instruction is used to stop a warp splitwhen it reaches convergence barrier
 <img width="764" height="631" alt="image" src="https://github.com/user-attachments/assets/34a42da8-71c0-4e6d-9cc4-90a76d549195" />

 - Warp Scheduling:
     - In ideal memory system: fixed latency for responded memory requests -> possible to have enough warps to hide latency with multithreading
     - Reduce area of chip for a given thorughput by scheduling warps in "round robin" (warps given some fixed order and selected in that order)
     - Increasing warps upto a point will increase througput and can hide latency
     - Each thread needs its own register (avoid need to copy and restore register states between reg and memory) so increasing warps increases register file storage to execution core ratio
     - Response latency of memory depends on many variables

 **3.2 TWO-LOOP APPROXIMATION**
 
- Instruction Buffer : instructions are placed afer cache access and seperate scheduler is used to decided which of the severl instructions in the instrcution buffer should be issued next
- Allow next instruction to issue for a warp with no dependencies upon earlier instruction
- Also helps hide instruction cache misses

- Detecting data dependencies in same warp: 2 approaches in CPU -> scoreboard and reservation stations
- GPU use scoreboards: prevent Read-after-write or write-after-write by having scoreboard of registers that indicates if an instriuctoion issues a write to that register
- Can be large and expensive to access
- Rather then holding single bit per register per warp, use 3 or 4 of entries per warp (entry is identifier of a register)
- Register are flagged when a write instruction is placed into the instruction data buffer and cleared when instruction write to register file
- in two loop:
  
    1.) first loop selects a warp that has space in the instruction buffer, looks up its program counter and performs an instruction cache access to obtain the next instruction
  
    2.) second loop selects an instruction in the instruction buffer that has no outstanding dependencies and issues it to the execution units

**3.6 RESEARCH DIRECTIONS ON REGISTER FILE ARCHITECTURE**

- 

