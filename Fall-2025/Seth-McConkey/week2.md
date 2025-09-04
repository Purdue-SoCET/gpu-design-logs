# Design Log Week 1

## Status

Not stuck or blocked.

## Notes on Chapters 3 GPGPU Architecture: The SIMT Core

- GPUs must have large off-chip bandwidths because of the amount of data they operate on at a time
  - However, caches can still be effective
    - Especially because of the spatial locality of adjacent pixels in textures for graphics

### GPU Pipeline Microarchitecture

![Diagram of GPU Pipeline Microarchitecture](./media/week2/pipeline.png)

> The diagram above shows what the pipeline of a single SIMT Core looks like

- Consists of a SIMT front end and a SIMD back end, and three loop scheduling loops:
  - I-Fetch
    - Contains the blocks labeled Fetch, I-Cache, Decode, and I-Buffer
  - I-Issue
    - Contains the blocks labeled I-Buffer, Scoreboard, Issue, and SIMT Stack
  - Reg. Access
    - Contains the blocks labeled Operand Collector, ALU, and Memory

### One-Loop Approximation
> Assume there is only a single scheduler that schedulues a single a warp/wavefront at a time

- GPUs contain function units such as a LD/ST unit, FP unit, or a Tensor Core for data processing in the pipeline
- An issue with the abstraction presented that all threads execute independently is branching and control flow
  - If one thread in a warp meets the requirement for a branch, and the rest of the threads don't, something needs to happen so that the branching thread instruction is cleared but the others are not
    - This is where predication and predicate masks comes into play
#### Predication and Predicate Masks
- Unlike the RISC-V processor design we made in ECE 437, which uses branch prediction, GPUs commonly use masking of threads to handle differences in control flow between threads
- Consider an if-else statement:
  - The threads that meet need to execute the instructions in the if block will do so first, while the threads that need to execute the instructions in the else statement are masked out and effectively NOPs
  - Then, the instructions in the else block are executed, and the threads that executed the instructions in the if block are masked out
- This effectively serializes the execution of threads that follow different paths
- A stack can be used to store the order of instruction blocks to be taken at branches, and what threads to be masked for each instruction block
-   However, this SIMT stack can induce a special kind of deadlock not found in MIMD architectures called SIMT-deadlock

#### Stackless Branch Reconvergence
- Uses registers to track the state of threads in warp during branches
  - These registers contain information suchs as Barrier Participation Mask, Barrier State, Thread rPC, and Thread State
    - Thread State can be used to push threads past a convergence barrier in the case of a SIMT-deadlock
- Threads are stalled until all necessary threads meet the convergence barrier, which are located where branches reconverge after diverging
  - The WAIT instruction is used to implement this behavior
  - There may be multiple barrier participation masks and convergence barriers for nested branches
- Warp splits occur using this method of branch reconvergence, which means that the scheduler will switch between groups of diverged threads 
  - The YIELD instruction is used to implement this behavior
  - This allows forward progress for a warp when some threads have acquired a lock and othes haven't

### Two-Loop Approximation
> We now take into account the fact that multiple instructions will be executed at the same time

- This means that data dependency and structural hazards must be addressed
  - GPUs fetch instructions in advance and use an instruction buffer to pick instructions that do not have hazards with instructions currently in the pipeline









