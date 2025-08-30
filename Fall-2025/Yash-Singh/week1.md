
State: Everything is good and I don't need help right now.

GOAL: Read Chapter 1 and 2 of the textbook. Notes below.

Chapter 1

| Point | About |
| --- | --- |
| What is Denard Scaling? | Scaling of transistor size to performance classical rules |
| Do clock frequencies scale with the size of the transistors? | Not any more—frequencies improve much more slowly now.Need better architecture. |
| What kinds of hardware specialization improve efficiency? | Vector hardware eliminates overheads of instruction processing.Scalar processor repeatedly [OVERHEAD: loop control, branching, etc.] does [if (OVERHEAD: getting instruction from memory/cache more than once) -> id (OVERHEAD: decoding it more than once)-> iexec ] the same instruction for each element.Vector operates on entire vectors with ONE instruction (same recipe, different ingredients. Fill in the blanks instead of rewriting it again and again.)Minimizing data movement: complex operation that do math to avoid access to large memory arrays for multiple, smaller, simpler operations. |
| Tradeoff between efficiency and flexibility? | Efficiency is gained by making more application specific things. But we need flexibility for hardware systems. |
| Turing Complete Programming Model | Any computation can be run given enough time and memory. |
| Why have a GPU and a CPU? | CPU initiates the computation.Not enough API’s with I/O for GPU (most assume some CPU) |
| Discrete vs. Integrated GPU-CPU Setup | Different memory architectures (DDR for FPU, GDDR for GPU).Optimized for latency vs. throughputSame memory technology (for low power devices, LPDDR) |
| What is the computational flow from the CPU to the GPU? | Version dependentDiscrete: both cpu and gpu allocate space for data structure in DDRAM and GDDRAM memory. CPU initates data transfer from the cpu -> gpu.Pascal architecture: automatic data transfer from cpu-> gpu. (UNIFIED MEMORY)Newer: integrated, no transfer is needed….BUT! cache coherence problems may be there. |
| Cache Coherence | Ensure all processors see the same up to date value of the shared memory.Ex.Some memory location ‘X = 0’.CPU: load x -> CPU cacheGPU: load x -> GPU cacheCPU: write X = 5-> CPU Cache (X = 5)DNEgpu cache X = 0, or memory. STALE. |
| Continued Computational Flow | CPU: initiate computation on GPUGPU Computing Application: Computes what code to be ran on the GPU (kernel)CPU: computes # of threads to run, where the threads should source dataCPU: driver communicates: kernel, # threads, data location to GPUDriver: translates info, make it memory accessibleDriver: signals GPU for new computations |
| Generic GPU Arch | Each core execs SIMT programCores communicate through a scratchpads + syncing |
| If the goal is throughput, we need high memory bandwidth. How can this be done? | Parallelism in the memory system : multiple memory channels…need to supply memory/data fast enough for a GPU.…More ‘lanes’ = get more data at the same time.GPU memory is partitioned:LLC ->‘last level cache’ shared across these partitions.Gpu is connected to this network : core access diff mem. Partitions in parallel.Generic vs. Xeon Phi model: |
| Memory controller | Manages communication between processor and DRAM (timing signals and commands for the DRAM chips) |
| CPu vs GPU arch, performance variance with the number of threads: | Multicore -> multithrerad region performance;Multithreading ‘hides’ off-chip latency |
| GPU Energy requirements | It takes a lot of emergy for the computation and data accesses. |

Chapter 2

| CPU vs GPU hardware implementation execution models | IDEA: each thread within a kernel can execute the same program but can follow a different control flow.Ex. SAXPY computation of a vector (scalar value A x scalar value X + vector value Y )CPU implementation:Very linear flowCUDE code line by line analysis:13: invoke gpu driver and allocate memory on GPUSet d_x to point to the allocated region (hold n 32 bit fpv’s)15: cp array in cpu memory (accessed through h_x) to d_x |
| --- | --- |
| What is a wrap? | Grid of thread blocks (multiple threads that are running the samne instruction on a lot of data) |
| What is a CTA? | Cooperative thread array, group of warps/thread block.L17: launch single grid of nblocks with each thread block has 256 threads; arguments from cpu code -> krnel config are in each instance of a running thread on the gpu GOT ITLike a WRAPPER. |
| How do we identify the blocks in the grids? | Grids and threads have a x y z dim as grid block and thread identifiers –like coordinates.L17: y, z = 0; only identifiable by x.L3: threadId.x = x coord of the thread within its thread block, blockID.x = x coord of the thread block within the gridHow to access? blockId.x + threadId.x = I, offset |
| Scratchpad/Shared memory | Each SM has a single shared memory / all CTAs.Acts as a software controlled cacheALSO has a global data store scratchpad memory shard by all cores on the GPU |
| How do threads within a CTA talk to each other? | Hardware supported instructions |
| How do threads across CTAs talk to each other? | Some global address space (more expensive access though) |
| What is a GPU’s ISA? | NVIDIA developed PTX, similar to RISCVFurther compiled down to the SASS ISA |
| Brief ISA version of the previous code example |  |
| See more on page 17 for the exact instructions and what they seem to do |  |
| Another model: Southern Islands Architecture | Difference from NVIDIA: separate scalar and vector instructionsUse OpenCL instead of CUDAArch: neahc SIMT core is a scalar unit with 4 vector units |
