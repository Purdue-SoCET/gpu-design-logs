State: I am not stuck with anything, don't need help right now. 

Slide is done for Monday. Below is book and then paper notes. Taking notes about pipeline seperately.

## Research Paper

### Background and Motivation
- Paper describes a more modern architecture. 
![alt text](image-8.png)
- Round robin scheduler selects warp witih instruction in the L1 Icache and has empty slots in the Ibuffer. 
- In issue, GTO scheduler selects a warp not waiting and its oldest instruction with no dependency. Previous architecture had two scoreboards for this.
- Instruction goes to collector unit and waits for operand retreival. Then moves to datapath when ready and then executed by correct unit. Writeback follows.
- This model misses some modern features. The hardware is reverse engineered using 3rd party assembly tools.

### Control bits
![alt text](image-10.png)
- The compiler is now responsible for handling data dependency. ASM instructions now include control bits taht manage dependencies and this improves performance and energy.
- Sub core issues a single instruction per cycle. 
    - Compiler indicates when instructions are ready for issue using the control bits.
    - Warps now have a stall counter to determine if it is a candidate for the scheduler.
    - Set by compiler, then decrease by 1 per clock. This is used in place of the scoreboard.
- Control bit yield
    - Do not issue an instruction of the same warp. Each instruction sets both of these. 
- Variable latency instructions have a dependence counter bit, with registers that can count for this purpose. 
    - Producer can increase the register at issue and decrease at writeback.
    - Up to two counters in instruction btis
    - One decreased at writeback and other at register read
- Above approach can be limited if more than 6 instructions needing to access or generate this data. Could either be in the same register or reordered.
- Instructions exist to stall until certain count registers are ready. Can solve some hazard issues. 
### GPU Cores Microarchitecture
![alt text](image-9.png)
#### Issue Scheduler

 - Warp readiness. Warps are candidates for issuing their oldest instruction if some conditions are met. Can depend on other instructions or hte core state. Resources must also be guaranteed to issue.
    - This includes execution unit. Instructions can be latched entering hte execution unit.