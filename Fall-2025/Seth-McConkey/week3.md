# Design Log Week 3

## Status

Not stuck or blocked.

## Notes on Chapter 4 GPGPU Architecture: Memory System

- GPGPU kernels interact with several memory spaces:
  - Global memory: Shared by all threads.
  - Local memory: Private to each thread, often used for register spilling.
  - Shared memory (NVIDIA): A programmer-controlled scratchpad for threads within the same CTA (Cooperative Thread Array).
- Using onchip memory (like the scratchpad) is crucial because offchip DRAM bandwidth is limited and expensive energy wise compared to onchip computation.

### First-Level Memory Structures

> The L1 Cache and Scratchpad Memory are first-level memory structures that each SIMT core interacts with.

#### Unified L1 Data Cache and Scratchpad Memory

- Modern GPUs often combine the L1 data cache and the scratchpad into a a singular configurable SRAM structure.
- Two key concepts for performance are:
  - Bank Conflicts: Occur in scratchpad memory when multiple threads in a warp try to access different locations within the same memory bank at the same time. 
    - Since banks are single-ported, these accesses get serialized which hurts performance.
  - Coalesced Access: Occurs when accessing global memory. 
    - An access is coalesced if all threads in a warp access locations that fall within a single L1 cache block. 
    - This is highly efficient since all data can be transferred using one transaction to main memory. 
      - Uncoalesced accesses require multiple transactions and should be avoided.

<br>

> The unified cache architecture handles different requests as follows:

##### Shared Memory Access

- Shared memory are directly mapped to SRAM banks by the programmer
  - This allows the programmer to manually avoid bank conflicts by controlling how data is laid out in shared memory.
- If a conflict exists, the request is split. A non-conflicting subset of requests continues on through the pipe.
- The conflicting requests are sent back to the pipeline for replay on a later cycle.

##### Main Memory Read

- On a cache hit:
  - If the data is in the L1 cache, it's returned to the register file.
- On a cache miss:
  - The request is sent to a Pending Request Table (PRT)
  - A request is sent to the L2 cache/DRAM.
  - The original instruction is marked for replay.
  - When the data returns, it fills the L1 cache, and the instruction is replayed, which is now guaranteed to be a hit.

##### Global Memory Write

- Can use write-through or write-back policies depending on the memory space.
- For many GPGPU workloads, a write-through with no-write-allocate policy is effective, as threads often write to a large array just once before exiting.
  - These are poor temporal locality memory accesses.
  - This is very different from how a CPU cache behaves:
    - GPUs prioritize high throughput so the old, stale data is not grabbed from main memory (hurts bandwidth) like it would be in a CPU cache.

##### Cache Coherence

- A major difference from the ECE 437 multicore CPU is that these L1 caches are typically not coherent. If a core modifies data in its L1, other cores won't see that change until it's written back to L2/DRAM. To avoid this, older GPUs only cached read-only data in the L1.
  - It's up to the programmer to make sure stale data isn't being used in some SM cores after the data has been modified by another core.

#### L1 Texture Cache

- Used heavily in graphics for texture mapping (not used as much in modern architectures anymore).
- Designed to tolerate high miss rates by separating the tag and data arrays with a large FIFO buffer.
- This cache pipelines the misses, assuming they will be frequent.
  - It hides the long off-chip latency by overlapping multiple misses.

### On-Chip Interconnection Network

- This network connects the SIMT cores to the memory partitions (which contain the L2 cache and DRAM controllers).
- It uses address interleaving to distribute memory traffic evenly across the memory partitions, preventing hotspots.
- Common topologies include a crossbar (NVIDIA) or a mesh network (AMD).

#### Crossbar (NVIDIA)
- Each core has a dedicated path to each memory partition.
- This provides high bandwidth and low latency but can be expensive to scale.
  - Requires a lot of die space and power.

#### Mesh (AMD)
- Cores and memory partitions are arranged in a 2D grid.
- Each core can only directly communicate with its immediate neighbors.
  - Allows for scalable designs with many cores and memory partitions.
  - Leads to high traffic in some mesh nodes which hurts latency
  - Also leads to higher latency since multiple "hops" may be needed to reach a memory partition.

### Memory Partition Unit

- A memory partition is a slice of the memory system that contains a piece of the L2 cache, a memory access scheduler, and a Raster Operation (ROP) unit.

#### ROP Unit

- In GPGPU contexts, the ROP unit handles atomic operations
- Contains caches which helps with latency when lots of threads are trying to conduct atomic operations on the same memory location.

#### L2 Cache

- Provides a large, shared cache for all cores.
- no-write-allocate policy: if a write completely overwrites a cache line on a miss, the old data isn't read from main memory.
  - Helpful for coalesced writes
  - Again, very different from CPU cache behavior

#### Memory Access Scheduler

- This block is very important for offchip memory access performance. 
  - Main memory access involves high-latency operations like precharging a row before reading it.
  - The scheduler reorders memory requests to group accesses to the same DRAM row together. 
    - This minimizes row-switching penalties by coalescing accesses to the same row.

### Memory System Research Topics

- Like with the register file, there's a lot of research into making the memory system more efficient.

#### Cache Management (Bypassing & Prioritization)

- Not all memory accesses have good locality, so caching them can actually hurt performance by evicting more useful data (cache pollution).
- The proposed solution is to use hardware or compiler techniques to predict which memory accesses will benefit from caching. 
  - Low-locality accesses can bypass the cache entirely, going straight to main memory.

#### Data Placement

- The programmer has to manually decide whether to put data in global memory, shared memory, etc. 
  - This is difficult compared to CPU programming and adds a barrier to entry.
- Research into compilers that can automatically analyze a kernel's access patterns and place data in the best memory space is being done to see if this can be done on hardware without the programmer's input.

#### Multi-Chip-Module (MCM) GPUs

- As Moore's Law slows, making single, massive GPU chips is becoming harder.
- An emerging idea is to build a large GPU by connecting several smaller GPU chiplets on a single package. A key challenge is managing data locality and communication between the chiplets efficiently.
  - AMD's modern architectures use this approach, while NVIDIA is still using monolithic dies.

##### Monolithic Dies vs. MCMs

- Monolithic Dies:
    - Lower latency communication between cores and memory.
    - Harder to manufacture and more expensive
- MCMs:
    - Easier to scale performance by adding more chiplets.
    - Potentially lower cost due to smaller, easier-to-manufacture dies.
    - Tradeoff: Higher latency communication between chiplets.