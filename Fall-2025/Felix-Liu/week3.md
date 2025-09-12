State: Lost on Research Directions for GPU Memory Systems

# Memory System
CPUs contain register file, memory.
GPUs contain the same, with memory split into local and global memory spaces. 
Local Memory: private per thread, typically register spilling
Global Memory: data structures shared upon multiple threads.
Also usually has implemented programmer scratchpad memory with shared access among threads in CTAs. This allows for programmer access of address at steps in computation. Parallel loading of data into shared memory to overlap latency accesses. DRAM bandwidth is small relative to computation of instructions in same time. Off-chip memory is magnitudes more energy intense than on-chip, thus on-chip memory yields higher performance and saves energy. 

## 4.1 First-Level Memory Structures 
Focused on L1 data cache and scratch pad "shared memory" and interaction with core pipeline. L1 texture cache design.

### 4.1.1 Scratchpad Memory and L1 Data Cache
Shared/scratchpad memory - relatively small memory spaces with low latency (comparable to register) and accessible to all threads within a CTA. (aka Global Register File by Nvidia). 

A problem with this memory is potential for bank conflicts. This memory is implemented through SRAM, with one bank per lane, one read and one write port, with all threads able to access all banks. 
Bank conflict: when more than one thread access the same bank on the same cycle. Threads want to access distinct locations in that bank. 

**L1 data cache**
Contains subset of global memory address space. Some architectures contains only locations not modified by kernels, which helps avoid issues from lack of cache coherence. A programmer cares about relation of address of global/thread memory accessed by different threads in a warp.
One request can be sent to lower level caches to obtain values from one L1 data cache. If all threads in a warp access location access the same cache, then the access is said to be "coalesced". If threads in a warp access different cache blocks then multiple memory access need to be generated, then the access is "uncoalesced". Hardware must allow both. 
<img width="827" height="532" alt="image" src="https://github.com/user-attachments/assets/37fe7c3e-5e11-4e23-a93e-152245f7efb4" />

The above design is a unified shared memory and L1 data cache, featuring SRAM data array (5) which can be configured for direct mapped access or *set associative cache*. There's a replay mechanism when handling bank conflicts and L1 data cache misses. Memory access requests are first sent from load/store unit to L1 cache. Said requests consist of a set of memory addresses, one for each thread in a warp along with operation type. 

**Shared Memory Access Operations**
Arbiter determines if requested addresses will cause bank conflicts. If one or more bank conflicts, the arbiter splits the request in two parts:

1. Addresses for subset of threads which don't have conflicts. Accepted by arbiter for further processing by cache. 
This portion request bypasses tag lookup inside tag unit (3) since shared memory is directly mapped. When accepting shared memory load request, arbiter schedules a writeback to register file inside of pipeline as latency of direct mapped lookup is constant in absence of bank conflicts (hash maps). 

The tag unit determines which bank each request goes to, to control address crossbar (4), which distributes addresses to individual banks. Each bank (5) is 32-bits wide and has a decoder allowing for independent access to each row in each bank. The data crossbar (6) then returns to the thread's lane for storage in register file. 

2. Addresses for threads which cause bank conflicts with those in the first part. This part is returned to pipeline and must be executed again, aka "replay". 
The tradeoff of where replay is stored: Area can be saved via replaying directly from instruction buffer, this costs more energy from accessing the large register file. A better alternative for energy is to provide limited buffering for replay in load/store unit and avoid scheduling memory access from instruction buffer when it is short on free space.  Further bank conflicts are subdivided into the same format.

**Cache Read Operations**
Since only a subset of global memory is in the L1 cache, the tag unit will check if data is present in the cache or not. Cache access is restricted to one block per cycle. L1 cache is 128 bytes, further split into four 32-byte sectors which corresponds to minimum size of data that can be read in a single access (GDDR5). Each cache block is composed of 32-bit entries at the same row of each of the 32 banks. 

The load/store unit (1) computes memory addresses and applies coalescing rules, which breaks a warp's memory accesses into individual coalesced accesses/requests to be fed into the arbiter (2). A request may be rejected by the arbiter if resources aren't available: If all accesses are busy or no free entries in pending request table (7). 

