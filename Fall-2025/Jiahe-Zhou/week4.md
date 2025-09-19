# Week 4
- State: Finished and not encountering any obstacle.
- About this: Chapter 5.1s

## 5.1 Thread Scheduling — Notes

- GPUs need massive parallelism to hide long memory latencies
- Thread hierarchy: threads → warps → threadblocks (CTAs) → cores (SMs)
- Scheduling happens at:
  1. Thread → warp fusion (compile time)
  2. CTA → SM assignment (launch time)
  3. Warp scheduling (every cycle)
  4. Multi-kernel arbitration (across kernels)

## 5.1.1 Assignment of Threadblocks to Cores (Research)

- Baseline round-robin
  - Assign CTAs to SMs until any resource (RF, shared mem, warp slots) is full
  - No preemption → resources freed only when CTAs finish
  - Some CTAs wait off-chip until resources free
- Throttling CTAs — Kayiran et al. (2013)
  - Problem: too many CTAs → memory contention stalls
  - Method: start with half CTAs per SM, monitor idle cycles vs. memory-delay cycles
  - If mostly waiting on memory → stop issuing new CTAs, pause some active CTAs
  - Effect: lower memory pressure, better performance despite fewer active CTAs
- Equalizer — Sethia & Mahlke (2014)
  - Goal: dynamic resource tuning for performance/energy balance
  - Monitors: active warps, mem-wait warps, ALU-ready warps, MEM-ready warps
  - Decides: #CTAs per SM, core freq, memory freq
  - Modes:
    - Energy-saving → scale down unused resources
    - Performance → boost bottleneck resource
  - Local SM decisions → global frequency controller aggregates them
  - Observations:
    - Compute kernels: lower mem freq
    - Memory kernels: lower core freq
    - Cache-sensitive: fewer CTAs if mem-stalled

## 5.1.2 Cycle-by-Cycle Scheduling (Research)

<img width="938" height="601" alt="image" src="https://github.com/user-attachments/assets/2b54f552-eb87-4879-9cee-9f648fa0f104" />

- Early Characterizations — Lakshminarayana & Kim (2010)
  - Fairness-based scheduling + DRAM row locality helps early balanced workloads
  - ICOUNT (prioritize fastest warp) didn’t help without caches
- Two-Level Scheduling
  - Gebhart et al. (2011c):
    - Warps split into active vs. inactive pools
    - Smaller pool → lower scheduler energy cost
    - Warps leave active pool on long-latency mem ops, return round-robin
  - Narasiman et al. (2011):
    - Groups of warps as fetch groups
    - Groups stagger long-latency ops to preserve row-buffer locality
    - Improves performance vs. purely round-robin
- CCWS — Rogers et al. (2012)
  - Detect intra-warp locality loss from per-warp victim tags
  - Raise warp’s score when its tag reappears on misses
  - High score → throttle warp (stop L1 access)
  - Increases L1 hit rate, reduces cache thrashing
- DAWS — Rogers et al. (2013)
  - Builds on CCWS:
    - Track per-warp cache footprint in loops
    - Adjust footprint when divergence removes lanes from loop
    - Preemptively throttle warps with large loop footprints
  - Greatly closes gap between naive and optimized kernels
- Prefetch-aware — Jog et al. (2013b)
  - Non-consecutive fetch groups → more DRAM bank parallelism
  - Coordinate with prefetcher to space out demand requests
- CTA-aware — Jog et al. (2013a)
  - Group warps by CTA boundaries
  - Reduce inter-CTA bank conflicts by staggering CTAs
  - Throttle + prefetch for better DRAM row locality
- DWS — Meng et al. (2010)
  - Split warps when some lanes hit and others miss
  - Runahead threads prefetch for slow threads → lower stall time
- DWF — Fung et al. (2007)
  - Dynamically regroup threads by branch outcome
  - Reduce control divergence penalty
- TBC — Fung & Aamodt (2011)
  - Compact warps by CTA membership
  - Schedule threads from same CTA together → better coherence
- Mascar — Sethia et al. (2015)
  - MAS (Memory-aware Scheduler):
    - Two queues: memory vs. compute warps
    - EP mode (balanced): memory warps first
    - MAP mode (mem-stalled): compute warps first, only 1 “owner” warp issues memory
  - CAR (Cache Access Re-execution):
    - Re-execution queue for stalled LSU ops
    - Enables hits-under-misses, avoids LSU backpressure
    - Requests from non-owner warps are delayed if miss again

## 5.1.3 Scheduling Multiple Kernels

- Chimera — Park et al. (2015)
  - Enables GPU preemption (previously unsupported)
  - Three strategies per CTA:
    1. Full context save/restore
    2. Wait to finish
    3. Stop + restart (if idempotent)
  - Selects mix of CTAs to preempt to hit user-specified latency target
  - Balances switch latency vs. throughput loss

## 5.1.4 Fine-grained Synchronization–Aware Scheduling

- ElTantawy & Aamodt (2018)
  - Problem: spin locks waste cycles and energy
  - Detect spin loops using:
    - PC path history (LSBs)
    - Predicate register updates
  - Reduce priority of warps stuck in spin loops after locks are released
  - Result: +1.5× performance, –1.6× energy
