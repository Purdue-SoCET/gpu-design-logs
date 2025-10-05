Statement: Some questions about our GPU and register hierarchy implementation (see below)

Questions:
Is it 2 instructions per 3 clks? 
I was told by frontend that wsel will come from ALU, what will that change?
Frontend told me about predicate registers/"branches", what will that change?

Overview: Extensive talks to compilers and hardware guys. Things discussed:
- Compilers will focus on implementing RFC first, without LRF or any other things yet.
- Little hardware control/decisions will be made, my job will basically be communicating simulation stuff and making the RFC as efficient as possible (I think?)
- Frontend is deciding on a 3-level scheduling: 32 -> 8 active -> 2 choosen -> 1 warp on SM.
  - Compilers is assuming 64 registers (see design review slides
  - This means that MRF must store 64 reg * 32 warps = 4096 registers?
- RFC will have 8 entries, oldest evicted by compiler (FIFO) to MRF. 
- RFC is directly (in compiler's eyes) placed in the lower 8 registers of MRF. Will this remove the power savings from having a smaller register file? (probably not, VLSI/chip will have them seperated)
- Bank conflicts will be assumed to happen **every time**. Thus, opperand collectors (OCs) are crucial for MRF/RFC.
- MRF will consist of 2 banks, each of which will store even/odd register numbers. (NOTE: this conflicts with Gebhart, but I'm assuming this is a result of 
  - Do compilers
- Prediction will go down each branch given a predicate register
    - This implies that each predicate register ("branch") must have its own register hierarchy.
      - Can there be multiple predicates per thread? 
    - Within the predicate registers, predicate conditions are "anded" (say, p1 & !p2 is a condition).
    - Thus, predicate registers are integral with the register hierarchy.
      - I'm assuming that predicate "condition/branch" and thread ids are given to the register hierarchy. In other words, the predication/scheduling logic is all invisible to the register hierarchy.
     
Frontend/Architecture Decision that DIRECTLY COMPLETELY changes the Register File Hierarchy
I was made aware by the Saturday meeting why everything changed. I had some idea on Thursday, but I think I understand the changes now:
- MRF is 2 banks, split into even and odd warp ids. Why?
- Bank conflicts are assumed to be guaranteed. Why?
- Access coalescor is implicit within scheduling/frondend stuff. Why?
It comes down to this: instructions/warps are multiplexed, operands collected in parallel:
ld B0, B0
ld B1, B1

By parallelizing two instructions to read the register hierarchy in 2 clk cycles, you effectively get 1 IPC (its really 2 instr per 3 clks).
By guaranteeing bank conflicts from splitting warp id's into even and odd (and into their respective banks), even and odd warp id's are alternated within the SM after decode.

Ibuffer
- Will have 16 ibuffers per warp, each storing the values of an "even-odd" pair.

Opperand Collector 
- Won't be able to tell if data came from MRF or RFC. 

See presentation for more detail:
https://docs.google.com/presentation/d/1Is6HNChVRcIMx3nnyw-dslQUPmFsOYvEmtePV2tYh2k/edit?slide=id.g38919b77428_0_0#slide=id.g38919b77428_0_0
