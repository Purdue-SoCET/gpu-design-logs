# Design Log Week 1

## Status: 

I am not currently stuck or blocked.

## Reading Notes 

### Chapter 1:

**Discrete GPU system**  
  - Older: CPU orchestrates system memory to graphics memory  
  - New: Automated transfer of data from CPU to GPU memory by leveraging virtual memory  

**Integrated GPU system**  
  - Share memory space but suffer cache-coherence problems  

**CPU-GPU Flow**
  - CPU initiates computation 
  - Driver takes CPU instructions and converts them into format for GPU  
    - This includes which program (kernel) to run, how many threads, where the input data is stored  
  - This is placed in a designated location in GPU memory -> CPU signals GPU to read this  
  - GPU runs kernel  
**Basic GPU architecture**
  - GPU core:
    - Order of thousands of threads  
    - 1st-level instruction and data cache  

  - Scratchpad memory: Enables communication between threads on a single core.

  - Multiple memory channels associated with last-level cache in memory partition, cores and partitions connected via on-chip interconnect network (crossbar)  

**Notes**
  - Memory access can consume much more energy than computations  
  
  - Multithreading in GPU hides memory access latency  

### Chapter 2:
**Warps and Thread Blocks**
  - Warps == wavefronts
  - Warps are grouped into Cooperative Thread Array (CTA) or thread blocks
  - Programmer specifies thread blocks and number of threads per block in `<<<>>>`
    - This info is passed by the CPU code to the kernel config statement, then to each instance of running threads on the GPU

**Programmer**
  - GPU programming uses MIMD-like APIs while hardware is SIMD
  - `cudaMalloc()`: CPU invokes the GPU drivers and asks to allocate memory for the program
  - `cudaMemcpy()`: copy content of array from CPU to GPU memory
  - Assign each thread a portion of the data:
    - Grid, block, and thread ID (x, y, z coordinate for each type of ID)
   
**Communication and Scratchpad**
  - Threads within CTA communicate via scratchpad memory (per compute core)
  - Scratchpad -> software-controlled cache
  - Hardware cache can have frequent misses, programmer can use scratchpad to avoid this if data allows
  - One scratchpad per SM (Streaming Multiprocessor)
  - Thread block running on SM gets a portion of the scratchpad memory

**ISA**
  - **NVIDIA**
    - PTX (Parallel Thread Execution ISA):
      - RISC-like
    - SASS (Streaming Assembler):
      - Not fully documented  
      - Limited physical registers  
    - PTX compiled to SASS is done by GPU drivers or stand-alone program called ptxas
      
    - **AMD**
      - GCN (Graphics Core Next, Southern Island):
        - Uses HSAIL (virtual ISA)  
        - Separate scalar and vector instructions (`s_` vs `v_`):
          - Scalar: executes 1 value shared across threads  
          - Vector: executes per-thread values  
        - Full hardware ISA documents available
