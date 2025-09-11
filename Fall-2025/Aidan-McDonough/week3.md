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
