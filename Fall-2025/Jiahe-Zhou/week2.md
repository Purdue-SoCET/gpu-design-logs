# Week 2
- State: Finished and not encountering any obstacle.
- About this: Chapter 3.1–3.3 and 3.6

<img width="791" height="232" alt="image" src="https://github.com/user-attachments/assets/5b836317-6cb2-46cb-9d2d-140f7de5cf35" />

## 3.1 ONE-LOOP APPROXIMATION
Simplify: single scheduler
- Schedule a wrap each cycle
- Program counter to fetch next instruction
- Decode instruction and fetch source register
- Determine SIMT execution mask(in parallel with operand fetch)
- Execution in SIMD(single instruction, multiple-data)

### 3.1.1 SIMT EXECUTION 
Key feature: threads execute independently
Theory: could use predication alone
Pratical: predication + SIMT stack

SIMT stack handle:
- Nest control flow: one branch depends on another
- Skipped computation: all threads avoid a control flow path

CPU vs. GPU
- CPU: multiple predicate registers for nesting
- GPU: SIMT stack handle nesting and skipping

<img width="789" height="576" alt="image" src="https://github.com/user-attachments/assets/44e3c3ed-b485-482b-8aa5-daaccb975827" />

Divergence within a warp
- Hardware serializes paths: execute one path with others masked, then switch.
- Stack push order after divergence: push the path with more active threads first, then the smaller path -> keeps reconvergence stack depth ~log(warp size).

###  3.1.2 SIMT DEADLOCK AND STACKLESS SIMT ARCHITECTURES
SIMT Deadlock Problem
- Cause: one thread acquires a lock and exits the loop; others spin.
- Effect: Exited thread not active on SIMT stack -> cannot release the lock.
- Result: Circular dependency -> deadlock
- Solution: Replace the SIMT stack with per-warp convergence barriers.

Per-warp state
- Barrier Participation Mask: threads that must meet at a barrier (may need multiple per warp)
- Barrier State: which threads have arrived
- Thread State: ready / blocked / yielded
  - yielded state make other threads forward when deadlock
- Thread rPC: next PC for inactive threads
- Thread Active: a bit indicate if a thread is active

Instruction
- ADD: set bits for active threads(initialize the convergence barrier participation mask)
- WAIT: stop a warp split at a barrier; when all in the mask execute WAIT, the scheduler reactivates them together to keep SIMD efficiency.
- YIELD: allow switching among warp splits to maintain forward progress.

### 3.1.3 WARPSCHEDULING
Assumption
- A scheduled warp issues one instruction, and cannot issue another until it completes.

Ideal Memory system
- responded to memory requests within fixed latency
- possible to design the core to support enough warps to hide this latency using fine-grained multithreading
-  schedule warps in round robin order
-  allows roughly equal time to each issued instruction to complete execution
- If (warps × per-warp issue time) ≥ memory latency -> units stay busy
- Throughput per core increase as warps increase, until latency is hidden

trade off:
- To issue a different warp each cycle, each thread needs private registers -> large RF.
- More warps -> larger registers area, fewer execution units/cores
- Fixed chip area -> more warps per core reduces cores per chip

Round-robin scheduling
- Equal progress increases cache hits
- Accessing DRAM is more efficient when nearby locations in the address space are accessed nearby in time
-  A given thread to be scheduled repeatedly for disjoint data

## 3.2 TWO-LOOP APPROXIMATION
Goal
- To hide long execution latencies -> reduce warps per core
- Allow a warp to issue a later instruction before earlier ones finish.

One-loop problem:
- The scheduler sees only the thread identity and the next PC.
- It cannot tell if the next instruction depends on an unfinished one.

Fix: fetch + buffer + second scheduler
- Fetch the instruction to learn data or structural hazards.
- Place fetched instructions in an instruction buffer after the cache access.
- Use a separate scheduler to pick a ready instruction from the buffer.

Instruction memory
- L1 I-cache backed by unified lower levels
- Instruction buffer + MSHR(miss-status holding register) can hide instruction cache miss latencies
- Simple way for buffer organization: storage for 1+ instructions per warp.

