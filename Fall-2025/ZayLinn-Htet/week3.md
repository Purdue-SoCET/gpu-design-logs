I am not currently stuck or blocked

Week 3: 9/5/25 - 9/11/25 

Sunday (9/7/25): 
- Attended first GPU Team weekly meeting
- We reviewed the readings we were assigned for Chapters 1, 2, and 3 and I realize I am not as proficient with the information as I thought I was
- I plan to thoroughly read through the chapters and fully grasp the architectures, terms, and protocols by heart in the upcoming week
- The terms Sooraj covered were definitely recognizable, but I failed to connect them to their definitions in the moment
- During the meeting, I mainly focused on listening to how Sooraj explained it, and the questions that other people asked about it
- Was assigned into a team with Seth (Seth Thomas McConkey) and Jack (Jia-He Zhou) to make a short presentation on 3.6.3 Register File Virtualization
- We have planned to get the presentation done by Friday

Thursday (9/11/25):
- Attended SoCET Meeting today and was very inspired by Intel's VP Daniel Elmhurst
- Everything he talked about was filled with so much experience and wisdom
- He talked about how applicability of the knowledge we learned is very important and gave us real world applications of ECE 337 for example
- I learned about how important it is in the working environment to push myself to keep learning new things that are outside of what I know
- I listened to him talk after the lecture as well just so I can absorb all the wisdom I can from him

- Was occupied with career fairs the entire week, so I had to do all the readings today
- Felt unconfident after Sunday's Meeting so reviewed the GPU hierarchy terms to make sure I can differentiate them

Review
Kernel: function written in CUDA that runs in GPU
Grid: collection of blocks launches for a kernel execution
Block: group of threads organized in 1D, 2D, or 3D
Thread: smallest unit of execution in a kernel; each executive same code but on different data (SIMT)

Warp: group of 32 threads (NVIDIA GPU) that execute in lockstep on the hardware

Software Items: kernel, grid, block, thread
Hardware Items: warp

- Block has at least one thread
- GPU splits block into warps automatically (Ex. 128 threads = 4 warps) (Ex. 1000 threads = 31 warps + 8 threads)
- Still forms 32 warps with inactive threads in last warp (mask off)
- Threads in a Block can cooperate (shared memory)
- Threads in warp execute in lockstep
- Warps diverge if branch instruction, then reconverge

- Threads in warp execute same instruction simultaneously
- Each thread has own registers and data
- GPU executes both diverged paths, but mask out thread that are not active in current path (slower)

- Different warps are different instructions
- GPU warp scheduler decides which warp gets execution resources


- GPU divide into local and global memory spaces
- Local Memory: private per thread; registers spilling
- Global Memory: data structures shared among multiple threads
- Scratchpad: shared among threads and executed together in a cooperative thread array
- Can avoid long latency mem_access if accessed fewer times

First Level Memory Structures
- First-level cache: unified L1 data cache and scratch pad "shared memory"; L1 texture cache

- Shared Memory (Scratchpad Memory): small memory space; low latency; access all threads
- CTA: Cooperative Thread Array
- NVIDIA refers as Global Memory
- SRAM
- One bank per lane; bank has one read port and one write port
- Each thread has access to all banks
- Bank Conflict: more than one thread access to same bank per cycle; thread wants multiple data in one bank
- L1 data cache: subset of global memory
- Only locations not modified by kernels due to lack of cache coherence
- Coalesced: if multiple data reqs but only one call needed
- Uncoalesced: if multiple mem access different caches
- NVIDIA Fermi Architecture and Kepler Architecture has unified shared memory and L1 data cache
- Ld/st instr to L1 cache
- mem access has multiple addr, one for each thread in warp
- Arbiter determines if addr will have bank conflicts
- If bank conflict, broken into two parts; first part addr subset for threads without conflict; second is addr with bank conflicts
- Original request instr sent back to pipeline and executed again
- Replay: first addr without conflict, replay for addr with conflict
- Have limited buffering for replaying data
- Accepted (first) addr skip tag lookup; shared memory is direct mapped
- Arbiter schedules wb event to register file inside instruction pipeline as latency of direct mapped memory lookup is constant
- Tag unit: determines which bank each thread's request maps to
- Bank inside data array is 32-bits wide
- Data returned to appropiate thread lane
- Lanes corresponding to active thread wb to reg_file
- If one cycle for mem lookup and accepted portion, second cycle for bank conflict portion
- If more bank conflicts further subdivide

