# Week 3


## Status: 

I am not currently stuck or blocked.

## Progress

### Memory Systems 

#### Intro 

- CPU-> Register File and Memory
- GPU -> Local and global, Scratchpad, 
- Local -> private per thread; typically used for register spilling 
- Global -> data structures that are shared between threads
- Scratchpad -> programmer managed; shared access between threads in theread array
- Accessing on-chip memory data is faster and more energy efficient

#### First-Level Memory Structures

**Scratchpad and L1 Data Cache**
- Cuda :
    - Shared Memory - small space with low latency accessible by all threads in a CTA
- Shared memory else where -> scrachtpad
- Latency similar to register file
- Bank conflict:
  - 1 bank per line; 1 read and 1 write port per bank; each thread has access to all banks
  - more then one thread access same bank on a cycle and threads want to access different location in the bank
- L1 data cache:
  - maintains a subset of global memory address space
  - some architectures only contains locations not modified by kernel
  - Coalesced -> access such that all threads in warp access location fall within a single L1 cache block and that block is not present in the cache -> only single request needds to be sent to lower level cache
  - Uncoalesced -> threads within a warp access different cache blocks then multiple memory accesses need to be generated
  - programmers try to avoid bank and uncoalesced by hardware allows fro both
    
<img width="690" height="432" alt="image" src="https://github.com/user-attachments/assets/77de0495-fb0b-49ce-86a8-d6c79c1fbcd7" />

- Each SM has l1 cache and shared memory
- A memory access request contains: set of memory addresses, one for each thread in the warp with op type
- 
**Shared Memory Access Operation**
- Arbiter:  
  - Checks warp requests for bank conflicts  
  - If no conflicts then request passes  
  - If conflicts then split request:  
    - Accepted part = threads without conflicts  
    - Replay part = conflicting threads, replay
- Replay storage tradeoff:
  - 1: pull again from instruction buffer -> smaller hardware, higher energy (big register file access)  
  - 2: small buffer in load/store unit -> more energy efficient, less stress on instruction buffer  
- Accepted requests:
  - Shared memory is direct mapped so no tag lookup needed  
  - Arbiter schedules writeback to registers (fixed latency if no conflict)  
  - Tag unit maps each thread to its bank -> drives address crossbar  
  - Banks: 32-bit wide, independent decoders, allow parallel access  
  - Data returns via data crossbar -> only active threads update their registers  
- Replays:
  - Replayed portion re-enters arbiter the next cycle  
  - If still conflicting, gets split again into accepted and replay parts

  **Cache Read Operation**
- Only a portion of global memory is cached in L1 -> tag unit checks if data is present  
- Data array is highly banked for shared memory, but cache reads are limited to one block per cycle  
- Cache block size: 128 bytes (Fermi/Kepler), split into 4 × 32-byte sectors (Maxwell/Pascal)  
- Each block is 32-bit entries across 32 banks in the same row  
- Load/store unit computes addresses and coalesces accesses -> sends to arbiter  
- Arbiter may reject request if: cache set ways are busy, or pending request table (PRT) is full  
- If resources available: arbiter schedules register file writeback (assuming cache hit), while tag unit checks hit/miss  
  - Cache hit: data array row accessed, data returned to register lanes for active threads only  
  - Cache miss: arbiter signals replay, request sent to PRT (acts like CPU MSHRs)  
    - PRT holds block address, offsets, and registers to update when block fills  
    - Can merge two requests to the same block  
    - Records info to replay deferred memory accesses  
- L1 cache is virtually indexed and virtually tagged (unlike CPUs, which are often virtually indexed and physically tagged)  
  - GPUs don’t need to flush L1 on warp context switches since warps are all from same app  
  - Virtual memory helps allocation and fragmentation handling  
- On miss: request goes from PRT -> MMU (virtual to physical) -> memory partition unit (contains L2 and scheduler)  
  - Memory request carries subid to match response with PRT entry  
