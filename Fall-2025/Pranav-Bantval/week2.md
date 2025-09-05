# Week 2

State: I am not stuck with anything, don't need help right now. 

Progress: Read chapters 3.1-3.3 & 3.6 from provided textbook. Watched the MIT videos on pipelining a single cycle processor

## Video Summary
- Data hazards can be solved with stall cycles or bypass
- Control hazards can be speculated as next instruction PC+4 & provision to annull for jumps and branches.
- Exceptions and interrupts caught with BNE  

## Chapter 3 - SIMT core instruction & register data flow

### 3.1 - one loop approximation
- Simplified GPU model with a single scheduler, similar to what might be inferred from CUDA documentation
- Execution unit, threads grouped into warps, scheduling is at the warp level
- Warp's PC fetches instruction & decodes
- source registers fetched
- SIMT execution mask determined parallel
- instructions executed on SIMD function units if mask bit active
- Execution unit has SFU, load/store unit, floating point unit, integer unit, tensor core
- can execute a warp across multiple cycles w/ pipelining (higher frequency higher power)
- SIMT deadlock is prevented through compiler restrictions (structured synchronization), hardware mechanisms (SIMT stack or stackless execution masks), and scheduler fairness (guaranteed forward progress)

### 3.2 - 2 loop approximation

- 2 loops: fetch: scheduler selects a warp, fetches warp's instruction from memory, places into instruction buffer
- issue loop looks at the i-buffer and checks for unresolved dependencies to buffer if needed
- scoreboard tracks register dependencies (RAW hazards)
- supports pipelining of instruction and fetch execution
- captures latency hiding more than 1 loop model

### 3.3 - 3 loop approximation
- GPU register files are huge, giving ports all read operands would require massive area and energy
- operand collection sits between register files and execution units
- collects operations over multiple cycles and buffers operands until all ready for execution
- Registers are banked; stored in multiple single-ported SRAM banks
- arbiter+crossbar handle bank conflicts
- replay mechanism if an instruction can't be issued due to bank conflicts
- models bandwidth and structural hazards explicitly

### 3.6 - Research Directions on Register File Architechture
- to reduce the power and area register files consume (more optimizations on top of operand collector)
- hierarchical register file - small register file cache
- exploit short register lifetimes w/ compiler hints to avoid unnecessary writes & works with 2 level warp
- drowsy state register file - split into fast and slow register files (FRF & SRF)
- SRF built w/ near-threshold SRAM low power and high latency
- operand collector hides latench
- FRF has drowsy mode for inactive warps
- Register file virtualization - logical registers dynamically mapped onto a smaller physical pool, reduces static power consumption
- partitioned register files divides RF into banks tied to subsets of warps
- RegLess radically reduces large RF by using operand staging buffers & employs compression to shrink operand storage
