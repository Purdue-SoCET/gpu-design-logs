# Week 1 

State: I am not stuck with anything, don't need help right now. 

Progress: Read chapters 1-2 from provided textbook

## Chapter 1 - Introduction

### 1.1
- Many improvements to computing systems came from scaling transistors, but that seems to have hit a ceiling. 
- To continue to improve performance we can focus on hardware architechture. Specializing and optimizing hardware architecture can improve energy efficiency significantly. 
- One challenge with this is that hardware overly specified will lack flexibility to support a wide range of programs.
- GPUs have strong interest because they are turing complete, meaning they can meet the flexibility requirement given the time and memory

### 1.2
- Due to Input/Output restrictions we cannot replace CPUs for GPUs. CPUs are responsible for controlling I/O to GPUs
- CPU uses a driver to initiate compuation on a GPU.
- The GPU computing application determines the code run on the GPU (kernel), how many threads used, and what data those threads should use.
- The driver moves this information to the GPUs memory and lets the GPU know it's there
- GPUs use multithreading to tolerate frequent cache misses (cache can't store entire working set with many threads)

## Chapter 2 - Programming Model

### 2.1
- A CPU allocates memory and transfers data to the GPU and then runs the computational kernel
- CUDA version of CPU SAXPY (C): __global__ indicates run on GPU. for loop parallelized on to different threads with malloc & memcpy. Computation starts on the kernel using CUDA syntax with # of threads.
- Groups of threads executed together are called warps.
- We will consider the case of separate GPU and CPUs where the GPU has its own DRAM memory (external GPU)
- Integrated graphics like on phones and laptops don't need this because the GPU and CPU are on a single chip.
- This means we can allocate memory on the CPU and the GPU, use h_ptr and d_ptr to differentiate respectively.
- More examples explaining how to manage memory and various other commands in CUDA in textbook
- Scratchpad data is local data (software cache) considered shared memory and allows threads with CTA to communicate

### 2.2
- PTX (Parallel thread execution) is the virtual instruction set architechture that CUDA uses (made by NVIDIA)
   - PTX is similar to RISC
- PTX is compiled down to SASS (streaming ASSembler) which is the ISA supported by the hardware.
- It is compiled using the GPU driver or a standalone program called ptxas.
- NVDIA does not fully document SASS so they don't need to fulfill backward compatibility
- There have been deassemblers (decuda) created to understand more about SASS, making it possible to develop an assembler
- AMD released a complete hardware level ISA - HSAIL as part of HSA