- On return: MMU -> fill unit -> looks up subid in PRT -> informs LSU via arbiter to replay load, now guaranteed to hit (cache line locked after fill)  

  **Cache Write Operation**
- L1 cache supports both write-through (cache and ram) and write-back (cache first)
- Global memory writes often have poor temporal locality -> write-through, no write-allocate makes sense  
- Local memory spills/stacks may have good locality -> write-back with write-allocate  
- Data to be written first placed in write data buffer (WDB)  
  - For partial/uncoalesced writes, only part of block updated  
  - If block present then update via data crossbar  
  - If block absent then fetch from L2/DRAM before write  
- Coalesced writes that fully fill a block may bypass cache (invalidate old tags)  
- No cache coherence across SMs:  
  - Example: SM1 caches value A, SM2 writes new A then SM1 may still read old value  
  - To avoid this, Kepler restricted L1 use:  
    - Local memory (spills, stacks) allowed  
    - Read-only global memory allowed

  **L1 Texture Cache**
  
<img width="657" height="713" alt="image" src="https://github.com/user-attachments/assets/e2b54ea2-7e42-4754-aaa9-c18fb81d9a8b" />

- Modern GPUs merge L1 data cache and texture cache
- Texture cache designed with assumption of many misses
- Exploits spatial locality
- What is a texture?
  - imaged applied to 3D surface
  - rendering pieplein computes coordinates od texels ( texture samples)
  - texel addresses are used to fetch values from memory
  - neighboring pixels -> neighboring texels -> locailty
- Microarchitecture
  - Load/store unit sends texel address to tag array
  - Fragment FIFO sits between tag array and data array
  - Purpose: hide miss latency -> tag array runs ahead of data array by 1 DRAM round trip
  - both hits and misses have about same latency
  - On a hit:
    - Tag array lookup returns a pointer to data in data array
    - pointer and meta data placed at tail of FIFO
    - When entry reaches FIFO head, the controller uses the pointer to fetch texel from data array
    - texel passed to texture filter unit -> filtering combines 4 or 8 texels into one color
    - result written back into register file -> instruction pipeline
  - On a miss:
    - Tag array sends request to miss request FIFO
    - Miss FIFO sends to lower memory system, where memory scheduler may reorder requests for efficiency 
    - Data must come back inorder -> reorder buffer: ensure the contents of the data array reflects the time-delayed state of the tag array
  - Now, NVIDIA and AMD use unified L1 data and texture cache
    - Only data values that can be guaranteed to read-only cached in the L1
    - texture cache data is read only
    - by caching only read-only data, GPU can reuse the existing texture cache hardware, with small tweaks

  ### On-Chip Interconection Network

  - GPUs connect multiple DRAM chips in parallel via memory partition units to achieve larger memory bandwidth
  - Address interleaving -> scheme for balancing traffic across memory partition units
  - NVIDIA: Crossbar -> on-chip interconnection network for memory partitiion units
  - AMD: ring network
 
### Memory Partition Unit

- Each memory partition unit contains L2 cache along with one or more frame buffers (memory access scheduluer)(FB) and raster operation unit (ROP)
- Memory access scheduler reorders memory read and write operations to reduce overhead of accessing DRAM
- The ROP unit is used in graphics operations
  
<img width="739" height="535" alt="image" src="https://github.com/user-attachments/assets/0c8e7c8e-bd08-44f9-afc0-76cd8e1a7f18" />

**L2 Cache**
- 2 slices: Each slice contains a seperate tag and data array and procces incoming requests
- Matches DRAM atom size of 32 bytes -> each cache line inside the slice has 4 32 byte sectors
- Cache lines can be used for load or storing
- if a write completely replaces a sector (coalesced write), the cache skips reading old data from memory -> faster then typical CPU cache
- when writes only partially cover a sector (uncoalesced write) -> possible approaches:
    -  tracking valid bytes
    -  skipping L2 cache

