# Explicit Statement: I am not stuck or blocked
# GPU Design Log Week 1 - Chapters 1 & 2 Reading Notes
# Chapter 1: Introduction
Section 1.1
- Clock  frequencies are now improving much slower as devices become smaller due to the scaling of transistors failing to follow previous patterns. Therefore, improving performance now requires finding more efficient hardware architectures, hence the need for GPUs
- Vector hardware in GPUs improves the efficiency by almost 10x by eliminating overheads of instruction processing as in traditional CPU architectures
- Other part of gaining performance is due to minimizing data movement, can be achieved by performing operation that does multiple arithmetic operations without making accesses to large memory arrays
- In addition to GPUs used for ML, GPUs are also Turing Complete (any computation can be run given enough time and memory)
- For software that can make full use of GPU hardware, GPUs can be significantly more efficient than CPUs
  
Section 1.2
- GPUs are either combined with a CPU on a single chip or by inserting an add-in card containing only a GPU into a system containing a CPU
- As of right now, CPU is still necessary (GPU can't completely take over), as I/O device software and OS services would lack major features, such as parallelism that allows them to run on the GPU (because GPU always relies on communication initiation from CPU... I think)
- DRAM spaces separated in discrete GPU systems (system mem for CPU (DDR), device mem for GPU (GDDR))
- CPU DRAM optimized for low latency, GPU DRAM optimized for high throughput
- Single DRAM space + same memory technology for integrated GPU systems
- GPU computing app starts on CPU
- More recent discrete GPUs have software and hardware support to transfer data from CPU mem to GPU mem automatically, done via VM support on both CPU and GPU
- No programmer-controlled copying from CPU to GPU mem is necessary on integrated GPU systems, but there can be cache-coherence issues on these systems
- Before computation starts on GPU, GPU computing app determines which code it should run, and which code should be offloaded
- CPU portion of GPU computing app determines number of threads and where these threads will look for data
- CPU driver will tell GPU kernel to run, num of threads, and data locations via a memory accessible location by the GPU, and then tells GPU it has computations to perform
- Each GPU core runs a SIMT program corresponding to kernel
- Threads on a single core communicate via scratchpad mem
- **Side note:  A <u>memory partition</u> is a distinct, separate section of RAM created by OS to hold a specific process/program, preventing it from interfering with other programs/system components**
- Each core also has L1 i+d caches, necessary for reducing number of memory accesses
- GPU parallelism is provided by incorporating multiple memory channels
- GPUs can get better performance compared to CPUs by focusing more on ALUs than control logic

# Chapter 2: Programming Model
Section 2.1
- Warp: group of scalar threads, typically 32
- Code carefully optimized for one GPU architecture may perform poorly on another
- **<u>SAXPY</u>: Single precision scalar value A times vector value X plus vector value Y**
- Threads that execute on the GPA are part of a compute kernel specified by a function
- The CUDA keyword __global__ indicates the kernel functional will run on the GPU
- Each iteration of a for loop in CPU-only C code is translated into an individual thread
- The number between the triple angle brackets (<<<>>>) specifies the number of threads 
- The threads that make up a compute kernel are organized
into a hierarchy composed of a grid of thread blocks consisting of warps
- Warps are grouped into larger units called Cooperative Thread Arrays (CTA) or thread blocks
- The number 256 in the triple bracket angles indicates each thread block should consist of 256 threads, and the nblocks variable in the same triple angle brackets indicates the compute kernel should launch nblocks thread blocks
- Unified Memory transparently updates GPU memory from CPU memory and vice versa
- We use the prefix h_ in naming pointer variables for memory allocated in CPU memory and d_ for pointers for memory allocated in GPU memory
- Common strategy in parallel programming is assigning each thread a portion of the data for executions
- To do this, each thread on the GPU can lookup its own identity within the grid of thread blocks containing threads
  - Each thread has an x,y,z coordinate identifier of non-negative integers within the grid of thread blocks, thread blocks have x,y coordinates within the grid, and the grid has an x coordinate
- Threads within a CTA/thread block can communicate with each other via scratchpad memory called shared memory
- Each SM contains a single shared memory
- The space in the shared memory is divided up amongst all CTAs/thread blocks on that particular SM
- Threads within a CTA can synchronize efficiently using hardware support, threads in different CTAs can communicate but do so through a global address space that is accessible to all threads
- Access to the global address space is more expensive in terms of time and energy than the shared memory

Section 2.2
- NVIDIA released its own high-level virtual ISA for GPUs called the Parallel Thread Execution ISA, known as PTX
- PTX is similar to a standard RISC ISA, and also to IRs in standard optimizing compilers
- Before running PTX code on the GPU it is necessary to compile PTX down to the actual instruction set architecture supported by the hardware, known as SASS, Streaming ASSembler (lol)
- This conversion can be done by either a GPU driver or a stand-alone program within CUDA called ptxas
- NVIDIA doesn't fully document SASS so they do not need to support backward compatability at the hardware level to prevent redesign on their ISA from generation to generation
- The first column in Figure 2.4 is the address of the instruction, the second column is assembly and the third column is the encoded instruction
- Line 7 of Figure 2.4 indicates an "operand reuse cache" was added to NVIDIA GPUs, and it appears to enable register values to be read multiple times for each main register file access, leading to reduced energy consumption and/or improved performance
- Key difference between AMD GCN architecture and NVIDIA GPUs is separate scalar and vector instructions
-  In Figure 2.7, scalar instructions are prefaced with s_ and vector instructions are prefaced with v_
-  Also in Figure 2.7, exec is a special register used to predicate execution of individual vector lanes for SIMT execution 
-  A potential benefit of the scalar unit in the GCN architecture is that frequent portions of a computation in a SIMT program will compute the same result independent of thread ID
