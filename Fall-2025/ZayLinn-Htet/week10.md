# Week 10 Design Log
## 10/24/25 - 10/30/25
I am not currently stuck or blocked

## Saturday (10/25/25) - PPCI Deep Dive
- Reviewed the main stages of a compiler
    - Preprocessing; Abstract Syntax Tree Generation; Intermediate Representation Generation; Optimizing; Linking; Assembling
    - Currently Assembling (from assembly into binary files) have been completed by Pranav
    - Main focus should be Preprocessing (interpretting special C functions from GPU Team, like sin/cos/invsqrt, and any GPU functions)
    - Register File Cache assignment should be within Optimization
    - Packet Start and End Bits could be determined within AST or IR as an additional parameter
    - Predication could also be determined in AST or IR
    - ppci has 1) cparser [frontend]; 2) ccodegen [middle-end]; 3) optimize [optimizer]; 4) codegen [backend]

- Setting up PPCI
    - Had to set up again on new laptop because old laptop broke
    - Set up virtual environment (sandbox) to run ppci

- Outputs of PPCI Analysis
    - Utilized example files given and analyzed running command and flags
    - Utilized "arch" as RISCV and used ppci-cc (C Compiler)
    - Basic execution generated object files that will be used by linker
    - Sections (held data and code);  Relocations (for Linker usage); Symbols (blocks)
    - There were three types of blocks per function: function itself, function block, and epilog
        - Function itself was whatever ran in the function
        - Function block includes registers and address saving when jumping PCs
        - Epilog restores registers and addresses before returning
    - This shows that minimal function calls would be optimal
    - The Setup
        1) Allocate Stack Space for entire frame
        2) Save Caller's Return Address (ra)
        3) Save Caller's Frame Pointer (fp)
        4) Establish New Frame Point (fp)
        5) Save Callee-Saved Registers (sX)
    - The Work
        1) Access Arguments aX and more on stack
        2) Use temp registers for calculation
        3) Store return value to a0
    - The Cleanup
        1) Restore Callee-Saved Register (sX)
        2) Restore Caller's Return Address (ra)
        3) Restore Caller's Frame Pointer (fp)
        4) Deallocate Stack Frame
        5) Return to Caller
- PPCI Execution Flags
    - Then I looked into the execution files itself and the flags that it used
    - There seemed to be a large multitude of flags available for different sorts of analysis
        - --ast // outputs abstract syntax tree
        - --ir // generates ir-code
        - --pycode // generates python code
        - -O // optimzations
- PPCI Execution Files
    - https://github.com/Purdue-SoCET/gpu-ppci-compiler/blob/preprocessing/ppci/cli/cc.py
        - C Parser File called by ppci-cc
    - https://github.com/Purdue-SoCET/gpu-ppci-compiler/blob/preprocessing/ppci/api.py
        - api.c_to_ir; loops through all source files and creates IR
    - In api.py
        - def cc() // C compiler; single source file into object file
        - args: source file; march (architecture); coptions (options for C frontend); debug (debug info)
        - returns: object file
    - https://github.com/Purdue-SoCET/gpu-ppci-compiler/blob/preprocessing/ppci/lang/c/api.py
        - def c_to_ir // C to IR translation
        - args: source file; march (architecture); coptions (options for C frontend)
        - returns: "ppci.ir.Module" (the ir_module)
    - There are A LOT of files and functions to dive through so it will be a matter to continue later
    - Should find out in meeting which files/functions to prioritize to only look at what is needed

## Sunday (10/26/25) - GPU Weekly Meeting
- Unit Tests with Hardware
    - Dicussed with Dan on small unit_tests they could use for their hardware emulator
    - Requested tests to fill pipeline with store_words for different data sizes (bytes/half-words/words)
    - Requested tests for simple arithmetic functions
    - Manually wrote out instruction binaries to ensure they are similar to what assembler produces and what is on Teal Card
    - Was small mistake in immediate due to it being signed so switched addi into lli for more immediate space

- Assembler Recap
    - Discussed with Pranav on how the Assembler worked
    - Edited changes to opcodes in Assembler for new instructions added to Teal Card
    - Assembler is just simple python file, no need other stuff in library except the ISA

- Questions with Graphics for Stack
    - Approached us to discuss existence of stack pointer
    - They explained how the overall memory would be divided into sections for each thread of each warp
    - Essentially everytime stack point allocated, would be for all 32 threads
    - There are 32 warps of 32 threads so there should be 1024 threads
    - Graphics will tell how big each stack limit should be

- REGISTER FILE CACHE HAS BEEN SCRAPPED; ONE LESS WORRY TO HAVE

- IR Diagnosing
    - Decided to figure out how IR works to see if the blocks it gives can be used to determine predications
    - Ran Sample_4 of PPCI's C Compiler to break down
    - Drew out the blocks and flowchart of the IR of Sample_4
    - There were a lot of "empty" blocks when going through if/else statements or for/while loops
    - Found out big issue that their for/while loops ran on branch instructions to repeat
    - Ours utilizes jump instructions, meaning the IR is something we will have to go into and alter to utilize predication
    - Need to figure out with a simpler C file to figure out how blocks are generated
    - Need to also just look into the files of the IR Generator
    - May also need to look into the AST Generator code to see how that might influence the IR


## Monday (10/27/25) - Weekly Meeting with Sooraj
- Gave Quick Recap on how IR needs to be looked into and altered for the issue of our unique while/for loops
- Brought up how assembler is essentially "complete"
- Mentioned how preprocessor also needs to be looked into for the custom C functions we create
- May ask graphics to utilize  special "g." for any custom C functions they may use
- Concern on linker was brought up and will be something we will need to keep out eyes open for
- Should try and get IR sorted out within the next two weeks

## Thursday (10/30/25) - Weekly SoCET Meeting
- Iron Wood Architecture
- Data and Communication Flow between Host & Management Plane; Latest Gen HBM, High Performance Vector/Matrix Compute; Sparse Compue Engines; and Fast, Scale-Up Interconnect
- TPUs can connect to 6 other TPUs (3-dimensionally), making up a TPU Pod
- TPU Pod Sizes for either Inference and Small Training or Large Scale Training
- Can rent out TPU sections to do specific tasks (based on different user needs)
- 2D Torus (Smaller Tasks) or 3D Torus (Larger Tasks)
- TPUs are essentially nodes in a neural network; with their own hierarchy of communications
- ICI (Inter Chip Interconnect)
- RDMA (Remote Direct Memory Access); every TPU can look into any part of Memory via ICI
- ICI: ICR Router (routes where things go; congestion/traffic), Link Stack(parallel transfer lanes); SerDes Layer (high speed data stream between layers and racks)
- Optical Circuit Switch (OCS): programmable hardware that uses micro-mirrors to redirect optical fibers (physical solution)
- ICI (low-latency local mesh) + OCS (high-bandwidth optical backbone)
- Together enable data center-scale training and inference for triliion-parameter workloads
- Unified AI Architecture: runs both training and inference
- NVIDIA uses NVLink + NVSwitch: general-purpose for diverse workloads; GPU-GPU communication
- GPUs are more power hungry than TPUs
- Compute Power based on magnitudes of chip combinations