**Atomic Operations**
- ROP unit includes functions units for executing atmoic and reduction operations:
    - atomic operation: thread safe update to shared data
    - reduction operation: combining many values into one (sum, min, max, product, etc.) -> in parallel computing this means multiple threads contribute to same result
- a sequence of atomic operations accessing the same memory location cna be pipelined

**Memory Access Scheduler** 
- GPUs use DRAM to store large amounts of data
- DRAM uses capacitors:
    - full row (page) is moved into the row buffer
    - sense amp detects and amps 0 or 1 
- Midigate DRAM overhead -> multiple banks, each with thier own row buffer -> overlap operations
- Even so, switching between rows introducing latency -> multiple access schedulers reorders requests to reduce row switching
- Each GPU memory partition may have multiple schedulers connecting its slice of L2 cache to DRAM
- Schedulers handle reads and writes separately:
    - read request sorter : to group reads targeting the same row in a bank, set-associative structure indexed by memory address, holds pointer
    - read request store: second table accessed via pointer from sorter, contains actual list of read requests for that row, multiple requests to the same row combined
    - other logic for write requests from L2
 
### RESEARCH DIRECTIONS FOR GPU MEMORY SYSTEMS

**MEMORY ACCESS SCHEDULING AND INTERCONNECTION NETWORK DESIGN**
- Yuan (2009) : SM requests have row-buffer locality -> lost when mixed so proposed interconnect arbitration to preserve
- Prioritize same SM -> same row-bank requests for simpler scheduler
- Bakhoda (2010,2013): More SM -> need scalable interconnects (meshes)
- Throughput insensitive to latency
- many-to-few-to-many traffic patterns -> half-routers that reduce area

**CACHING EFFECTIVENESS**
- Bakhoda (2009): Adding L1/L2 caches in GPGPU-Sim showed mixed benefits across apps  
- Jia (2012): Fermi GPU experiments confirmed cache usefulness depends on app  
- L1 cache not sectored -> misses trigger larger 128 bytes off-chip accesses, harming bandwidth-limited apps  
- Cache hit rate alone not reliable -> must consider traffic to L2 and memory partitions  
- Locality taxonomy: within-warp, within-block, cross-instruction  
- Compile-time algorithm proposed to infer when caching is beneficial based on locality types

**MEMORY REQUEST PRIORITIZATION AND CACHE BYPASSING**
- Jia (2014): Built on cache characterization and CCWS work  
- Intra-warp contention: multiple requests from same warp map to one cache set -> associativity stalls and pipeline stalls  
- Proposed bypassing L1 cache on a miss if no block can be allocated due to associativity stall  
- Cross-warp contention: one warp evicts data fetched by another  
- Introduced Memory Request Prioritization Buffer (MRPB) placed before L1  
- MRPB: parallel FIFOs, requests assigned using warp ID signature  
- Drain policy: fixed-priority scheme to select which FIFO feeds cache  
- MRPB and bypassing -> about 4% geometric mean speedup over 64-way 16KB cache  
- Showed better results than CCWS in some comparisons  
- Rogers (2012) used more advanced set index hashing, reducing stalls  
- Nugteren (2014): reverse-engineered NVIDIA Fermi -> XOR-based index hashing to reduce conflicts  
- Jia (2014): approach is transparent to programmers, narrows performance gap between cache-based code and hand-optimized scratchpad code  
- Arunkumar (2016): Studied bypassing + variable cache line size depending on memory divergence and reuse distance  
- Lee & Wu (2016): Proposed runtime control-loop bypassing -> tracks reuse per instruction, bypasses when reuse too low