Detecting dependencies in traditional CPU
1. scoreboard
   -  in-order execution(simple) or out-of-order execution(complex)
2. reservation stations
   - eliminating name dependencies
   - need for associative logic that is expensive in terms of area and energy

GPU choice: in-order scoreboard
- One bit per register in a scoreboard.
- When an instruction that writes a register issues, set that bit.
- Any instruction that reads or writes a register with its bit set must wait.
- Prevents read-after-write and write-after-write hazards.
- With in-order issue and in-order register reads, it also prevents write-after-read.
- Minimal area and energy, but challenges appear with many warps.

Challenge:
- GPU has large number of registers: 128 register/warp * 64 warps/core = 8192 bits/core to implement scoreboard
- A dependent instruction must keep checking the scoreboard
- multiple threads waiting and might probe the scoreboard
- 64 warps × up to 4 operands = 256 read ports if all probe

Alternative
- restrict the number of warps that can probe the scoreboard each cycle
- cons: restricts the number of warps that can be considered for scheduling.
- if none of the instructions checked are free of dependencies no instruction may be issued even if other instructions that could not be checked happened to be free of dependencies.

Solve:  Coon et al. [2008]
Rather than hold a single bit per register per warp, the design contains a small number (around 3 or 4)
each entry is the identifier of a register that will be written by an instruction that has been issued but not yet completed execution

Compare: Traditional vs. Coon et al.
- regular in-order scoreboard is accessed both when instructions issue and when they write back
- Coon et al.’s scoreboard is accessed when an instruction is placed into the instruction buffer and when an instruction writes its results into the register file

Two-loop architecture
-  first loop selects a warp that has space in the instruction buffer, looks up its program counter and performs an instruction cache access to obtain the next instruction
-  second loop selects an instruction in the instruction buffer that has no outstanding dependencies and issues it to the execution units

##  3.3 THREE-LOOP APPROXIMATION

hide long memory latencies -> support many warps per core
support cycle by cycle warp switching -> large register file containing registers for every warp

Implementation
- Naive:  one port per operand per instruction issued per cycle
- reduce area:  simulate the large number of ports using multiple banks of single-ported memories

operand collector: more transparent way -> third scheduling loop

###  3.3.1 OPERAND COLLECTOR
- Replace staging registers with collector units.
- Each instruction gets a collector unit at the register-read stage.

Multiple collector units
- Overlap source-operand reads across cycles.
- Improve throughput when bank conflicts exist.
- With more pending operands, the arbiter can exploit bank-level parallelism to read multiple RF banks in parallel.

Tolerating and reducing bank conflicts
- Collector schedules operand reads to ride out conflicts.
- To reduce conflicts: map same-named registers of different warps to different banks.
- Helps inter-warp conflicts when warps make even progress (e.g., round-robin or two-level scheduling).
- Does not fix conflicts between operands within one instruction.

Ordering and correctness
- The collector does not impose order among ready instructions of the same warp.
- Risk: a write-after-read hazard if a later instruction writes a register before an earlier read of that register completes.

Prevention options
- Enforce program order when leaving the collector for execution.
- Alternatives from prior work:
  - Release-on-commit: at most one executing instruction per warp -> can nearly halve performance in some cases.
  - Release-on-read: at most one operand-collecting instruction per warp -> ≤10% slowdown on tested workloads.
  - Bloom-based tracking: use a small bloom filter to track outstanding reads -> only a few percent impact while keeping instruction-level parallelism.

Hardware support
- Some GPUs add a read-dependency barrier to avoid write-after-read for selected instructions.
- NVIDIA’s Maxwell: read dependency barrier to avoid WAR hazards

###  3.3.2 INSTRUCTION REPLAY:HANDLING STRUCTURAL HAZARDS
Structural hazards
- cause: e.g. the register read stage run out of operand collector units

What happens when an instruction encounters a structural hazard in a GPU pipeline?
- single-threaded in-order CPU pipeline: Stall younger instructions until the blocked one can proceed.

