State: I am not stuck with anything, don't need help right now. 

Progress: 
## Chapter 1
### 1.1 - Landscape
GPUs are graphics processor units, capable of running general code but originally designed with the intent of accelerating graphics/videogame workloads. A GPU is better for a highly parallel task involving many threads, which can lead to large throughput increases and latency reductions or reduced power. GPUs are more flexible than specialized accelerators, leading to the term of General Purpose GPUs also being used.
### 1.2 - Hardware Basics
Generally, there is a need for I/O interface, so systems with a GPU also generally use a CPU for those purposes. If the GPU is not integrated on the CPU chip, it will have its own memory and communicate via a bus. GPU memory is specialized for throughput. GPUs support virtual memory and can leverage this for better information sharing to the CPU. 

The GPU contains many cores and executes programs designed around the concept of SIMT. Each core can run thousands of threads with the instructions it recieves. The threads can communicate with a scratchpad of memory, and latency is hidden in some way using the amount of threads when memory is missed.

There can be tasks which are better to parallelize on the CPU if the thread count is low, but for many cases this is not true. Energy efficiency is now important since dennard scaling has ended. The complexity of memory is proportional to its energy usage, so the design of memory is important. 

## Chapter 2 - Programming Model
### 2.1 - Execution Model

Important chapter. GPUs also have SIMD capabilities for when data parallelism exists. This is masked with an abstraction layer, such as APIs like CUDA and OpenCL. These allow programmers to use the GPUs many scalar threads properly. Each thread can follow its own execution and access different memory. GPU hardware With discrete hardware executes groups of these threads in a SIMD method. This is called SIMT. The CPU must allocate memory for GPU usage and initiate data transfer, then launch a GPU kernel to begin computation. 

A CPU and GPU CUDA program to do a "SAXPY" is shown. The CPU version is simple enough. The CUDA code uses cudaMalloc several times, copies memory with a function, and then invokes a saxpy method, before copying the result to the solution location. The __global__ tag indicates that the saxpy command is for the GPU. The number of threads requested is specified in triple <>. There is a grid of thread blocks that consist of warps. Groups of threads are executed together. AMD calls these wavefronts and NVIDIA calls them warps. NVIDIA warps have 32 threads while AMD wavefronts have 64. The incovation says to launch a kernel with a single grid of nblocks thread blocks, which each block containing 256 threads. 

Memory can be unified, but it does not have to be, which is the case considered here. In CUDA programming style, h_ is used for CPU pointer names, and d_ is for GPU memory. The usage of CUDAmalloc is simple enough. It is common to assign each thread a portion of the data being used. CUDA grids have x,y,z dimensions. Each thread has a fixed unique combination of positive x,y,z coords within the grid and thread block. The thread block has coordinates within the grid, and the thread has coordinates within the thread block. These are set by the kernel configuration. In this example, 256 is specified for x and this is done for y as well. These can be used by the GPU during execution. When the GPU has completed the kernel it was given, it will return control of the program to the CPU.  GPU memory is then manually copied back into CPU memory. 

Threads within a compute thread array can communicate with a per compute core scratchpad memory(shared memory, nvidia). Streaming multiprocessors(SM) contain a single shared memory. Space in shared memory is divided up among all the CTAs running on the SM. AMD calls these local data store. These memories are small, 16-64kb, and exposed to the programmer as different memory spaces. __shared__ can be used with CUDA. Scratchpad acts like a software controlled cache. GPUs have hardware caches but often miss, so using this memory can be beneficial with commonly used data. AMD GPUs also have a global data store. 

### 2.2  - GPU Instructions

#### 2.2.1 - Nvidia GPU Instruction Set Architectures

Back when there were more than 2 options for the GPU, abstraction like OpenGL was very important. When you write code, you don't want to think too much of the specific GPU being used, rather its overall architecture. CUDA is also a high level virtual instruction set, which has to be compiled into actual GPU instructions. This is called PTX(Parallel Thread Execution). PTX is similar to some RISC ASM. There exists a compiler and IR. THe PTX is converted in a process called SASS(Streaming ASSembler). EIther the GPU driver or standalone hardware can do this. Less documentation exists for this stage. PTX code looks like assembly. The advantage here is that the same PTX could be converted to different asm as the GPUs change. Some decompiler type tools exist.

#### 2.2.2 AMD Graphics Core Next Instruction Set Architecture

AMD released an ISA level specification. More useful in academic research. Virtual instruction set called HSAIL, part of heterogenous system architecture(HSA). Has seperate scalar and vector instructions. AMD architectuer has a scalar unit paired with 4 vector units.

Vector instructions execute vector units per individual thread in wavefront, scalar instructions compute one value for all threads in the wavefront. Scalar instructions relate to control flow handling.

## Questions
How does GPU SIMD compare to CPU SIMD instructions in real world tasks, some tasks I have seen in networking are too fast to wait on a dedicated GPU to respond, but how are these tradeoffs determined? What does the threads hiding latency mean?