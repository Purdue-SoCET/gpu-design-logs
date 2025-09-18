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
- 


