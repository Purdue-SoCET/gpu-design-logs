# Week 7
statement: I am not stuck.
## Progress
- Presentation on Sunday for each subteam.
## Notes from Presentation 
### Frontend Hardware 
- Top level workflow: Thread Block Scheduler -> Warp Scheduler -> Fetch -> Predicate Register File/Decode -> iBuff -> Issue -> Operand Collector
- Thread Block Schduler receives kernel dimensions and assings to the SM core.
- Use two level warp scheduler
- The decoded instruction was sent to 16 iBuffers, which are indexed by warp groups
### Compiler
- Use 32 bit size of ISA.
- Register File Cache uses FIFO for eviction when writing back to register file
- Group independent instructions into packets and it is marked by one bit in the instruction. 
### Backend Microarchitecture
- The Main Register File is split into two banks for even and odd warp ID to allow colesced access.
- Funtion Units: INT32, FP32, TRIG Unit, LD/ST Unit
- Cache: Instruction cache, L1 cache, L2 cache
### Thinking on relevance to our Graphics Team
- Our shaders will contain conditional logic like if statement. Since the predication logic is designed by compiler and it is iplemented in fronted hardware, we should implement the code to reduces the performance loss from thread dievrgence.
- The backend team uses Access Coalesce Unit in LD/ST to combine multiple memory requests from a warp. We can improve the performance by putting adjacent data into memory, to make contiguous memory access.

