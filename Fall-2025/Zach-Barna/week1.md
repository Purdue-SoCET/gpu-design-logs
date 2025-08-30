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
- 