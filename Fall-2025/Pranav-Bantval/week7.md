# Week 7

State: I am not stuck with anything

Progress: some backend work to the compiler, setting up registers and slowly implementing instruction types

majority of the greencard is complete as well

## compiler meeting
- need functional simulator to run integration testing on the compiler
- for now we can do unit tests on various parts of the compiler
- basic c code to hand translate to assembly and verify output
- only responsible for gpu processing compiling and not setup/initialization
- forget about packetization algo/caching/optimization for now and try to get a bare minimum compiler with the new ISA

## misc
- modulo can take 3 instructions, div mul sub to identify remainder
- graphics team says we should change sqrt to isqrt (inverse sqrt)
