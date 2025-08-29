# Week 1 (Chapter 1 - 2)
**State**: I'm not stuck with anything!

**Progress:** Read chapters 1 & 2 from General-Purpose Graphics Processor Architectures
## Chapter 1: Introduction
### 1.1: The Landscape of Computation Accelerators
- GPU has mainly been used for graphics computing in the past, but the non-graphics computing uses are increasing drastically
- Before, performance of computing system was improved by reducing transistor sizes leading to faster operations. However, the clock frequency no longer improves as fast as it used to when transistor size decreases. **Hardware specialization** can increase performance by 500x by moving to vector hardware (eliminates overhead(non-productive work that a computer does) of instruction processing) and minimizing data movement by introducing multiple arithmetic operations avoiding access to large memory arrays
- There's a tradeoff between specialized hardware and flexibility in what types of programs can be ran (general-purpose). Modern GPUs support a **Turing Complete programming model**. This means that teh GPUs can run any programs given enough time and memory

### 1.2: GPU Hardware Basics
- GPU hasn't replaced CPUs, rather they work together. CPUs initiate the computations done on the GPU and transfers data between them. CPU has access to I/O devices which GPUs don't have. The I/O devices also lack massive parallelism which runs better on GPUs
- Discrete GPU setup is where the CPU and GPU are separate with a bus connecting them. Both CPU and GPU use DRAM memory but the technology differs. For CPU, low latency is prioritized (DDR) while for CPU, high throughput (GDDR) is prioritized. Integrated GPUs share the same DRAM memory with the CPU and the shared memory is optimized for low power (LPDDR)
- A GPU application starts at the CPU. On older GPUs, the CPU will allocate space for the data structures in both the GPU and CPU memory. The CPU will have to manually move the data to the GPU memory too. More recent GPUs, have software that automatically moves the data. On integratd CPUs and GPUs, no data movement is needed. However, if private caches exists, there might be cache-coherence problem
- There's a driver in the CPU that intiates the computation on GPU by placing the information about the kernel (specifies which code should run on GPU), number of threads, and data location somewhere in the memory where that the GPU knows of
- Modern GPUs consists of several cores and each core can execute a single-instruction multiple-thread (SIMT) program. The threads in a core communciate through a scratchpad memory and syncrhonize using fast barrier operations. Each core has its own first-level i-cache and d-cache which can act as bandwidth filter by not going all way down into memory to fetch the data needed.
- Fast computatyion requires high memory bandwidth. GPUs has multiple memory channels to provide parallelism. Each core has a memory partition that consists of memoyr channel and last-level cache. All the memory partitions are connected through the interconnection network. 
- GPUs dedicate a large area for their ALUs and less area for control logic. 
    - Guz et al model: Initially when increasing number of threads (MC region) te performance increases. As you increasess the number of threads even more, performance decreases because there's not enough space for all of the working sets and lower-level memory needs to be accessed. Lastly, when increasing the number of threads further (MT region), performance increases becauses multithreading can hide the long off-chip latency. 
- Energy efficiency has becomne importatn and is taken into account for GPU architecture. Accessing larger memory structures consume more energy

## Chapter 2: Programming Model
- Most modern GPUs use SIMD hardware but programmers are not exposed directly to the SIMD hardware. Instead, the programmers use APIs (CUDA, OpenCL) to launch scalar thread which can follow its own path and access different memory locations. At runtime, the GPU executes all these scalar threads, which is called warps 

### 2.1: Execution Model
- A GPU computation starts with the CPU who allocates memory and transfers the data to the GPU and launches a **computational kernel** (composed of typically thousands of threads)
- SAXPY: 
    1. With CUDA, allocates memory on the GPU for the values in the arrays. 
    2. With CUDA, uses cudaMemcpy to copy the content of the arrays from the CPU memory to the GPU. 
    3. In C code, a for loop is utilized. However, in CUDA, global is used to specify that the program will run on the GPU. Each iteration in the for loop corresponds to a thread running
    - A compute kernel <-- grid of thread blocks <-- warps
    4. Each thread is assigned a portion of the data. The thread needs to look up its identity in the grid of blocks of threads by identifying its x,y,z dimensions within the block. Likewise, each block has its own (x,y,z) location in the grid. blockIdx.x, threadIdx.x, and blockDim.x are used to assign each thread its "ID".  
- **Warps**:
    - A group of threads (32 for NVIDIA, 64 for AMD) that execute the same instruction. 
    - Warps can form into a larger unit called cooperative thread array (CTA) or thread block. Threads in CTA commmunicate with each other through **scratchpad memory/shared memory**. Threads in CTA can communciate through **global addresses**, but accessing these addresses can be expensive in terms of time and energy. 

### 2.2: GPU Instruion Set Architectures
***
#### Glossary: 
- **Backward compatibility**: A program that compiled for a previous generation runs on the next generation with no changes
- **PTX**: ISA for GPU developed by NVIDIA to use with CUDA
***
- NVIDIA came out with an ISA called PTX (parallel thread executation). PTX needs to be compiled down to the **SASS** (Streaming ASSember) which is the asssembly language that runs on NVIDIA GPUs. NVIDIA has only provided a list of the assembly opcode names but very little detail
    - PTX and SASS are both RiscV and use predications. Differences are e.g. PTX uses infinite set of registers while SASS uses a limited set of registers. In SASS, kernel parameters are access through non load/store instructions while the parmeters are given their own address space in PTX
- Difference between AMD and NVIDIA GPUs architectures is separate scalar and vector instructions
    - In each SIMT core in AMD GCN architecture, each scalar unit is coupled with 4 vector units. Vector instructions happen on the vector unit where each thread computes a 32-bit value. A scalar instruction executes on the sclar unit and computes a 32-bit value that's shared with all threads in the wavefront (warp)


## Questions
- The large number of threads running on a core are used
to hide the latency to access memory when data is not found in the first-level caches. **Is the latency "hidden" because the other threads can execute other instructions?**