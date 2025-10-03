# Week 6 Design Log
## 9/26/25 - 10/2/25
I am not currently stuck or blocked

## Saturday (9/27/25) - Personal Review
- Reviewed GPU Architecture Components because I felt lost
- Had the following questions and reviewed knowledge by myself
   - What are the physical components on a SM? What are the physical components on a CUDA Core?
   - What is the GPU Kernel? Is it part of the Compiler, the Warp Scheduler or the Hardware?
   - How is the work from a Kernel distributed accross multiple Streaming Multiprocessors?
   - Is the Warp Scheduler part of Hardware or Compiler?
   - In a Load/Store, is the coalescing of memory done by the hardware or the compiler?
   - How does a Warp Dequeue itself?
   - How does it keep the memory access going?
   - How does it know when the specific memory access is done?
   - How does it know when to come back? Who takes care of all of this? The hardware or the compiler?
   - What is a packet? How does a compiler create it? How does a Warp Scheduler execute it?
   - Is there a register file per warp or register file per thread?
   - How does a Thread get its own ThreadID?
   - How is a Warp marked as having a complete an instruction?
   - Is the Warp Scheduler part of the compiler or the hardware?
   - How are packets determined in a kernel? How are they grouped? How are they nested?
   - Ask questions about register file cache
   - Does compiler have to do anything for L1/L2 and DRAM, and Register File?

# Sunday (9/28/25) - Weekly Sunday Meeting
- Meeting was mostly talking with graphics and hardware on design choices

- Compilers
   - Created separate discord chats for each of the compiler's main tasks (PPCI, Packet Ordering, ISA, and RFC)
   - Recapped on decisions from previous week and questions remaining to be answered
      - Are we having matrix operations (to graphics)
      - Are we sticking with 32bit instr or 48bit instr? (Do we need extra bits for reg_file cache, for immediate?)
      - Cache spilling into register file
      - If last bit of instr no longer used, add it to the predicate bits (4->5)?
      - Being able to exceed predicate regs and rerun instr to recreate mask

- Graphics
   - Approached graphics to clarify set of instructions they'd plan to use
   - Regsiter File won't have separate places for integer and floating point data, they will be stored the same
   - Compiler has to keep up with which register has what type of value
   - If an int and float operation, must convert int into float
   - Value type conversion instruction needed in hardware

- Hardware (Packets)
   - Clarified and finalized policies of packet ordering with Yash
      - Packets Ordering by Compiler
         - 1) Packets with no mem-access instrs and no dependencies
         - 2) Packet with mem-access instrs and no dependencies (fill up mem access queue)
         - 3) Packet with non mem-access instrs and dependencies to packets (1 and 2)
         - 4) Packet with mem-access instr and dependencies (1, 2, and 3)
         - ...
         - N-1 Packet with no mem-access instrs and dependencies to packets  (1, 2, ... N - 2)
         - N Packet with mem-access instr and dependencies to packets (1, 2, ... N - 1)
      - every instruction in a packet will have the same predicate
      - There can be packets with the same predicate mask
      - issue of nested for loops predicates
      - if nested branch instr. rd uses 5 bits to determine where to store to. And mask to determine where to run

- Hardware (RFC)
   - Was proposed to implement a LRF (Last Result File) to further optimize efficiency; may leave idea for if we have time
      - Last Result Register File has three banks per instruction
   - There were some papers on GPU Compilers that we should try to take a look into
   - Stick to Register File Cache being a compiler-controlled component
      - Will run in FIFO
      - If overflow, flows into Main Register File
      - If Register File overflows, flows onto Stack
   - Hardware needs to implement a stack
   - 8 Registers in Register File will be used specifically for the Register File Cache (RFC)
   - Eviction from RFC will be done in two instructions (1. Move RFC->RF and move new_val->RFC)

- Overall (ISA)
   - Finalized that Instruction will only be set 32-bits
   - There is no need to be that much space for intermediates (not even for floating points)
   - Extra bit will go to predicate to have 2^5 = 32 entries for the predicate masks
   - Will stick to 7-bit opcode, but will try to minimize to 32 if possible
   - No more RFC enable bits or selects needed as the rs1, rs2, and rd themselves will go to the part of the register file that is the RFC
   - RS2 and RD2 spots can become the immediate when needed on certain instruction types (Ex. SW, or LI)
   - Decided to break down fused instruct fma (multiply add) into just individual multiply and add instructions

   - All warps start at the same PC but diverge off into different paths
   - Only one warp is "running" at the same time
   - If mem_access instr, warp dequeues and enqueues next independent instruction to run in another warp

- Tasks by next meeting
      - Figure out how to get ThreadID? (special reg in general purpose reg file)
      - Determine how to figure out how a loop works with Predicate Registers?
      - Start documenting decisions in a Google Docs that can be viewed by other teams
      - Start working on presentation with coverage on the following topics
         - Execute one block at a time
         - Special register to define threadID (0-1023)
         - 32 bit instr and format
         - Immediate (break into two instructions)
         - Predicate Mask Table
         - Package Ordering
         - Register File Cache Eviction
      - Read through NVIDIA GPU design paper


# Monday (9/28/25) - Weekly Meeting with Sooraj
- Asked about immediates, figuring out how predicates would work in a loop, stack pointer and RFC
- Have a load constant instruction (little constant table that compiler can directly access, that hardware will fetch from)
- Get bit address of array
- Don’t do FMA please (rd will get clobbered in the process)
- If unconditional jump that is predicated, is that enough to go through a loop? (Loop is conditional jump)
- In loop, all threads will keep running until all their predicate masks == 0, so they all can move on. Ones that are already equal 0 will keep running and assigning to 0, until all are 0
- Special instruction (one instruction) to convert INT into float
- Stack pointer in hardware for if reg file is full
- If pred table gets full, spill to reg file, then spill to stack
- Stack is controlled by compiler

- Team started working on slides for Design Review Presentation
- Added slide about Packets Reordering Optimizations
- Will look into other slides and polishing up my current one later in the week


## Thursday (10/2/25) - Weekly SoCET Meeting
- William Russel from the company Relativity Space came to talk about themselves
- Was a Purdue AAE graduate and came to advertise that they do indeed need people for electrical positions

- Decoupling Networks and Switched Mode Power Supplies presentation by Eric King
- Most imortant thing is fundamentals
- SMPS-IC designer responsible for everything required to deliver power
- Rise and fall of charge in capacitor will create an oscillation that will eventually lead to needed voltage
- Find Power Distribution Network at specific range of frequencies
- 1) Calculate max frequency with minimum period
- 2) Determine max AC current
- 3) Determine max allowable voltage ripple
- 4) Calculate max PDN impedance
- Voltage second balance to get a zero average voltage, otherwise don't work
- Charge in charge out or the voltage will change
- 1 McChicken = 1930 Capacitors\
- Understand physics of your problem, and fundamentals of your components, to problem solve
- SMPS IC DEsigners, work with board services to design layout and extract parasitic inductances
- Work with Systems for floorplan
- Vendor websites to obtain data on capacitors
