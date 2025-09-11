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
- 