- Diagram Overview
Load/Store Unit: interface between warp scheduler/execution and memory system
Arbiter: decides which request proceeds first to avoid conflicts (replay)
Tag Unit: checks if req mem in L1 cache
Addr Crossbar: directs addr from tag unit to correct cache bank
Data Banks: data storage arrays
Data Crossbar: routes data from cache bank to req thread
Pending Request Table (PRT): keeps track of outstanding cache misses
Memory Management Unit (MMU): handles virtual-to physical addr translation
Fill Unit: when cache miss is resolved, fill unit

Cache Read Operations
- subset of global mem in L1 cache
- data arr across warps; single cache block per cycle
- compute mem addr; coalesced addr to arbiter;
- pending req table diff from CPU cache
- MSHR (Miss Status Holding Register): keeps track of cache misses
- PRT merges two requests to same block
- L1 dcache is virtually indexed and tagged; page-based virtual mem advantageous within GPU
- MMU deals with virtual to physical addr translation
- Memory Partition Units contain L2 cache and mem access scheduler
- FIll Units uses SubID field in mem req to look at req info in PRT

- Cache Write Operation
- GPGPU applications have poor temporal locality; threads write out data to large array -> write through with no write allocate
- Local memory for "spilling registers" may be good temporal locality
- Data to write to shared mem or global mem is placed in Write Data Buffer (WDB)
- If data in cache, wb there; if not get read from l2 cache/dram mem and write
- Cache coherence not supported
- SM (Streaming Multiprocessor) : fundamental hardware execution unit on NVIDIA GPU
- NVIDIA recently combined L1 dcache and texture cache
- APIs use texture mapping on 3D model to make look realistic; samples "texels" coordinates; average pixels next to texel; significant locality in texture mem access

- Tag array and data array separted by FIFO buffer; FIFO hides latency of miss reqs
- Texture cache designed assuming cache misses are frequent, small working size
- ld/st sends computed addresses for texels; tag array lookup; if hit, placed in FIFO; at exit FIFO, uses pointer to look up texel data from data array; returns to texture filter unit
- if miss; mem request miss FIFO; sends to lower memory
- L1 unfied cache used by NVIDIA and AMD; AMD uses all on texture cache

On-Chip Interconnection Network
- multiple DRAM chips in parallel via memory partition units
- memory traffic with address interleaving
- SIMT cores to mem partition with on-chip interconnection

Memory Partition Unit
- Each memory partition unit has portion of L2 cache with one or more mem access schedulers
- Frame Buffer/FB/Raster Operation (ROP) Unit: memory access schedulers
- ROP reduces overhead for DRAM access; also supports atomic ops in CUDA

- L2 cache has two slices; slice has tag and data arrays; 32-byte sectors
- Cache lines for ld/str instructions
- Coalesced: threads in warp access contiguous (shared/touching) memory address
- Uncoalesced: scattered memory addresses
- For uncoalesced in GPU; store byte-level valid bits; bypass L2 entirely
- Data to be written in memory buffered in cache lines in L2 while writes await scheduling
- Atomic ops can be pipelined; ROP unit has local ROP cache
- DRAM for GPU
- bits stored in capacitor; read from capacitors; 
- DRAM Read: Page: row of bits from capacitors; read row buffer first; bitlines connecting to individual storage must precharge; pulls bit line up or down from initial charge; semse amplifier senses change for a read
- Precharge op prevents DRAM from read or write in the moment, causing delays
- DRAMs contain multiple banks to mitigate the delay; each memory partition in GPU may contain multiple memory access schedulers; connects portion of L2 cache to off-chip DRAM
- Each slice of L2 cache has own mem access scheduler
- Reads in same row in DRAM bank, two separate tables; first (read request sorter) maps read reqs of same row to single pointer; pointer looks in second table (read request store)

Research Directions for GPU Memory Systems
- Mem Access Scheduling and Interconnection Network Design
- Row Buffer Locality: requests appear nearby in sequence access same DRAM row in same DRAM bank
- If sent to memory partitions, intermixed with reqs from other SM to same mem partition; thus, lower row buffer locality of sequence of req
- As SMs increase, more to happen; need meshes
- CUDA applications utilize "half routers" reduce area cost