Assuming enough resources to handle a miss, arbiter requests for pipeline to schedule a writeback to register file a fixed number of cycles in the future corresponding to a cache hit. In parallel, the arbiter requests the tag unit to check if access leads to cache hit or miss. 

In a cache hit, the row of the data array (5) is accessed in all banks and data is returned (6) to register file in pipeline. In shared memory accesses, only register lanes corresponding to active threads are updated. 

During cache misses, the arbiter informs the load/store unit that it must replay the request. In parallel, it sends the request to the PRT (7). The PRT is similar to CPU cache memory systems:
L1 cache architecture: similar to Miss Status Register holder (MSRH). Traditional MSHR for dcache contains block address of cache miss along, info on the block offset, and associated register that needs to be written. Multiple misses are supported by recording multiple block offsets and registers. The PRT above supports merging two requests to the same block and records information needed to tell pipeline which deferred request to replay. 

The L1 dcache above is virtually indexed and tagged, different from virtual index physical tagged CPU L1 dcache. While GPUs perform a context switch on every warp issue cycle, warps are part of the same application. Page-based VM is advantageous within GPU due to simplification in memory allocation and reduces memory fragmentation. 

After entry is allocated to PRT, a request is forwarded to memory management unit (MMU) (8) for virtual to physical address translation. Then, it is passed over a crossbar interconnect to appropriate memory partition unit. Said unit contain a bank of L2 caches along a memory access scheduler. A request also contains a "subid", used to lookup entry in PRT containing information about the request when it returns to the core. 

Once the request is loaded to the core, it passes the MMU to the fill unit (9). The fill unit uses the subid to lookup information about the request in the PRT. The fill unit can pass information to the load/store unit via arbiter to reschedule the load, which is guaranteed to hit the cache by "locking the line in the cache" after it is in the bank. 

**Cache Write Operations**
Write through: writes update both cache and main memory.
Write back: writes update only the cache. 
L1 dcache can support both write through and write back policies. The memory space written to determines if the write is write through or write back. Accesses to global memory in many GPGPU applications are expected to have poor temporal locality, since kernels are prone to have threads write out data to a large array before exiting. For such accesses, a write through with no write allocate can make sense. In contrast, local memory writes for spilling registers to stack can show good temporal locality with subsequent loads, justifying write back with write allocate policy. 
Data to be written is first placed in the write data buffer (WDB). For uncoalesced accesses or when some threads are off, only a portion of a cache block is written to. If the block is present in the cache, data can be written to the "data array" via the data crossbar (6). If data is not present in cache, the block must first be read from L2 cache or DRAM. Coalesced writes which completely fill a cache block may bypass the cache if they invalidate tags for stale data in cache. 

NOTE: There is still no cache coherence. To avoid issues, Nvidia GPUs only permit local memory accesses for register spills and stack data, or read-only global memory to be put in L1 dcache. There is research on L1 dcache coherence on GPUs and the need for clearly defined GPU memory consistency models. 

NOTE: what is the difference between all the mentioned memory types? data array, cache, buffer, global/local memory, etc. 

### L1 Texture Cache

Nvidia GPU architectures combine L1 dcache and texture cache to save area. 

**Standalone Texture Cache**
<img width="623" height="687" alt="image" src="https://github.com/user-attachments/assets/26427593-b8ea-4587-9cc1-5000f3a76038" />

To achieve good graphics, texture mapping is employed. An image, aka texture, is applied to a surface in a 3D model. The rendering pipeline first determines the coordinates of one or more samples (texels) within the image. Temporal locality can be exploited with adjacent pixels on the screen. 
As in the L1 texture cache above, the tag array (2) and data array (5) are separated by a FIFO buffer (3). The motivation of the FIFO buffer is to hide latency of miss requests from DRAM. The texture cache is designed assuming that said cache misses are frequent and working set size is small. Thus, the tag array runs ahead of the data array to keep them small and reflects what's in the data array's future (equivalent to round trip of miss request from memory and back). Thus, throughput is improved relative to regular CPUs, but cache hits and misses experience roughly the same latency. 

