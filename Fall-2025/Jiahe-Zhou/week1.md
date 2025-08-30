## 1.1 THE LANDSCAPE OF COMPUTATION ACCELERATORS
One key consequence is that clock frequencies now improve
 much more slowly as devices become smaller. To improve performance requires finding more
 efficient hardware architectures.
 
 hardware specialization ->  improve 500x energy efficiency
 - vector hardware
 - minimizing data movement -> avoiding accesses to large memory arrays

modern GPUs support a Turing Complete programming model -> an order of magnitude more efficient than CPUs

## 1.2 GPU HARDWARE BASICS
GPU is not likely to replace CPU
- GPU is not independent computing device
- combined with CPU
- need CPU to access I/O devices for start/end states

CPU starts computation on the GPU and transfers data between GPU.

Treat GPU as API to lower complexity -> still need a nearby CPU

GPU is good at parallelism

Why not eliminate the CPU? I/O devices and operating system services are not massive parallelism

<img width="1036" height="466" alt="image" src="https://github.com/user-attachments/assets/fdb1b66b-4c2e-44cb-8d1e-40f39dc674e7" />

Discrete GPU
- connect CPU with bus(PCIe)
- CPU and GPU have individual DRAM
  - DDR for CPU, low lantency
  - GDDR for GPU, high throughput

Integrated CPU+GPU
- Use on low-power mobile devices
- CPU and GPU share the same DRAM
- Use LPDDR to optimize power consumption

Compare:
- Discrete GPU has better memory for certain scenario but transfer data via bus
- Integrated CPU+GPU might not have specialized memory usage but transfer data via Cache

<img width="929" height="530" alt="image" src="https://github.com/user-attachments/assets/968160af-869c-4ef7-943e-45d1c0aa4a19" />

1. start CPU
   - GPU computing application running on the CPU
   - CPU allocate and initialize data structures
   - Old: Allocate space and communicate data movement
   - New: Automatically transfer data by virtual memory(Nvidia calls unified memory)
   - Integrated CPU+GPU might have cache-coherence problem
2. CPU initiate GPU computation
   - GPU computing application decides kernels(codes run on GPU), number of threads, location
   - CPU driver convey information to GPU memory and signal GPU to start new computation
3. GPU kernels and multithread
   - GPU is composed of many cores
     - Nvidia: streaming multiprocessors
     - AMD: compute units
   - Each core executes the kernel in SIMT (single-instruction multiple-thread) mode
   - Each core can run approximate 1000 threads
   - threads executing on a single core communicate through a scratchpad
   - Each core contains first-level instruction and data caches
   - Use massive threads to hide the latency to access memory when data is not found in the first-level caches

<img width="694" height="407" alt="image" src="https://github.com/user-attachments/assets/e5685e27-0d40-4b53-b565-83336cb7dd2a" />

High performance needs balance high computational throughput with high memory bandwidth -> Otherwise, waste of resources

Insufficient threads cause performance valley

Architectures:
- CPU: few threads + large cache -> performance rises, but drops when cache overflows
- GPU: many threads hide memory latency -> performance sustained despite cache misses

accessing large memory structures can consume as much or more energy as computation -> reducing memory accesses and improving cache efficiency