- Caching Effectiveness
- Using scratchpad via L1 cache not effective
- Consider impact of caching on request traffic to L2 cache
- Three Forms of Locality: within warp, within block, cross instruction
- Within warp: mem read access from single load execute by different threads within a single warp
- Block Locality: mem read from single ld execute by threads in dif warps from same thread block access same cache
- Cross Instruction: memRead from dif load instr execute by threads, same thread block, same cache block

- Memory Request Prioritization and Cache Bypassing
- Similar to warp scheduling
- Low cache associativity can make conflict misses
- Assume cache space allocated upon miss
- Associativity Stall: all blocks in cache set are reserved to provide space for data and will be supplied by cache misses
- Cross Warp Contention: result of one warp evicts data brought in by another wap
- Mem Req Prioritization Buffer (MRPB): reduces capacity misses; modify order of access to increase locality
- MRPB implements mem req reorder before L1 dcache
- MRPB takes mem reqs from instr pipeline; results go into L1 cache
- MRPB has FIFO queues; use warp ID
- MRPB has drain policy

- Exploiting Inter-Warp Heterogeneity
- Memory Divergence Correction (MeDIC): heterogeneity in level of mem lat divergence across warps in same kernel
- warps are usually all/mostly hit, all/mostly missed or balanced
- Queuing for L2 cache can be significant
- Microarchitectural Mechanism: 1) warp-type detection block (all-miss, mostly-miss, balanced, mostly-hit, all-hit); 2) warp-type-aware bypass logic block for req by pass the L2 cache; 3) warp-type-aware insertion policy (where instr in L2 will be placed in LRU stack)
- Hit ratio of warps (total hits/accesses)
- Bypass mech sits in front of L2 to be mem_req_unit
- MeDiC change where reqs returned from DRAM are placed in L2's LRU stack
- Modifies baseline mem req sch for two mem queues: high-prio for all-hit and mostly-hit; low-prio fro mostly-miss, and all-miss

- Coordinated Cache Bypassing
- Ld op with good locality accepted; bad locality bypassed
- Use L1 or bypass; better cache hit rate and significantly more than static warp limiting

Adaptive Cache Management
- Cache Bypassing and Warp Throttling
- detects cache contention and mem resource contention; coordinates throttling and bypassing policies
- Protection Distance: prevents cache line from being evicted for a number of accesses
- When distance==0, line no longer protected and evicted
- Protection Distance: set globally and optimal value differs between workloads

Cache Prioritization
- Warp Throttling: limits number of active warps 
- warp throttling optimize L1 cache hit rate; lowers L2 and mem usage
- "non-polluting warps" - mem access bypass cache (write through)
- Choose W Warps to be Scheduled and T tokens to set less than max number of warps
- dynPCALMTLP: W to max warps, varies T across different SIMT cores; value of T with best performance selected
- dynPCALCCWS: uses CCWS to set W, then dynPCALMTLP to get T
- CCWS: Cache Conscious Wavefront Scheduling
- dynPCALMTLP: Dynamic Perceptron-based Cache Access Locality Memory Throttling with Locality Prediction
- dynPCALCCWS: Dynamic Perceptron-based Cache Access Locality Cache Conscious Wavefront Scheduling

Virtual Memory Page Placement
- DRAM for bandwidth more expensive in cost and energy than optimized for capacity
- GPU can access low bandwidh/high capacity CPU mem at low latency
- Use both CPu and GPU mem to increase mem bandwidth
- Allocate pages to bandwidth, or capcity-optimized mem
- Refine page placement; propose profiling pass implemented; use profile-guided page placement hints

Data Placement
- POROPLE: portable data placement strategy; specification language, source-to-source compiler, adaptive runtime data placer
- mem specific language to help extensibility and portability
- source-to-source compiler named PORPLE-C; transforms GPU into placement agnostic version
- use PORPLE-C find static access patterns through code analysis
- Run on CPU for short period of time to determine best GPU-based data placements
- Estimate number of transactions; esimate how much cache is devoted to each array

Multi-Chip-Moduel GPUS
- Large GPU out of smaller GPUs
- local caching of remote data, CTA scheduling, locality and first-touch page allocation