**Operation of Texture Cache**

Load/store unit (1) sends computed address for texels for tag array (2) lookup. If access hit, pointer to location in data array is placed in entry at tail of FIFO (3) along with other relevant information. When texture reaches head of FIFO, a controller (4) uses pointer to look up texel data from data array (5) and returns it to texture filter unit (6). Textel lookups can be parallelized for bilinear and trilinear filtering, which combines texels to produce a single color value returned to pipeline via register file. 
If cache miss during tag lookup, tag array sends memory request via miss request FIFO (8). This sends requests to lower levels of memory system (9). DRAM bandwidth utilization can be improved by scheduling techniques that may service requests OoO, reducing row switch penalties. Data must be returned from memory system in order (preventing data array from differing from tag array) using the reorder buffer (10).

## 4.2 On-Chip Interconnection Network

GPUs connect multiple DRAM chips in parallel via memory partition units. Traffic is distributed across said units using address interleaving, with an Nvidia patent balancing traffic: up to 6 memory partitions at granularities of 256 bytes or 1024 bytes. 
SIMT Cores connect to memory partition units via on-chip interconnection network via crossbars (ring networks if AMD). 

## 4.3 Memory Partition Unit
Each memory partition unit contains a portion of the L2 cache, along with one or more memory access schedulers (frame buffers, FB), and a *raster operation* (ROP) unit. L2 cache contains both graphics and compute data. Memory access scheduler reorders memory read and write operations to reduce overheads of accessing DRAM (what does this mean?). ROP is used in graphics operation (like alpha blending) and supports compression of graphics surfaces. ROP unit supports atomic operations, like those in CUDA.

### 4.3.1 L2 Cache
Optimized for overall throughput per unit area. L2 cache portion in each memory partition is composed of two slices, each containing separate tag and data arrays, and processes requests in order. To match DRAM atom of 32 bytes (GDDR5), each cache line in the slice has four 32-byte sectors. Cache lines are allocated for use by load/store instructions. 

To optimize for common case, coalesced writes that completely overwrite each sector on a "write miss", no data is first read from memory. Uncoalesced writes are handled via storing byte-level valid bits and bypassing L2 entirely. Data that's being written to memory is buffered in cache lines in L2, while writes await scheduling (to reduce area of memory access scheduler). 

### 4.3.2 Atomic Operations
ROP unit includes function units for atomic and reduction operations. A sequence of atomic operations accessing the same memory location can be pipelined, since ROP unit contains local ROP cache. Atomic operations can be used to synchronize across threads in different thread blocks. 

### 4.3.3 Memory Access Scheduler
Special DRAM, like GDDR5 gdd is used. A row of values in said DRAM, called a page, is first read into a "row buffer". The bitlines connecting DRAM capacitor storage to the row buffer must first be precharged to halfway between 0 and Vss. When capacitor is connected to the bit line via access transistor during active operation, the voltage of bit line is pulled up or down as storage cell is written. A sense amplifier amplifies this change until a 0 or 1 is read. 
Thus, the process of reading the values into the row buffers refreshes values in DRAM. The precharge and activate operations introduce delays, where no data can be read or written  DRAM. To mitigate this, DRAM contain multiple banks, each with their own row buffer, though this doesn't hide latency from switching between rows. Thus, memory access schedulers are used to reorder DRAM memory access requests to reduce data movement between row buffers and DRAM cells.
 
Enabling DRAM requires each memory partition in GPU to have multiple schedulers, connecting its L2 cache to off-chip DRAM. The simplest approach is for each slice of L2 to have its own scheduler, containing separate logic for sorting read/write requests ("dirty data notifications?") sent from L2. To group reads to same page, two separate tables are employed: 
1. Read request sorter. Set associative structure accessed by memory address and maps read requests to same row in a bank to a single pointer. 
2. Read request store: Pointer looks up a list of individual read requests in this table. 
