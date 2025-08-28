State: I am not stuck with anything, don't need help right now. 

Progress:

**Discrete GPUs**
Separation of CPU and GPU memory, which feature different memory technologies (DDR vs GDDR). This allows for optimizations of different factors: latency for CPU, throughput for GPU.

**Integrated CPU + GPU**
Due to sharing memory and usage in mobile devices, DRAM tech is LPDDR.

CPU starts applications and transfers/creates data structures in memory. 
For discrete GPUs, this transfer must go from CPU to GPU memory. 
For integrated GPUs, there may be cache-coherence problems due to CPU vs GPU access of private caches. 

A CPU driver tells the GPU how many threads to run and where to connect inputs. It also performs memory translations for GPU memory and signals (to the kernel) when new computations arrive.

**Core**
SIMT programs are initiated corresponding to kernal to run on GPU cores. 
Each core had thousands of threads, which communicates to each other via "scratchpad memory" and "synchronize using fast barrier operations".
Cores all contain L1 data and instruction caches, to reduce traffic sent to lower levels of system. 
NOTE: with high computational throughput, a high memory bandwidth is necessary. This is done with parallelism with multiple memory channels.
A portion of last-level cache is included within memory partitions. Finally, memory channels are connected via an interconnect network.
Key takeaway: GPUs tolerate frequent cache-misses through multithreading.

**Programming Model**
SIMT - uses GPU SIMD parallelism to launch many "scalar" threads (aka warps/wavefronts) in *lockstep*. Each thread executes on their unique execution path and memory accesses. 
Lockstep - same instruction performed on different operands/data simultaneously. 
Computational kernel - thousands of threads, each of which executes the same program, following their unique control flows. 
SAXPY - scalar A * vector X + vector Y

**Execution Model**
Threads executed by the GPU are a part of a compute kernal, which runs a specified function, say SAXPY. 
From there, it can unloop/parallelize a for loop such that each loop iteration turns into a thread. 
These threads are organized into a "grid of thread blocks consisting of wraps" (aka cooperative thread array, CTA). They perform/execute scalar instructions.
Each thread is assigned a portion of the data and identified with grid, thread, and block identifiers. Grid and thread use x,y,z coords. 
Each streaming multi-processor (SM) contains a single shared memory, which is shared by all CTA in the multi-processor. 
