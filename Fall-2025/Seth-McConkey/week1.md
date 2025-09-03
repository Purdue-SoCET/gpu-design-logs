# Design Log Week 1

## Status

Not stuck or blocked.

## Notes on Chapters 1 and 2 of GPGPU Architecture

### Chapter 1: Introduction

#### Motivation for GPUs:

- There were diminishing returns from increasing transistor count in traditional CPUs, so large architectural changes to allow for large parallel processing capabilities was how the GPU and other hardware such as TPUs were born.
- GPUs dedicate more die space to arithmetic logic rather than control logic, which takes up a lot of die space on modern OoO scalar processors.
- GPUs were initially used only for graphics applications, but are now used for much more such as AI/ML applications

#### GPU-CPU Systems:

##### Integrated System:
- CPU and GPU share memory
- Used mostly in mobile/low-power applications

##### Dedicated System:
- CPU and GPU have their own memory
  - Memory is transferred and communication is done between CPU and GPU memory using a bus (ex: PCIe)
- Used in higher-compute systems where higher-bandwidth memory is needed for the GPU

##### Program Flow:
- A program is run on the CPU
- Instructions for the GPU is sent to the GPU via the bus by the CPU
- Necessary info from System Memory is transferred to Graphics Memory via the bus by the CPU
- The GPU executes its kernel (instructions from CPU)
- Any modified memory in Graphics Memory is sent back to System Memory via the bus by the GPU

### Chapter 2: Programming Model

#### Kernels

- The program that runs on the GPU
- Contains thousands of threads
  - Each thread executes the same program

#### CUDA

- NVIDIA's GPU programming model
- \_\_global\_\_: keyword that indicates the kernel function/program
- \_\_shared\_\_: keyword for allocating memory to scratchpad memory shared between all CTAs (cooperative thread arrays)
- CUDA implementations of functions can look very similar to implementations created for CPUs
  - However, manually managing memory, thread count, and thread blocks is necessary in CUDA programs

#### Warps/Wavefronts
- A group of threads executed in lockstep

##### Warps
- NVIDIA terminology
- Consists of 32 threads

##### Wavefronts
- AMD terminology
- Consists of 64 threads

#### Scratchpad Memory
- Acts as a software-controlled cache
- Managed directly by the programmer
- Allows allocating memory in a shared memory pool accessible by other threads in the same CTA 
- Called shared memory by NVIDIA and local data store (LDS) by AMD
- Most effective when the programmer can identify data that is used frequently and predictably

#### GPU ISAs

##### NVIDIA: PTX and SASS
- Not backwards compatible like Intel's x86
- NVIDIA's high-level virtual instruction set architecture is called Parallel Thread Execution ISA, or PTX
- Before executing PTX code, it must be compiled down to SASS (Streaming ASSembler), which is done by the GPU driver or the ptxas program provided by NVIDIA
  - PTX allows the use of infinite virtual registers, whereas SASS uses a limited set of registers
  - Both PTX and SASS are RISC-like
- SASS has changed quite a bit over the years
  - Now includes control instructions, which gets rid of the need for explicit dependency checking
  - 1 in every 4 instructions are control instructions on Maxwell GPUs

##### AMD
- Unlike NVIDIA, AMD released a complete spec for their hardware-level ISA 
- AMD also has a virtual ISA called HSAIL
- One of the larger differences between AMD and NVIDIA's ISAs is that AMD's ISA contains separate scalar and vector instructions.
  - in AMD GCN (Graphics Core Next) architecture, each SIMT core contains a scalar processing unit and four vector processing units
    - The scalar processing unit is used for control flow handling