Not desirable for highly multithreaded throughput architecture
- stall signal may impact the critical path
- stalling an instruction may cause instructions from other warps to stall

Solve: instruction replay
- CPU: speculatively scheduling a dependentinstruction upon an earlier instruction that has variable latency
- GPU: avoid speculation as it tends to waste energy and reduce throughput
- To implement instruction replay a GPU can hold instructions in the instruction buffer either until it is known that they have completed or all individual portions of the instruction have executed

##  3.6 RESEARCH DIRECTIONS ON REGISTER FILE ARCHITECTURE
To switch between warps rapidly -> hardware warp schedulers and store the registers -> huge capacity of register files

minimize register file storage area
- low-port count SRAM banks -> accessed in parallel; supply the operand bandwidth required to sustain instructions running on the wide-SIMD pipeline at peak throughput
- use operand collector to minimize bank-conflict penalties

### 3.6.1 HIERARCHICAL REGISTER FILE
70% values read once; ~10% read >2 times
capture this short lifetime of the register values -> add RFC(register file cache)
- hierarchy of the register file
- dramatically reduces the access frequency to the main register file

RFC strategy
- Allocates entry for the destination operand of every instruction(FIFO)
- Avoid pollution: source operands miss don't load into RFC
- Default:  write evited value back to main register file
- Liveness: register marked dead won't write back to main register file

RFC with two-level warp scheduler -> reduce size
- Keep a small active warp pool (e.g. 4–8 of 32)
- RFC store active warps’ values only -> smaller RFC
- long-latency operations flush RFC entries -> space for new active warps

LRF(Last Result File)
-  buffers the register value produced by the last instruction
-  Replace RFC with ORF(operand register file)
   -  managed by compiler
   -  removes the tag-lookup required by the RFC

### 3.6.2 DROWSY STATE REGISTER FILE
Tri-modal register file design
- ON: normal mode
- OFF: not retain the register value
- Drowsy: retain the register value, but awaken to ON mode before access

Strategy
- non-allocated registers -> OFF mode
- allocated registers -> Drowsy mode after access
- long pipeline in GPU -> not significant latency of awake registers from drowsy

### 3.6.3 REGISTER FILE VIRTUALIZATION
live registers in a GPU thread tends to be small
up to 60% of registers go unused

register renaming to virtualize physical registers -> 50% register file size or double threads
- a thread starts executing with no registers allocated
- physical registers are allocated to destination registers as instructions are decoded
- final read annotations: compiler analysis to determine the last read of a register
- May need extra bits in instruction encoding

reducing the size of the register file by 50% by employing spilling increased execution time by an average of 73%
Use metadata instructions from liveness to reclaim registers

### 3.6.4 PARTITIONED REGISTER FILE
Pilot Register File -> partition the GPU register file into fast and a slow register file (FRF and SRF)

FRF
- Use regular SRAM
- Every warp has 4 entries
- service most of the access to compensate for the slowness of the SRF
- FinFET allow inactive warp switch to low power mode
- benefits of two-level scheduling without explicit warp pool swaps

SRF
- NTV(near-threshold voltage) SRAM
- lower access energy and lower leakage power
- longer lantency -> take several cycles
- operand collector handle additional latency

Not hierarchical caching: partitions hold exclusive sets, fixed per warp
pilot CTA profile the most-frequently used registers
recorded in a lookup table that is accessible to every subsequent warp from the kernel launch.

### 3.6.5 REGLESS
Eliminating the register file -> replace with an Operand Staging Unit(OSU)

- Compiler splits kernel execution into regions(contiguous in a basic block)
- Select boundary between regions to limit the number of live registers
- CM(Capacity Manager) determine warps scheduling, preloads region registers into OSU
  - OSU: 8 banks and 2 instruction/cycle.
- CM maintains state machine for next-region registers present
- reduce memory traffic between OSU and memory -> use register compression(affine values)

Evaluation: 512-entry OSU ≳ performance of 2048 KB RF, 25% area, –11% energy.
