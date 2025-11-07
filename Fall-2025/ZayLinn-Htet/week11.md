# Week 11 Design Log
## 10/31/25 - 11/06/25
I am not currently stuck or blocked

## Saturday (11/01/25) - codegeneration alteration
- Finding codegeneration.py
    - Continued digging through PPCI libraries like last week to end up in codegeneration file
    - This took the Abstract Syntax Tree generated, ran through it, and outputs a generated intermediate representation
    - Ideal place to make changes on how loops would work

- Codes of Interest
    - ppci\lang\c\codegenerator.py
    - def gen_if(self, stmt: statements.If)
    - def gen_while(self, stmt: statements.While)
    - def gen_do_while(self, stmt: statements.DoWhile)
    - def gen_for(self, stmt: statements.For)

- Updating codegeneration.py
    - Main goal was to look through gen_X functions in the codegeneration file and update them
        - Update gen_while, gen_for, and gen_dowhile
        - These will be updated to jump back and check conditions rather than doing a check and branch
        - Will have to check with graphics team on whether the following gen_X may also need to be altered
        - Switch; Case; Range; GoTo; Continue; Break; InLine Assembly
        - Could also potentially reuse "GoTo" as a way to jump instead of what they already have
        - Main issue is need to change up the order and usage of "condition" blocks
    - Generated new versions of the gen_while, gen_for, and gen_dowhile functions with the help of AI
    - Implemented them with "changes indicator messages" but did not seem to be running
    - Didn't run when utilizing the --IR flag, but did run when utilizing the -c flag; will need to look more into this

- Preparing for tomorrow's meeting
    - Thought about all the things that still need to be completed for the compiler before the end of the semester
    - 1) Adding New Functions (GPU Related Terms)
        - For utilizing instr from new ISA, and anything GPU related that C usually wouldn't have
        - Most likely change in Preprocessing
    - 2) Fixing Loops to be Jumps instead of Branches
        - Basically what I was trying to do right now
    - 3) Implementing Predicates with Created Blocks from IR
        - IR seems to already have blocks created for each divergence and convergence of instructions so it can be used as an indicator of predicates to be added
        - Will need a way to create a software stack for these predicates
    - 4) Code Gen from IR with Teal Card ISA
        - Assembler is already created; but not sure if it goes from IR straight to executable binary yet (need to check with Pranav)
    - Should catch up with teammates' progress and see what is done, wahat still needs to be done, and who needs to do what

## Sunday (11/02/25) - GPU Weekly Meeting
- codegeneration update
    - Recapped team on my progress on codegeneration alteration
    - It seems that I was executing it based on the online ppci library instead of my local files
    - Spent some time actually installing the library based on local files
    - Helped teammates set up the executable on teammate's laptop as well
    - Jack was able to start running and help me make changes to codegeneration

- Progress on assembler
    - Assembler already seems to compile from our ISA as well
    - For it to compile from the IR, it should be able to do so because the architecture file has already been created and implemented
    - There were some bugs that graphics and hardware brought up during the meeting, but it was mainly due to the way they wrote their code
    - Some issues kept popping up but Pranav dealt with them as he knew how it worked the best

- Notice about special GPU functions
    - Pranav was actually already working on it, so he will continue to do it; he says it's not difficult to add new ones
    - Main issue now is bringing these used functions down into the AST and IR to ensure they compile into the correct machine opcode

- Implementing Predicates
    - This was the most crucial aspect of the entire compiler so it should be our main focus
    - Decided Justin, Jack, and I will work on this together to ensure it works fully correctly
    - May be difficult because we will have to track convergence and divergence points
    - Will need to track which predicates are still in use and which ones are no longer in use to reuse them
    - Will be going through codegeneration as well to try and implement these changes
    - Main thing is to have an additional parameter in each block to use as a predicate
    - Jack brought up that there were some empty parameters that the devs left while working on it that we can reutilize
    - I can help out too because I am working on loops/jumps that would be the key of divergence and convergence points

- Important Dates
    - (Sunday) 16th November, Code Review; in-place of Design Review
    - (Tuesday) 18th November, Fall Expo Presentation
    - (Before Thanksgiving Break), Draft of Final Report Due (if you want to get it checked)
    - (Thursday) 19th November, Senior Design Presentation, in-front of SoCET (15 mins presentation + 5 min questions)
    - (Friday) 19th December, Final Report Due Date

- (UPDATED) TASKS TO DO
    - 1) Adding New Functions (GPU Related Terms) [Pranav]
    - Preprocessing (g key term)
    - AST (new compound type)
    - IR (new function type) [Ex. def gen_sine]
    - Code Gen (Utilizing instr from ISA Teal Card)

    - 2) Fixing Loops to be Jumps instead of Branches [Zay]
    - IR (alter gen_for, gen_while, and gen_dowhile)

    - 3) Implementing Predicates with Blocks from IR [Justin] [Zay] [Jack]
    - AST or IR (add parameter for predication or whatever works)
    - Stack for Predication

    - 4) Code Gen from IR with Teal Card ISA (IR->Binary) [Pranav]
    - Code Gen or Assembler


## Monday (11/03/25) - Weekly Meeting with Sooraj
- Justin's Progress
    - He already implemented predicates as a parameter in codegeneration and was able to assign predicate values to it
    - Managed to also create a predicate stack that would hold these predicate values
    - He seems to have a good amount of it figured out; it would only be left to keep track of which ones can be reused when it's usage is done
- Sooraj's Interrogation
    - Talked about what we're currently working on and what is left to do
    - Rediscussed how stacks would be implemented as according to how we discussed it with graphics
    - Brought up how packets were something we haven't touched at at all
    - Because packets are more of an optimization thing, it can be a lower priority
    - Predicates implementation should be our main priority in this case
    - We should try and get the tasks mentioned above done hopefully be next week
    - Will use the week after to wrap up anything else that pops up in preparation for the code design review

## Thursday (11/06/25) - Weekly SoCET Meeting
- Multicore because singlecore couldn't be any faster
- Based on previous multicore work (homogenous cores)
- Homoegenous means cores same architecture; heterogenoush cores mean different architectures
- Homogenous multicore support in the AFTx08 top level
- Had software tests to confirm functionality
- Tested on 1,2,4,8 cores; mergesort, matrix multiplication and vector adding
- Heterogeneous multicores supported; build framework goes from a YAML File to a Python Script that creates PKG File, Header File(.vh) and .h File which all goes to make RISCV Files
- Power and Area Analysis still needs to be completed (CLK Gating to estimate potential power savings)
- Compute Task by I2C data periodically and sleeps between samples; while big core performas multiple matrix multiplications
- Each testcases for different types of scenarios; lack of parallelism; vector bound aspect; memory bound aspect