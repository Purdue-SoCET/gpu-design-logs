# Week 6

State: I am not stuck with anything

Progress: Currently working on creating a backend in arch/ dir of ppci for the new ISA. Finalized most of the ISA encoding (possible change to yield bits?)

## design review presentation / design choices
- drafted design review presentation (link in discord)
- our design choices included:
- complex isa instructions implementation (like fma/sin/cos),
- predication and loop control flow
- rfc,
- threadid,
- floating point arithmetic
- packet optimization

Our main discussions were with rfc and predication/loop control flow.

### RFC
- many solutions to the spills/fills for the RFC, the final one agreed by the entire hardware and compilers team is as follows:
- rfc is just 8 numerically defined registers e.g. x0-x7 or x1-x8 if we use x0 as zero register
- rfc is purely compiler managed, the compiler will decide when any register should be written in rfc by setting the rd to x1-x8
- for spills, the compiler will decide if the value being overwritten is necessary, if not, free to overwrite
- if it is necessary, compiler will write the existing value into a register, and then overwrite it in the rfc
- e.g. addi x200, x1, x0 --> overwrite x1, x10, x10
- if the register file is completely full write data will be spilt to the stack

### predication and control flow
- predication occurs when a branch happens (if/else statement) and some threads take the if block and some take the else block
- the outcome of a branch operation will be written to a predicate table given by the rd flag in the branch instruction
- the predicate table stores WEN masks for all 32 threads, there is a predicate table for each warp
- after the branch operation, the pc steps into the if statement and uses the predicate mask just calculated for threads to write if they satisified the condition
- then the pc steps into the else statement and uses the inverse of the predicate mask created to write to the threads that did not satisiy the condition
- for loops: int i = 0; i < val; i++
- i<val is a branch operation that creates a predicate, but how do we know when the for loop is done?
- we will read the predicate mask calculated at the end of every iteration
- once the predicate mask is 0, no threads are performing any operation during the for loop and the thread is complete
- if the predicate mask is not 0, we need to jump to the top of the loop (i<val), recalculate the predicate mask and run the contents of the for loop with it once again

I will briefly summarize the ambiguity with the other choices. 

For threadId, we needed a way for software to distinguish between threads without having to look inside warps. Hardware should have an identifier for each thread to do this.
I thought we could have software take the identifier and then make data structures to organize the thread but it seems like this might happen in hardware. 
Either way, this doesn't directly affect compilers, it's between software and hardware to agree on and manage (I believe we're taking the hardware approach) and the compiler can just
send an opcode to return threadId and possibly include thread dim/blockdim as rs1/rs2 if needed.

For floating point arithmetic, there was a choice to have unique floating point registers. We decided that we don't need to do this if we can just keep track of which registers
are floats and which are ints in the compiler itself. The compiler would have to support an instruction floating32_to_int32 and vice versa.

For packet optimization, this has been briefly discussed and basically the hardware team wanted packets to come in a specific order to optimize their design.
We could do this after having a baseline for the compiler. Due to how yield bit will function, it's likely that only 1 packet will be in the hardware pipeline at a time.

Complex instructions: we decided not to support fma because we don't have 3 read ports and rd=rs1*rs1 + rd might cause overwrite issues in the compiler.
We will do sin/cos and floating point and hardware will have special units for those to optimize performance.
There was definitely at least 1 more instruction I thought we needed to add but I completely forgot... we have < 64 instructions right now (54-55) so we could add 9 more without much difficulty
