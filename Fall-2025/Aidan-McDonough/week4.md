# Design Log Week 4

## Status: 

I am not currently stuck or blocked.

## Reading Notes 

### Analyzing Modern NVIDIA GPU cores

#### Background and Motivation

<img width="391" height="323" alt="image" src="https://github.com/user-attachments/assets/12cd0458-6573-46c8-916e-085c79be5053" />

**Context**
- Most GPU microarchitecture research in academia use GPGPU-Sim simulator microarchitecture.
- This simulator was updated to include sub-cores: 4 sub-cores with memory unit containing L1 instruction and data cache, shared memory, and texture cache.

**Operation**
- Fetch: Round-robin picks a warp only on L1I hit and free per-warp instr buffer slots.
- Instr buffers: Per-warp; hold decoded, consecutive instructions until issue-ready.
- Issue (GTO): Select warp not at barrier whose oldest instr has no dependencies.
- Scoreboards (per warp):
  - RAW/WAW: pending writes -> operands must clear to issue.
  - WAR: counts in-flight readers (handles out-of-order operand fetch from variable-latency ops).
- Operand collection: Issued instr waits in Collector Unit until all sources retrieved.
- Register file: arbiter resolves bank conflicts.
- Dispatch/Exec/WB: when control unit ready -> dispatch to unit (latency varies) -> result writes back to register file.

**Paper Focus**
- Accel-Sim today: Tesla-like core with sub-cores with sectored caches.
- Missing modern features: L0 instruction cache, Uniform Register File, updated issue/RF/RF-caches.
- Goal: Reverse-engineer modern NVIDIA cores and update Accel-Sim for industry-closer baselines

#### Control Bits in Modern NVIDIA GPU Architectures
- Rely on compiler to handle register data dependacnies rather that at run time in the hardware
- Assembly instrcutions include some control bit to manage dependacies and improve performance/energy consumptiom
- Each sub-core issues 1 instruction/cycle
- The scheduler prefers to keep issuing from the same warp if that warp's oldest instruction is ready
- Fixed latency dependances are handled by a per warp Stall Counter set by the compiler -> decrementes every cyle and a nonzero value makes the warp ineligble to issue
- The hardare does not check RAW hazards for fixed lat ops -> depends on stall counter
- this design avoids scoreboard wiring from fixed lat units -> area/energy benefits
- Yield-bit: tells hardware not to issue from same warp next cycle -> if not other warp is ready then sub-core bubbles
- each instruction also has a stall and when its > 1, the warp will stall regardless of yield
- Variable lat hazard: handled with 6 per warp dependene counters all initialized to 0 at start
- increment at issue -> decrement at write-back for RAW/WAW or read for WAR
- Two 3 bit field specify up to 2 counters to increment, 6 bit mask lists which counters must be 0 to issue
- If more theb 6 groups exist then compiler must reorder or group some under one condition
- increments take effect a cycle late, so if the consumer is immediately next the producer must set stall = 2
- DEPBAR.LE SB1, 0x3, {4,3,2} = do not issue yet until SB1 <= 3 and counters SB4, SB3, SB2 are all 0
- If N loads will write back in order and your consumer only needs the first M, use DEPBAR.LE ..., N−M
- Per operand resuse bit tells hardware to cache that source in the Register File Cache

#### GPU cores Microarchitecture
- Components: issue scheduler, front-end, register file, memory pipeline

<img width="812" height="134" alt="image" src="https://github.com/user-attachments/assets/3e3d5312-8905-42e9-bc5e-7c58b502c76c" />

<img width="409" height="386" alt="image" src="https://github.com/user-attachments/assets/185ed9e5-2527-4bb9-884e-63b1b1b11104" />

<img width="829" height="215" alt="image" src="https://github.com/user-attachments/assets/f58c6b46-fc78-46b3-833f-0ece7b0a8ade" />

**Issue Scheduler**
- Warp Ready:
  - Valid oldest instruction in the per warp instruction buffer
  - No data dependancies vs older same warp instructions (control bit)
  - For fix latency ops: hardware ensures resources will be available, execution unit latch must be free, constant cache operand: tag lookup at issue and on miss it stalls (issues other instructions) until miss returns, switches to youngest ready warp if too long
  - Register File read ports:
    - Scheduler doesn't know port availability
    - after issue -> all instructions go through Control stage (updates dependancie counter and read clock)
    - allocate stage: fixed lat only, hold until register file read port can be used without conflict
    - Variable lat ops skip allocate and enter a queue and proceed ot register file read when no conflict
    - priority is fixed lat ops to keep timing correct
**Scheduling Policy**
- CGGTY: Compiler-Guided Greedy Then Youngest
- Greedy within warp: keep issing from the same warp if it remains eligible
- On switch, pick the youngest eligible warp in the same sub-core
- Issue youngest until miss then switch to next youngest
- if none available then one-cycle bubble
**Front-End**
- Structure:
  - 4 sub cores per SM
  - Warps assign round robin by warpID % 4
  - each sub core has private L0 i-cache, all 4 share L1 i-cache via an arbiter
- Prefetching:
  - Each L0 i-cache has a prefetcher, simple stream buffer that pulls successive blocks on a miss
