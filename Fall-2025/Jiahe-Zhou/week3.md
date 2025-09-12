# Week 3
- State: Finished and not encountering any obstacle.
- About this: Chapter 4

## 4.1 First-Level Memory Structures

### 4.1.1 Scratchpad Memory and L1 Data Cache

share memory(scratchpad)
- Small, low latency
- Accessible to all threads in the same CTA
- Implemented as SRAM, one bank/lane, 1 read+1write ports/bank
- bank conflict: multiple threads access different addresses in the same bank

L1 data cache(global space)
- Holds a subset of global memory
- restricted to read-only global data to avoid coherence issues
- Coalesced: threads hit one block -> one request to lower levels
- Uncoalesced: threads span blocks -> multiple requests -> usually avoid
- unified shared memory + L1 cache via configurable SRAM
  - Support direct mapped access and a set associative cache
- Replay provides non-stalling pipeline interface on bank conflicts and L1 misses

<img width="866" height="559" alt="image-5" src="https://github.com/user-attachments/assets/da7e88ed-3e0f-45a7-a050-9ad578fbeafd" />

#### Shared Memory Access Operations
Shared access flow: Arbiter
- Determine whether requested address in warp cause bank conflict
  - Conflict: replay
  - Non-conflict: accept
- Schedule fixed-latency write-back when non-conflict
- Banks: 32-bit wide, independent row decoders
- data return via crossbar, write-back to register file
- Shared memory is direct-mapped; tag lookup is bypassed

#### Cache Read Operations
Global Load flow
- One cache block/cycle for global access
  - reduce tag cost, fit standard DRAM interface
  - Fermi/Kepler: 128B blocks; Maxwell/Pascal: 4×32B sectors
- LSU forms coalesced requests -> arbiter admits if resources free
- Tag unit check hit/miss
  - Hit: read data array rows across banks and write back to lanes
  - Miss: mark replay and allocate PRT(pending request table) entry; merge same-block misses
- virtually indexed and virtually tagged L1
  - send to MMU(memory management unit) translates virtual -> physical address
  - memory partitions hold L2 and schedulers
- Response uses subid to find PRT entry; fill unit locks the line and reschedules load to hit.

#### Cache Write Operations
Global Store flow
- Supports write-through and write-back
- Determine by memory space written
  - Global writes poor temporal locality -> write-through, no-write-allocate
  - Local spills/stacks good locality -> write-back, write-allocate
- Data first goes to WDB(write data buffer)
  - if hit cache, write to data array
  - else fetch line from L2/DRAM
- Full-line coalesced writes may bypass cache and invalidate stale tags
- No L1 coherence in this design
  - Kepler and onward restrict L1 to local memory(spill/stack) and read-only global memory

### 4.1.2 L1 Texture Cache
Why Texture Cache
- NVIDIA GPUs often unify L1 data and texture caches to save area
- 3D Graphic: realism with the high frame rates required for real-time rendering
  - Adjacent pixels map to adjacent texels; average nearby texels
  - strong spatial locality -> can be exploited by caches

Key Architecture
- FIFO buffer between tag array and data array
- Tag leads, data lags -> small array size
- Assumes frequent misses and small working sets
- Throughput ↑, but hit ≈ miss latencies

Hit path
- LSU sends addresses -> tag lookup
- On hit, push a pointer/metadata into fragment FIFO
- Texel data is read from the data array when the entry reaches the FIFO head
- Filter combines texels -> outputs color to pipeline

Miss path
- Tag sends request via miss request FIFO to lower memory
- Memory may serve out-of-order to raise DRAM efficiency
- Use a reorder buffer so data returns in-order to match advanced tag state

### 4.1.3 Unified Texture and Data Cache
Core
- Only read-only data is cached in L1
- Unified L1 caches both data and textures
- Reuse texture cache hardware with minor addressing logic changes

## 4.2 On-Chip Interconnection Network

