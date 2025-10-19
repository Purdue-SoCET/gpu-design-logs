# Week 8

State: I am not stuck with anything

Progress: the compiler is hard to work on. i made an assembler for the other teams to use to test their functional simulator.

no general meeting and no compiler's meeting since fall break

slow week since 437 exam thursday too

I will look at how aihw implemented custom isa on their compiler and try to replicate their process. I tried implementing all of the types at once and it was very hard to debug, so I will just try to do rtype before next sunday (26th). 

The assembler (assembly to binary) is mostly correct I believe. Currently it is in the format `rd, rs1, rs2, pred(decimal < 31), packet_start_bit, packet_end_bit`. I do not know if this format will be changing after it goes directly from the compiler (C to binary). Either way, compilers can support the assembler updates/changes, and the binary should not change even if the format of the operands do.
