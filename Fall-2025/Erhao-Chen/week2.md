# Week 2
statement: I am not stuck.
## progress
Finish reading chapter 2 and chapter 3.1-3.3,3.6.
## learning and key concept
### Chapter 2
### 2.1
1.	The warp is a hierarchy (or a group) that organizes the kernel that consists of thousands of threads. NVIDIA names warps which consists of 32 threads while AMD names wavefronts which consists of 64 threads. 
2.	Kernel is the instructional program sent to the grid, which consists of multiple threads. The different warps are grouped to a larger unit which is called CTA (cooperative thread array) or thread block.
3.	A grid is a complete collection of all thread blocks (CTA) that was used for kernel execution.	
4.	The line 17 indicates that the SAXPY kernel is executed to nblocks number of thread block. Each thread block contains 256 threads. We can deduct that there are 8 warps for this.
<div align="center">
<img width="400" height="561" alt="2025-09-04 132826" src="https://github.com/user-attachments/assets/fda21b6d-20e1-4863-a2f8-0503b2e4ce64" />
</div>

5.  We use h_ in naming pointer variables for memory allocated in CPU, and d_ for memory allocated in GPU. On line 13, we use cudaMalloc to ask the GPU driver to allocate memory on the GPU used by program. On line 17, cudaMemcpy means that we copy the data at address of h_x in CPU memory to the GPU at address of d_x. After executing on line 17, the data at address d_x in GPU memory is copied to the CPU memory at h_x. 
6.  CTA can communicate through a per compute core scratchpad memory and it is called shared memory. The scratch pad acted as a software controlled cache. 
7.  Threads in a CTA can be synchronized by hardware instructions, while communication between threads in different CTA is through a global address space that is accessible to all threads. Accessing global space is more time and energy consuming. 

### 2.2

This section talks about the GPU instruction set architecture (ISA).
1.	NVIDIA used their own high-level virtual ISA called Parallel Thread Execution ISA, or PTX. Also, they have Streaming Assembler (SASS) which compiles PTX down to the actual ISA on hardware, which is a native low-level process.
2.	The process of NVIDIA:
    1.	Write high level code, such as c. This is the kernel function that is instructed. 
    2.	We compile the c to PTX, which is an assembly language.
    3.	Translate it to SASS. We compiled the PTX to SASS for a specific GPU product. It is a low-level undocumented machine code that GPU cores can execute. 
    4.	The AMD uses GCN (graphics core next) architecture. It is a hardware-level ISA specification. The AMD hardware used a special scalar instruction. The scalar instruction on scalar units computes the value can be shared by all threads in wavefront(warps). 

### Chapter 3
This chapter zooms into the discovery on microarchitecture of the SIMT core itself.
overview graph of the SIMT core: instruction and register data flow
<div align="center">
<img width="645" height="209" alt="1 2025-09-04 145401" src="https://github.com/user-attachments/assets/4fb810f2-44fa-425b-9023-2bcce1ecbcba" />
</div>

### 3.1

1.	One loop process for executing a single instruction for one warp:
    1.  In each cycle, the hardware selects what specific warp to work on.
    2.  Fetch instruction: We use the warp’s program counter to fetch the instruction from instruction memory to find the next instruction to execute for the warp.
    3.  Decode and Fetch operand: The instruction is decoded, and source operand registers are fetched from the register file.
    4.  Determine SIMT execution mask. It means that the hardware determines which 32 threads in the warp are active. As for the 32 threads warp, there are 32 bits consisting of 0 and 1, and 0 stand for inactive and 1 means that this thread is active. 
    5.  SIMD execution: each thread executes on the function unit on the active threads, which is decided by the SIMT mask. 
    6.  Write back: The results from the active threads are written back to the register file.

2.	In GPU, warp can be executed over several clock cycles. This can be achieved by clocking the function to achieve high performance while increasing energy consumption. There are 2 ways to increase clock frequency:
    1.  Pipeline execution
    2.  Increase pipeline depth     
3.	Threads are working independently and individually. 
4.	SIMT stack is a memory in SIMT core that can keep track of different paths that threads in a warp when they diverge at a branch jump such as if statement.
5.	The SIMT stack employed by GPUs can handle both nested control flow and skipped computation. 








## Questions

## Plan