<img width="780" height="903" alt="image-6" src="https://github.com/user-attachments/assets/f3329485-d712-45ed-9f42-ce399f6e101f" />

Purpose: Provide high bandwidth from DRAM to SIMT cores

Memory Partition Units
- Connect multiple DRAM chips in parallel
- Address interleaving to spread traffic
- NVIDIA patent: 256B/1024B granularity, up to 6 partitions

On-chip interconnection
- Connect SIMT cores <-> memory partitions
  - NVIDIA: crossbar networks
  - AMD: ring networks

## 4.3 Memory Partition Unit
<img width="943" height="675" alt="image-8" src="https://github.com/user-attachments/assets/1e370230-ca03-4957-8ba5-df68740ba2b9" />

- a portion of L2
  - Holds graphics + compute data
- 1+ memory access scheduler(frame buffer, FB)
  - Reorders reads/writes to reduce DRAM row activations/precharge penalties and improve bus efficiency
- ROP(raster operation) unit
  - Graphics: blending, compression
  - CUDA: atomic operations

### 4.3.1 L2 Cache
- optimize -> improve throughput/area
- 2 slices; separate tag/data; in-order per-slice processing
- Line = 4×32B sectors -> match 32B DRAM atom size
- Coalesced full-sector writes on miss: no read-for-ownership
- Uncoalesced writes: options include byte-valid bits or L2 bypass (not fixed)
- Pending writes buffered in L2 lines to shrink scheduler area

### 4.3.2 Atomic Operations
- ROP has atomic/reduction units + local ROP cache
  - Local cache -> Same-address atomics can be pipelined
- Atomics enable inter-block sync

### 4.3.3 Memory Access Scheduler
GPUs employ dynamic random access memory (DRAM) such as GDDR5
- Stores bits in small capacitors
  - a row of bits -> a page
- Precharge -> Activate(connect bitlines) -> Sense Amplifier -> Row Buffer
  - Read also refreshes cells
  - delays when precharge and activate; no data can be read or written
- Row switches are costly -> group same-row requests to reduce activations
- Multiple schedulers/memory partition
- Simplest: 1 scheduler/L2 slice
  - Separate read and write paths from L2
  - Group reads to the same row in bank -> Two-table
    - Read request sorter(by address): pointer per bank+row
    - Read request store: linked list of requests per pointer

## 4.4  Research Directions for GPU Memory Systems

### 4.4.1 Memory Access Scheduling and Interconnection Network Design
To preserve row-buffer locality under interleaved traffic from many SMs and enable scalable, low-cost on-chip networks as SM counts grow.
- SM requests have row-buffer locality
- Intermixing across SMs reduces locality at partitions
- Arbitrate by SM or row–bank similarity to preserve locality
- Scalable network-on-chip(mesh); many apps insensitive to interconnect latency
- Half-routers use many-to-few-to-many traffic to cut area

### 4.4.2 Caching Effectiveness
Because cache hit rate alone cannot predict performance, and some workloads even slow down due to extra off-chip traffic when caching is enabled.
- Caches help some apps, not all
- Using L1 to stage into shared memory yields little benefit
- Performance: Hit rate alone is not enough; consider L2/DRAM traffic
- Fermi L1 non-sectored -> 128B misses can hurt bandwidth-limited apps
- Locality taxonomy -> guidance for compile time
- Within warp: single load, different threads, access same cache block
- Within block: single load, different warps, access same cache block
- Cross-instruction: different load
 instructions, same thread block, access same cache block

### 4.4.3 Memory Request Prioritization and Cache Bypassing
Because low cache associativity and set-indexing conflicts cause intra-/cross-warp contention and pipeline stalls that must be mitigated.
- Intra-warp contention: indexing + modulo cache set
- Associativity stalls with limited MSHRs( miss-status holding registers) -> pipeline stalls
- Bypass L1 on miss when a set is reserved (associativity stall)
- MRPB: memory request prioritization buffer
  - reduces capacity misses by modifying order of cache access
  - multi-FIFO reorder by warp ID
  - fixed-priority drain policy
