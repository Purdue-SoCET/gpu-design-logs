# Week 1
- State: Finished and not encountering any obstacle.
- About this: Chapter 1&2

## 1.1 THE LANDSCAPE OF COMPUTATION ACCELERATORS
clock frequencies improve much more slowly as devices become smaller. Improving performance requires more efficient hardware architectures.
 
hardware specialization ->  up to 500x energy efficiency
 - vector hardware
 - reduce data movement -> avoid large memory access

modern GPUs support a Turing Complete programming model -> about 10x more efficient than CPUs

## 1.2 GPU HARDWARE BASICS
GPU is unlikely to replace CPU
- GPU is not an independent device
- Always combined with CPU
- Need CPU to access I/O devices at start/end

CPU starts GPU computation and transfers data between them.

Treat GPU as API can hide complexity, but GPU still need a nearby CPU

GPU is good at parallelism

Why not remove the CPU? I/O devices and operating system are not highly parallel -> still need CPU

<img width="1036" height="466" alt="image" src="https://github.com/user-attachments/assets/8b3f04f1-4764-4a6a-b1d4-2a2ecc4222de" />

Discrete GPU
- connect CPU via bus(PCIe)
- CPU and GPU have individual DRAM
  - CPU: DDR(low lantency)
  - GPU: GDDR(high throughput)

Integrated CPU+GPU
- Common in low-power mobile devices
- CPU and GPU share the same DRAM
- Use LPDDR to optimize power efficiency

Compare:
- Discrete: better memory system but needs bus transfers
- Integrated: unified memory, simpler transfers via cache, but less specialized

<img width="929" height="530" alt="image" src="https://github.com/user-attachments/assets/8b653a81-a0b2-4a40-ab7a-e018adde0203" />

1. Start on CPU
   - GPU computing application running on the CPU
   - CPU allocate and initialize data structures
   - Old GPU: Manually allocate space and communicate data movement
   - New GPU: Automatically transfer data by virtual memory(Nvidia calls unified memory)
   - Integrated CPU+GPU might have cache-coherence problem
2. CPU initiate GPU computation
   - GPU computing application specifies kernels(codes run on GPU), number of threads, location
   - CPU driver copies info to GPU memory and signal GPU to start new computation
3. GPU kernels and multithread
   - GPU has many cores
     - Nvidia: streaming multiprocessors(SMs)
     - AMD: compute units(CUs)
   - Each core executes the kernel in SIMT (single-instruction multiple-thread) mode
     - SIMT: execute the same instruction in multiple threads even the results might be the same
   - Each core can run ~1000 threads
   - Threads communicate via scratchpad memory
   - Each core has first-level caches
   - Use massive threads to hide memory latency when cache missed

<img width="694" height="407" alt="image" src="https://github.com/user-attachments/assets/6c324874-4f91-422c-b5e1-191f4fc428f3" />

Performance Balance
- Balance high computational throughput with high memory bandwidth for high performance
- Insufficient threads -> performance valley

Architectures:
- CPU: few threads + large cache -> great performance until cache overflows
- GPU: many threads hide memory latency -> stable performance despite cache missed

Energy
- Accessing large memory structures can consume as much or more energy as computation
- Reducing memory accesses and improving cache efficiency

## 2.1 EXECUTION MODEL
Serial on CPU
```c
void saxpy_serial(int n, float a, float *x, float *y)
{
	for (int i = 0; i < n; ++i)
		y[i] = a*x[i] + y[i];
}
main() {
	float *x, *y;
	int n;
	// omitted: allocate CPU memory for x and y and initialize contents
	saxpy_serial(n, 2.0, x, y); // Invoke serial SAXPY kernel
	// omitted: use y on CPU, free memory pointed to by x and y
}
```

Parallel with CUDA
- Break loop into many threads
1. Allocate memory and transfer to GPU
2. Indicate which function should run, number of threads and signal GPU to start computation(`saxpy<<<nblocks, 256>>>(n, 2.0, d_x, d_y);`)
3. Copy results back to CPU(`cudaMemcpy( h_y, d_y, n * sizeof(float), cudaMemcpyDeviceToHost );`)
```c
__global__ void saxpy(int n, float a, float *x, float *y)
{
	int i = blockIdx.x*blockDim.x + threadIdx.x;
	if(i<n)
		y[i] = a*x[i] + y[i];
}
int main() {
	float *h_x, *h_y;
	int n;
	// omitted: allocate CPU memory for h_x and h_y and initialize contents
	float *d_x, *d_y;
	int nblocks = (n + 255) / 256;
	cudaMalloc( &d_x, n * sizeof(float) );
	cudaMalloc( &d_y, n * sizeof(float) );
	cudaMemcpy( d_x, h_x, n * sizeof(float), cudaMemcpyHostToDevice );
	cudaMemcpy( d_y, h_y, n * sizeof(float), cudaMemcpyHostToDevice );
	saxpy<<<nblocks, 256>>>(n, 2.0, d_x, d_y);	// START COMPUTATION, a single grid consisting of `nblocks` thread blocks where each thread block contains 256 threads.
	cudaMemcpy( h_x, d_x, n * sizeof(float), cudaMemcpyDeviceToHost );	// MIGHT BE WRONG
	// cudaMemcpy( h_y, d_y, n * sizeof(float), cudaMemcpyDeviceToHost );
	// omitted: use h_y on CPU, free memory pointed to by h_x, h_y, d_x, and d_y
}
```
To assign data to each thread, use grid/block/thread with x, y, and z dimension

Threads within a CTA(Cooperative Thread Array) communicate via shared memory (scratchpad).

Grid -> Block -> Thread
- Grid: many blocks(CTAs)
- Blocks: many threads, also called CTA(Cooperative Thread Array) in Nvidia
- Threads: Smallest executable unit
- Wrap: 32 threads(Nvidia)
- Wavefront: 64 threads(AMD)

SM(Streaming Multiprocessor)
- control lots of CTAs(not grid).
- Each SM has a internal shared memory, cannot be shared accross SMs.

Synchronization
- Same CTA: threads can sync with barriers(fast)
- Across CTAs: must use global memory(slower, more energy)

Efficiency
- Predict and reuse frequently accessed data → avoid cache misses and improve efficiency

## 2.2 GPU INSTRUCTION SET ARCHITECTURES
GPU ecosystem evolves with instruction set.

###  2.2.1 NVIDIA GPU INSTRUCTION SET ARCHITECTURES
PTX: Parallel Thread Execution ISA
- virtual ISA, similar to RISC
- provides backwards compatibility across GPU generations
SASS: Streaming ASSembler
- hardware ISA
- documentation not fully revealed

PTX -> compiled by driver/CUDA Toolkit -> SASS

### 2.2.2 AMD GRAPHICS CORE NEXT INSTRUCTION SET ARCHITECTURE
Southern Islands
- hardware ISA
- helped researchers build low-level simulators
- Compute Unit = 1 scalar unit + 4 vector units
  - Vector: compute different 32-bit values per thread in a wavefront
  - Scalar: compute and share a value in a wavefront -> avoid redundant works
  - exec: special register used to predicate execution of individual
 vector lanes for SIMT execution
HSAIL
- virtual ISA for portability across devices

Difference
- NVIDIA: only vector instructions
- AMD: separates scalar and vector instructions
