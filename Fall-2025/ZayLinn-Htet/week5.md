I am not currently stuck or blocked

Week 5: 9/19/25 - 9/25/25

Sunday (9/21/25): GPU Team weekly meeting
- static timing analysis in compiler; the life cycle of an instruction
- order instr in compiler to track when an operant will be used
- look for conference workshops on how PCCI works (YouTube vids)
- Look into PPCI for how translate the assembly into registers
- Get list of ISA instructions to implement and theirs ops
- Look through optimization IR
- 6-8 per warp in Reg File Cache Eviction
- Updated address size {7'b opcode, 6'b rs1, 6'b rs2, 6'b rd, 4'b predicate mask, 1'b packet start, 1'b packet dependency, 3'b reg file cache sel, 9'b reg file cache sel addr, 11'b imm}
 - Predicate mask is a 4-bit addr that goes to the predicate mask table with 2^4= 16 entries, with 32-bits (one bit per thread) entries of masks; table will be in hardware
 - Upon branch instruction; GPU in three cycle approximation (fetch, decode, execute);
 - By the time branch/jump instr in execute, can write into predicate mask table for which threads are going into branch taken and which won't go into branch taken
 - Scheduler will load and run both instructions from taken and not taken paths, and only those with a mask bit on will run
 - Communicated with hardware team to see how the register file cache will run
 - Register file cache will have 6 (or 8) spots only and they will store either the rd or rsel1/rsel2 of an instruction if it will be seen to be used again anytime soon
 - Had issues deciding how the replacement/evicting protocols would be, and how much of the instruction width this would take up
 - Had idea to utilize register addrs itself as a way to store replacement address in a separate hardware table; would mean we can go back to 32 bit instr
 - Still ongoing discussion about whether to keep this 32-bit instr or extend up to 48-bit instr
 - Didn't get a chance to talk to graphics team about what instrs they may have needed
 - Still need to continue discussion with hardware on how many bits of the instr that'll need to be used for reg_file_cache
 - Main goal by next week's meeting is to get the instrs that the graphics will be working with, and determing ISA operand formatings for each; also to look into PPCI's assembly aspect and see how we can write ours on there
 - This can be done by looking through PPCI's current repo files on their RISC-V ISA and see how their encodement will work


Monday (9/22/25): Compilers Team & Sooraj Weekly Meet
- ThreadID will be a register in the hardware
- BlockDimension can be global variable; but BlockID and ThreadID can be finicky
- First thing a warp does is to register itself; first one gets to go through, and + for each next
- Look into loop unrolling and software pipelining
- can only packetize the things in the GPU kernel; don’t worry about CPU initial execution for now (separate compilers)
- if 32 warps in hardware and thread block has more than 32 warp; manually put in code 32 warps then put next 32
- if 32 warps goes and faces a block, dequeue them and run another set of 32 warps
- can tell hardware to not have a thread blocks of more than 32 warps
- point of reg file cache isn’t just for raw hazards; just for more locality usage
- We need to see how we will be determining the threadID for each thread by communicating with hardware
- For myself, I need to review myself on how threads, thread blocks, warps, and kernels come together, and how each instruction or package will be run through them

Monday (9/22/25): SoCET Project Proposal Presentation
- Presented with Jack and Pranav in front of the SoCET leads about our Compiler's Team's Problems, Tasks and Timeline
- Received feedback to name our Compiler something (Ex. Robin)
- Need to stop calling the Graphics team's code "CUDA"
- Make more edits to the timeline to incorporate working on packages reordering and organizing
- Overall presentation went fine and we had good feedback to work with