- Bypass + reorder ≈ +4% geometric mean speedup
- Other works: adapt line size/bypass by divergence

### 4.4.4 Exploiting Inter-Warp Heterogeneity
Because warps have different L2 hit behaviors, and treating them equally causes fast warps to wait for slow ones, increasing queuing delay.
- Warp types: all/mostly-hit, balanced, mostly/all-miss
- Bypass L2 for non all-hit warps -> less queuing for all-hit
- Type-aware insertion:
  - mostly-miss -> LRU(Least Recently Used)
  - others -> MRU(Most Recently Used)
- Type-aware scheduling: high-priority queue for (mostly/all-hit)
- Classification by interval hit ratio; thresholds tuned online

### 4.4.5 Coordinated Cache Bypassing
Because load instructions have widely varying data reuse, and blindly caching all of them causes pollution and low hit rates.
- Offline profiling labels static loads: good / poor / moderate locality
- Good -> use L1; Poor -> always bypass
- Moderate -> per-TB adaptive (all use L1 or all bypass)
- Threshold tuned online with hits + pipeline-conflict metric
- Outperforms static warp limiting on hit-rate gains

### 4.4.6 Adaptive Cache Management
Because cache and memory contention change dynamically, requiring runtime coordination of warp throttling and cache bypassing.
- Idea: coordinate cache bypassing + warp throttling
- Detect at runtime: cache contention & memory contention
- Protection distance: lines are temporarily non-evictable; when none unprotected in a set -> bypass
- Workloads insensitive to the exact protection distance

### 4.4.7 Cache Prioritization
Because simple warp throttling improves L1 hits but leaves off-chip bandwidth and L2 underutilized, needing token-based cache access control.
- Tokens decide L1 allocation; non-polluting warps run but cannot evict
- Optimize W (schedulable warps) and T (tokened warps)
- Static best W,T: +17% vs CCWS (static)
- dynPCALMTLP: fix W=max, search T -> CCWS-level perf with less area
- dynPCALCCWS: CCWS sets W, then find T, then adjust W online -> +11%

### 4.4.8 Virtual Memory Page Placement
Because future systems will mix bandwidth-optimized and capacity-optimized memory, and current OS policies ignore bandwidth non-uniformity.
- Heterogeneous capacity- vs bandwidth-optimized memories; need bandwidth-aware placement
- For bandwidth-limited apps: use both CPU & GPU memories to raise aggregate BW
- If pages are uniformly accessed and BW memory capacity ok -> allocate in proportion to bandwidth (optimal)
- Simple random-by-bandwidth works well; if BW memory capacity limited, refine by access frequency
- Tooling: profile-guided hints via modified nvcc/ptxas + CUDA API -> ~90% of oracle

### 4.4.9 Data Placement
Because programmers cannot easily decide where to place data across diverse GPU memory types or architectures, hurting portability and performance.
- Components: spec language, PORPLE-C compiler, adaptive runtime placer
- Spec by serialization conditions (e.g., coalescing vs shared-bank conflicts)
- Compiler inserts guards; runtime chooses best path
- Static analysis; else generate a brief CPU-side tracer to decide before kernel launch
- Model: estimate transactions; reuse-distance for caches; linear partition cache among arrays

### 4.4.10 Multi-Chip-Module GPUs
Because single monolithic GPUs face area and scaling limits, and MCM-based designs can extend performance scaling beyond process limits.
- Build big GPUs from smaller modules (MCM)
- Use local caching of remote, CTA scheduling with locality, first-touch page allocation
- Achieve within 10% of an ideal monolithic (unbuildable); +45% vs largest buildable monolith

<img width="931" height="424" alt="image-9" src="https://github.com/user-attachments/assets/1ca195e1-f2b1-4cf4-94fb-413cff80c4fb" />
