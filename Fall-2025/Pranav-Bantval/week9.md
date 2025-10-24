# Week 9

State: I am not stuck with anything

Progress: adding rtype and itype to compiler backend. we need to add instructions to the isa.

the assembler is little endian. the teal card is big endian. i don't think we want to change the format of the teal card. if it's too confusing we can write this in big endian and i can make the changes to the assembler.

rtype is currently added but can't test rtype without itype. once i add itype i will run some tests to see if basic c code can compile into asm. the isa is called twig. the compiler is called twig too.

# function calls
- graphics team brought up that predicates will be cooked if a function is called inside and outside an if
- predicate entries are now caller saved
- P0 will have to be overwritten with the current predicate (after being saved) and then restored after the function returns
- We need to add instructions for this P0 logic i think. our isa doesn't even support direct reads/writes to predicate masks
- how do we save them?
- have specific instruction type (P type) for single threaded operations
- Ptype instructions will only run on thread 0
- we might need to do the same for J type (jalr at least, maybe jal) so that the PC is controlled by one thread
- then we will also need to make sure that thread is write masked on when calculating the pc to jump to in the case of jalr e.g. auipc + (lui/addi) MUST happen for t0

# stack stack stack stack stack
- we are using ram as our stack
- each warp gets its own stack pointer to some fixed space in ram
