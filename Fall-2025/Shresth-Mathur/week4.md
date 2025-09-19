## *Analyzing Modern NVIDIA GPU Cores* Notes 

by Shresth Mathur

## 1\. Motivation & Goal

* GPUs have become the dominant platform for HPC, ML, and scientific workloads, especially for LLM training & inference.  
* Most academic simulators (e.g., GPGPU-Sim, Accel-Sim) still rely on Tesla-era models (2006) – very outdated.  
* This paper reverse-engineers modern NVIDIA GPU SM cores (Ampere, Turing) and integrates findings into Accel-Sim.  
* Goal: get simulation models that reflect reality much more closely.  
  * Leads to more relevant research.

## 2\. Contributions

* Dissected issue logic: warp readiness rules, CGGTY (Compiler-Guided Greedy Then Youngest) scheduler.  
* Proposed plausible model for fetch stage with per-warp instruction buffers & stream buffer prefetcher.  
* Characterized register file organization, confirmed absence of operand collectors, detailed RF cache behavior.  
* Revealed key memory pipeline details: queue depth, issue bandwidth, per-sub-core throughput.  
* Built an improved Accel-Sim SM model.  
  * 13.98% MAPE vs hardware, an 18% accuracy improvement over previous state-of-the-art.  
* Demonstrated software-assisted dependence tracking (compiler-set stall & dependency counters) is more efficient than hardware scoreboards.

## 3\. Methodology (Reverse-Engineering)

* Wrote microbenchmarks in SASS (hand-tuned assembly).  
* Surrounded code regions with GPU clock reads to measure exact cycle counts.  
* Varied registers to reveal bank conflicts.  
  * Measured 0-2 cycle bubbles depending on which bank operands were mapped to.  
* Used CUAssembler to manipulate control bits, explore semantics of stall counters, yield bits, dependence counters.

## 4\. Control Bits & Dependency Handling

* Compiler handles hazards (unlike older scoreboard-only GPUs).  
* Each instruction encodes:  
  * Stall Counter (for fixed-latency producers): warp is frozen until counter hits 0\.  
  * Yield Bit: forces scheduler to switch to another warp next cycle.  
  * Dependence Counters (SB0–SB5): track variable-latency producer/consumer relationships (RAW, WAW, WAR).  
    * Producer increments counter at issue, decrements at write-back (or after read for WAR).  
    * Consumer stalls until counter reaches zero.  
* This avoids area/power overhead of fully wired scoreboards and still preserves correctness.  
* Verified by experiments: if counters not set correctly, RAW hazards cause wrong results.

## 5\. Issue Scheduler Findings

* Warp readiness conditions:  
  * Must have a valid instruction in per-warp buffer.  
  * No pending dependencies (stall counter=0, dep. counters satisfied).  
  * Execution unit latch must be free.  
* Fixed-latency instructions pass through two stages after issue:  
  * Control: increments counters, updates clock.  
  * Allocate: reserves RF read ports; stalls here if not enough bandwidth.  
* Variable-latency instructions bypass Allocate.  
  * Sit in a queue until safe to proceed.  
* Scheduling Policy: CGGTY.  
  * Greedily issue from same warp until blocked, otherwise pick youngest ready warp.  
* Confirmed through warp timing experiments.

## 6\. Front-End / Fetch

* Each SM has 4 sub-cores; warps distributed round-robin.  
* Each sub-core has L0 I-cache \+ stream buffer prefetcher.  
* Fetch stage tries to follow same warp as previous cycle (to keep IB full) unless buffer is full, then switches to youngest warp.  
* Instruction Buffer per warp \= 3 entries – necessary to support greedy scheduling without stalling.

## 7\. Register File & Cache

* Regular RF: 65536 32-bit regs per SM, banked (2 banks per sub-core).  
* Uniform RF: 64 regs per warp for broadcast values.  
* Predicate RFs: for thread masks & branch outcomes.  
* Finding: no operand collectors.  
  * Latency must be fixed and predictable.  
* RF banks: 1024-bit read/write ports; bypass network forwards results before write-back.  
* Register File Cache (RFC): small, compiler-controlled cache with reuse bits.  
  * Each bank has 3 entries (one per source operand).  
  * Reuse bit must be re-set on every instruction that wants to keep operand cached.  
  * Behaves like a small software-managed operand buffer to avoid RF reads.

## 8\. Memory Pipeline

* Each sub-core can issue 5 consecutive memory instructions before stalling.  
* Global structures accept 1 mem request every 2 cycles.  
  * Throughput bottleneck when multiple sub-cores active.  
* Address calc throughput: 1 per 4 cycles per sub-core.  
* Measured latencies (RAW/WAR) for different memory types:  
  * Shared memory faster than global.  
  * Using uniform registers for addresses reduces latency (single address computation).  
  * Constant cache accesses have surprisingly high WAR latency; discovered two constant cache levels (L0 FL vs L0 VL).  
* LDGSTS (global-to-shared DMA) bypasses RF entirely.  
  * Saves cycles and registers.

## 9\. Simulator Enhancements (Modeling)

* Integrated all above findings into Accel-Sim:  
  * New L0 caches w/ stream buffers.  
  * CGGTY scheduler, control \+ allocate pipeline stages.  
  * Accurate RF port conflicts & RFC behavior.  
  * Modeled tensor core latencies based on operand type.  
* Extended tracer tool to capture control bits & operand IDs at compile time (not JIT).

## 10\. Validation & Results

* Benchmarked against 143 workloads across 12 suites.  
* RTX A6000: MAPE improved from 32.22% (Accel-Sim) to 13.98%.  
* 90th percentile error dropped from 82.6% to 31.5%.  
* Instruction prefetcher: stream buffer size 16 gave best match (close to perfect I-cache).  
* Register file cache critical for some workloads (e.g., sgemm).  
* Dependence management using control bits.  
  * 0.09% area overhead vs 5.3% for scoreboard while matching accuracy.

## 11\. Key Takeaways

* Modern NVIDIA GPUs rely heavily on compiler-guided execution, not purely hardware scoreboard.  
* Software \+ minimal hardware support (stall counters, dep counters) yields big area savings and good performance.  
* Stream buffer prefetching is likely implemented and works well for regular control flow.  
* Operand collector units are gone.  
  * Fixed latency assumption is fundamental to pipeline predictability.  
* Simulation research should adopt these updated models to avoid misleading conclusions from Tesla-era assumptions.
