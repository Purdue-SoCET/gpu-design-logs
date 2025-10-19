# Week 8 Design Log
## 10/10/25 - 10/16/25
I am not currently stuck or blocked

## Saturday (10/11/25) - GPU Teal Card
- Worked on refining and polishing up ISA for other teams to view
- Discussed with teammates on presence/absence of instructions like addi/xori/subi
- Created new instruction types for special instructions like Predication and CSR
- Clarified on hardware executions of specific instructions
- Mentioned usage of immediates in instructions like lui (shift or anding)
- Brought up case of un-used immediates in sin/cos/invsqrt
- Suggested idea of using immediate space as possibly for rounding amount? (will have to check with hardware)
- Moved around some instructions from different types or into new special types
- Thinking to make a new Function F type for sin/cos/invsqrt

## Wednesday (10/15/25) - Abstract Draft
- Worked on Abstract for VIP Submission
- Had Discord Call to discuss with teammates on how questions should be answered
- Decided the main focus of our work would be for making the ISA, dealing with Register File Cache assignments, setting Predication usage policies, and creating Packet Optimizing algorithms
- Difficult to figure out ways of measuring success other than with a testbench to see functional correctness
- Different from usual GPUs because compiler would deal with RFC assignment rather than the hardware (reduce hardware complexity)
- Asked Sooraj to check for feedback

## Thursday (10/16/25) - Abstract Final and Submission
- Did edits according to feedback comments Sooraj gave
- Learned that success will be tested by using simulators and emulators that hardware have developed
- Two main points of testing: decoding into executable binary and decoding higher level into the ISA
- Should give more of an emphasis on GPU size minimizing and power usage minimizing; on top of resource maximizing
- Was still not the best polished work, but will work on finalizing better in the future


## Thursday (10/16/25) - Weekly SoCET Meeting
- Al Loper from AMD Corporate VP, Silicon Engineering at AMD
- Zen 5 Microarchitecture
- Wafers -> Certain Amount of Yield -> Processors
- When you know how to get it works, does it meet power and area specifications
- Cost becomes critical when designs work
- Organic Package Interconnects (anchor and chiplet)
- Advanced Packing Interconnects; power bumps underneath
- How do you route and get enough signal (EE)
- How to get proper interfaces and topologies to make sure things actually works? (CmpE)
- Compute per dollar is better with organic package
- Same concept can be used in GPUs (shader engines require massive amounts of connectivity)
- Multiple x86 computer, GPU tiles, chunks of HBM, ability to layer more cache on top
- A supercomputer in a single substrate (AMD CDNA 3 Next gen AI Accelerator Architecture)
- OpenAI demands a lot of GPUs; focus on less power consumption
- For AI usage AMD Instinct MI300 Accelerator; two flanks of HBM, Silicon Interposer, Carreir Si, IOD, XCD, Substrate (LGA Pads)
- If AMD Fabless, how do they do this? Strong connection with companies like TSMC
- Design Objectives are to increase performance and give variety of platforms of support