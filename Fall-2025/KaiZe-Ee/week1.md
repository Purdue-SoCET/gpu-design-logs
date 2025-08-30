# Week 1 Design Log
Explicit Statement: I am not currently stuck or blocked

## Questions: 
1. How can GPU suppourt a Turing Complete model?
   - I figured that the GPU needs the CPU to tell it to do something, like GPU can't go and fetch instruction and have general action like a CPU?
  
2. Clairfy Grid | Thread Block | Thread heirarchy
    - Where does SM sit in here
    - Why is the lower two (x,y,z) addressable

# Chapter 1 Intro
- 1.1 Landscape of Computation Accelerators
  - Moore's Law -> Transistor reduction
  - Dennards Scaling -> Power Consumption is lowered
  - TPU is a DNN specific architecture
    - Argument made that still need GPU due to traditional programming language
  - GPUs support a Turing Complete Model?<br><br>
  
- 1.2 GPU Hardware Basics
  - GPUs need CPU to access I/O (like what I thought)
  - Discrete GPU != Integrated GPU
    - Discrete uses GDDR
    - Integrated uses single DRAM
  - Memory Data Flow
    - Old Discrete architecture 
      - is self facilitated
      - CPU -> DRR
      - GPU -> GDDR
    - New Discrete arch (unified memory)
      - Auto Transfered using VM suppourt
        - Leads to some cache coherence problems
  - Kernel
    - Code that runs on CPU to tell what needs to be executed on GPU
    - **So how does instruction fetch occur for the GPU if the CPU tells it what to do?**
  - Streaming Multiprocessors (Compute Units)
    - "Threads on a singel core can communicate through a scratchpad memory" -> synchronize through barriers
    - "Large number of threads are used to hide the memory access latency"
  - "GPUs improved performance per unit area vs. superscalar OoO CPUs" -> more area to compute
  - Figure 1.3 -> Don't have threads that exceed the working set of the cache<br><br>

- 1.3 History of GPUs
  - Vertex shaders & pixel shaders led to first programming in GPUs
    - This then led to computing in linear algebra
    - <u>NVIDIA GeForce 8</u>
      - Write to memory addr & scratchpad -> limit off-chip bandwidth
    - <u>NVIDIA Fermi Arch</u>
      - Caching of read-write data
    - <u>AMD Fusion</u>
      - Integrated CPU adn GPU on the same die
      - Dynamic Parallelism -> enable launching threads from GPU
    - <u>NVIDIA Volta</u>
      - Tensor Cores -> Machine Learning acceleration
  

# Chapter 2 Programming Model
- 2.1 Execution Model
  - Overall Flow:
    - Discrete/Integrated
      - CPU allocates memory for GPUs use
      - Initiate transfer of input data to GPU
      - Launch computational kernel on GPU
  - Computational Kernel
    - Composed of thousands of threads
  - **SAXPY** - Ax + y (where x & y are vectors, A const)
    - ![image](Fall-2025/KaiZe-Ee/images/fig2_2.png "Figure 2.2")
      - **why does global indicate running on GPU?**
      - Let: d -> device(GPU) & h -> host(CPU)
      - saxpy:
        1. Identify offset of singular thread
        2. Thread less than number of blocks calculate
        3. Operation
      - Main:
        1. Allocate memory for the vetors
        2. Bring over data from CPU
        3. Run saxpy (<<<>>>) <-- this indicates kernel 
            - Launch n threadblocks where each threadblock has <u>(256 threads | 8 warps)</u> 
        4. Return result to CPU
      - **What does it mean by "compute kernel made up of ... hierarchy composed of a grid of thread blocks consisting of warps"** 
  - <u>Groups</u> of threads: 
    - Warps(32)
    - Wavefronts(64)
  - <u>Larger than Group</u>
    - Thread Block
    - Cooperative thread array
  - <u>Unified Memory</u>
    - Allows CPU <-> GPU memory updates (automatic, does the copying on programmer's behalf)
  - Grid | Block | Thread (Identifiers)
    - All three in the heirarch is x,y,z
      - But why does a thread need to be three dimensional?
  - <u>Scratchpad/Local Data Store</u> or <u>Software Cache</u> 
    - is "Shared memory" per Streaming Multiprocessor (SM)
    - Allows threads within a CTA/Thread Block to communicate
      - Each CTA within the SM has some space on the scratchpad
  - <u>Global Data Store</u>
    - Only for AMD, for scratchpad for ALL cores on GPU
- 2.2 GPU Instruction Set Architectures
  - NVIDIA GPU ISA
    - Parallel Thread Execution (PTX) ~= standard RISC ISA
    - Similar also to intermediate representation IR (before optimization)
    - Need to Compile down to ISA suppourted by GPU
      - Streaming ASSembler (SASS)
      - PTX(IR) -> SASS(ASSMB) conversion done by:
        - GPU Driver
        - program ptaxas <- within NVIDIA's CUDA Toolkit
    - decuda
      - Disassembly of SASS
      - (cuobjdump) Led to partial documentation of SASS (by NVIDIA)
        - List of assembly opcodes no details on operand or ins semantics
      - Similar projects for following architectures<br><br>
    - Some architectural details: 
      - Explicit Dependency checking via scoreboard
      - Explicit-dependence lookahead
      - One control instruction for every three regular instruction (Maxwell/Pascal architecture)
        - 64 bits contain three groups of 21 bits
          - Stall count
          - Yield hit flang
          - Write, read, and wait dependency barriers
      - Register reuse flags on regular instructions
      - Operand reuse cache starting from Maxwell
  - AMD Graphics Core Next ISA
    - Released complete hardware-level ISA spec.
    - Virtual ISA -> HSAIL
    - Seperate scalar and vector instructions
      - s_ & v_ (prefacing for instructions)
    - AMD GCN arch -> within each **compute unit (SIMT CORE)**
      - one scalar unit w/ four vector units
      - VUs run v_ ins
      - SUs run s_ ins 
        - compute 32bit vals shared by **ALL** threads in a wavefront (64 threads)
      - scalar ins -> control flow handling
        - "exec" reg confrims/denies individual vector lanes for SIMT
    - <u>masking for control flow handling 3.1.1</u>
    - Architecture details: 
      - S_WAITCNT instruction
        - enable data dependency resolution for long lat operations
      - Each wavfront (64 threads) have three counters for outsanding ops per type:
        - Vector memory count
        - Local/global data store count
        - Register export count

      - Compiler|programmer inserts S_WAITCNT so wavefront waits until num. of ops drop below treshold