- Each sub core can fetch and decode 1 instr/cycle
- greedy fetch: unless that warp's instruction buffer is full (if full switch to youngest)
- Instruction buffer has 3 entries/warp
- with 2 pipeline stages from fetch to issue, size 3 preserves greedy same warp issuing
**Register File**
  - Types:
    - Regular-> 65,536x32-bit regs per SM -> 2,048 warp-regs (32/thread x 32 threads). Evenly split across sub-cores, 2 banks/sub-core
    - Uniform RF: 64x32-bit per warp (same value for all threads).
    - Predicate RF: 8x32-bit per warp (1 bit/thread).
    - Uniform Predicates: 8x1-bit per warp.
    - SB (dependence) counters: 6 per warp (variable-lat deps).
    - B registers: >= 16 per warp (reconvergence).
- No operand collector -> collector would vary lat, breaking fixed lat ISA guarantees
- Even with register file bank conflicts -> required stall values and elasped time remain constant
- write path: 1x2024 bit write port per bank
- if a load and fixed lat op complete in the same cycle -> load is delayed by a cycle
- 2 back to back fixed lat writes to same destination bank are not delayed
- read path: 1x2024 bit read port per bank
- bank conflicts manifest as bubbles
- best fit pipeline model for fixed lat reads:
  - after issue -> control stage
  - then allocate stage reserves register file read ports
  - all fixed lat instructions occupy a 3 cycle read window redardless of operand count, if not all reads can fit then instruction stalls in allocate and creates a bubble upstream
  - variable lat ops skip allocate again
  - per sub core and per register file bank: 1 entry each holds three 1024 bit values
  - total per sub core: 6x1024 bit sub entries (2 bank x 3 operands)
  - ops needing 2 consective regs map across both banks and cache in their respective entries
  - compiler managed via per operand resuse bit
  - only cache operands sourced from regular register file
  - A subsequent instruction can hit RFC iff: same warp, same reg ID, same operand position as the instruction that cached it.
  - Eviction-on-access semantics per (bank, operand-position): any read request to that slot makes the cached value unavailable, afterward even on a hit, unless the consumer also sets reuse to re-place it

  <img width="381" height="38" alt="image" src="https://github.com/user-attachments/assets/42d437f5-37e9-48c2-b11b-5b235a7d6704" />
  
  <img width="403" height="227" alt="image" src="https://github.com/user-attachments/assets/5560cfa5-2a07-4a37-8a1d-726ca6003a69" />
  
  <img width="391" height="246" alt="image" src="https://github.com/user-attachments/assets/a0fe7ad9-c4c7-44ef-a84c-91737f5e3f93" />

  **Memory Pipeline**
  - Early memory stages are per sub core
  - final access stages are shared by all 4 sub cores in an SM (data cache and shared mem)
  - each sub core can issue 1 mem instruction/cycle for 5 consectutive memory ops
  - the 6th mem instruction stalls, downstream shared structures accept 1 request every 2 cycles (from any subcore)
  - issue cadence per sub core as more sub cores become active:
    -  1 active sub core: burst of 5 at 1/cycle then next in 4 cycles
    -  2 active: each can issue a me op every 4 cycles
    -  3-4 active: shared structure saturate at 1 req/2 cycles total -> with 4 active, each sub core issues ~1 every 8 cycles (round robin)
  - per sub core memory queue: estimeated size of 4 entries, even though 5 can be buffered across stages
  - RAW/WAW latency (loads only): issue -> earliest consumer/overwriter can issue
  - WAR latency (loads & stores): issue -> earliest instr that writes a source reg of that mem instr can issue
  - Uniform-addr vs regular-addr:
    - Global memory loads/stores are faster when addresses use uniform registers (single address computed) vs regular registers (per-thread addresses).
  - Shared memory vs global:
    -  Shared memory loads have lower latency than global.
    -  WAR latency (SMEM): same for uniform and regular regs -> implies address calc for SMEM occurs in shared structures.
    -  WAR is released once source regs are read.
    -  RAW/WAW latency (SMEM loads): 1 cycle lower when using uniform regs
  - Access size effects:
    - Loads (RAW/WAW): latency increases with read size (more data moved).
    - Loads (WAR): unchanged with size (sources only feed address calc).
    - Stores (WAR): latency increases with write size (the data value itself is a source read from RF).
    - WAR release point: when address calc completes; RAW/WAW release: when the read step finishes, independent of granularity beyond its effect on transfer time
  - Favor uniform addressing when possible (fewer address-calculation cycles and lower RAW for loads).
  - Expect burst-then-throttle behavior: 5-deep per–sub-core burst capacity, then backpressure from shared units at 0.5 req/cycle SM-wide.
  - With many sub-cores active, memory issue becomes bandwidth-limited by shared structures, not per–sub-core front-end.
  - Measured data-return bandwidth = 512 bits/cycle from the memory system back to the register file.
  - WAR latency from the constant cache is significantly higher than for global-memory loads, while RAW/WAW latencies are slightly lower (cause unconfirmed).
  - There are two L0 constant caches by access type:
    - L0 FL (fixed-latency): used when fixed-latency instructions read the constant address space.
    - L0 VL (variable-latency): used by LDC (load-constant) instructions.