**EXPLOITING INTER-WARP HETEROGENEITY**
- Ausavarungnirun (2015): Proposed L2 and memory controller improvements to reduce latency divergence in irregular GPU apps  
- Key idea: warps differ in cache hit/miss behavior -> classify warps as all-miss, mostly-miss, balanced, mostly-hit, all-hit  
- All/mostly-hit warps stall on slowest access -> benefit if other warps bypass L2 to reduce queueing delay  
- Four components:  
  - Warp-type detection: classifies warps via dynamic hit ratio sampling  
  - Warp-type-aware bypass: all/mostly-miss warps skip L2, go directly to DRAM  
  - Warp-type-aware insertion: cache lines from mostly-miss warps placed at LRU, others at MRU  
  - Warp-type-aware memory scheduler: two queues (high-priority for all/mostly-hit, low-priority for others)  
- Effect: reduces L2 queuing delays, improves latency for hit-heavy warps, adapts to workload phase changes

**COORDINATED CACHE BYPASSING**
- Xie (2015): Profiling classifies loads as good, poor, or moderate locality -> good use L1, poor bypass, moderate decided adaptively  
- Adaptive scheme works at thread block level, using an online threshold based on L1 hits and pipeline conflicts  
- Approach improves cache hit rates more than static warp limiting  

**ADAPTIVE CACHE MANAGEMENT**
- Chen (2014b): Proposes combining warp throttling with cache bypassing for cache-sensitive GPU applications  
- Runtime mechanism detects cache and memory contention, then coordinates the two policies  
- Cache bypassing via protection distance: lines kept in cache for fixed accesses; if no unprotected lines remain, new requests bypass  
- Workloads show performance improvement and are largely insensitive to the protection distance value

**CACHE PRIORITIZATION**
- Li (2015): Observed warp throttling improves L1 hit rate but underutilizes L2 and bandwidth  
- Proposed token system: only token warps can allocate lines in L1; non-token warps execute but cannot evict data  
- Optimization uses two knobs: total scheduled warps (W) and token warps (T) -> static tuning gives 17% gain over CCWS  
- dynPCALMTLP: fixes W at max, samples T to maximize performance with less area than CCWS  
- dynPCALCCWS: uses CCWS to set W, dynPCALMTLP to set T, then adjusts W dynamically -> 11% gain over CCWS  

  **VIRTUAL MEMORY PAGE PLACEMENT**
- Agarwal (2015): Studied systems with both bandwidth-optimized and capacity-optimized DRAM in heterogeneous CPU-GPU setups  
- Found bandwidth-limited apps gain from using both memory types to increase aggregate bandwidth; latency-limited apps benefit less  
- Optimal placement: allocate pages proportional to available bandwidth; simple random allocation proportional to bandwidth works well unless bandwidth memory capacity is insufficient  
- When capacity is limited, refine placement by profiling access frequency; profile-guided hints via extended CUDA API achieve 90% of oracle performance  

  **DATA PLACEMENT**
- Chen (2014a): Proposed PORPLE, a portable GPU data placement framework with three parts: specification language, source-to-source compiler (PORPLE-C), and adaptive runtime placer  
- Memory specification language: describes GPU memory types by serialization conditions (e.g., coalesced global vs serialized shared bank accesses) -> improves portability  
- PORPLE-C: rewrites code into placement-agnostic form, inserting guards to select predicted best placement  
- Placement decisions: use static analysis of access patterns; if uncertain, insert runtime tracing to profile patterns on CPU before kernel launch  
- Prediction model: estimates transactions under serialization, uses reuse distance for cache hit rates, and partitions cache space linearly among arrays  

  **MULTI-CHIP-MODULE GPUS**
- Arunkumar (2017): Proposed scaling GPUs by combining smaller GPU modules in a multichip module, using local caching, locality-aware CTA scheduling, and first-touch page allocation  
- Achieved 90% of ideal monolithic GPU performance, 45% better than the largest practical single-chip GPU in the same technology  

  
<img width="649" height="310" alt="image" src="https://github.com/user-attachments/assets/5b825d43-e7ca-4099-9246-0fd1b44efc00" />

