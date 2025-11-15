# Week 12 Design Log
## 11/07/25 - 11/13/25
I am not currently stuck or blocked

## Saturday (11/08/25) - Implementing PJMP in IR
- Figuring Out What to Change
    - Did all edits and testing in the preprocessor branch
    - Looked through files and folders to see where the IR-Generator was
    - It was found in the ppci/lang/c/codegenerator.py
        - Functions for each type of code structure (for, if-else, expressions, etc.)
        - Each function generated appropiate blocks (condition, body, end)
    - Tested the current IR and Assembly outputs for for, while, and do-while loops
    - Created copies of the outputs and altered them for the desired output synax
    - Looked through gen_while function to see what each part did (utilized Gemini to understand what's going on)
        - Overall multiple recursional function calls, but will eventually lead to self.gen_condition() call
        - Altered inputs to gen_condition function so that function will jump to next block regardless
        - Now at the end instead of jumping back to condition block regardless, will need a jpnz instruction
    - Decided to create a custom gen_pcondition function instead to check predicate
            codegenerator.py
                def gen_condition(self, condition, yes_block, no_block):
                def gen_pcondition(self, condition, yes_block, no_block):
- Creating gen_pcondition and PJMP
    - There was a bit of confusion on how jpnz would work but clarified with Pranav
        - In a while loop, will check conditions with branch instr at the start and write to predicate
        - Predicate would be updated each iteration
        - On the iteration where the branch instr writes all 0s to mask, whill go through all instrs with nops then jump to next block
    - Attempting to create IR output of 
        - pjmp p5 == 0 ? main_block4 : main_block2;
        - Will check predicate mask at predicate address 5
        - If mask all 0s, will move forward to main_block4; else will jump to main_block2 to recalculate
    - Such change brought up a lot of errors betweeen ppci/ir.py and codegenerator.py
    - Utilized errors to find out which files needed changing and to what
    - Utilized Gemini to understand errors and what other files or functions were doing
    - Spent most of the time just running through these errors and trying to figure out what to do
- Successfully created gen_pcondition and PJMP
    - Decided to start again and just use the original CJMP that existed in ir.py and was utilzied in codegenerator.py through gen_condition()
    - Made a copy of both and just changed the name so it has the same functionality throughout and just outputed a "p" to show this was from the new functions
    - From here went through changing up gen_condition() and PJMP to make sure they outputed the correct IR output
    - Tested them on for, while, and do-while loops to make sure they worked on all outputs; also tested nested versions
- Attempt in implementing it into codegen
    - Tried to run the -S command to generate the assembly from IR
    - Continued going through a bunch of errors and figuring out which files and functions needed alteration
    - After spending hours on it, decided would be best to get help from Pranav who has worked with the codegen for the assembler before

## Sunday (11/09/25) - GPU Weekly Meeting
- Updating Team
    - Showed team my update of implementing jpnz instructions for while, for and do-while loops, and how it generated IR correctly
    - Justin showed his stack implementation of the predicates and how it is able to be assigned and diverged for if-else statements
    - Jack created an overall main file for the compiler that allowed us to run the command "twig -f file.c" where -f is the flag and file.c is our test file
    - Pranav has updated the assembler and made sure that the graphics functions can be accessed and compiled correctly as well
- Putting it all together
    - Justin and I combined the changes we made in his repository branch "predication"
    - Jack's changes were already combined with Pranav's already created assembler
    - Created a new branch called "merge" to combine our predication, jpnz, assembler, and main file
    - Talked about current predication system; whether we want to keep current stack implementation or have predicate register allocation similar to regular register allocation
    - Decided due to time crunch, would stick to stack for now because we have it implemented already
    - Limit is current predication register stack won't know what to do when more than 32 nested loops are utilized
- test_merge Branch
    - Created a new branch to test new changes we would add to it
    - Determined that if/else statements would need their own control of predication
    - I quickly updated gen_if in codegenerator.py to make sure it worked the way it should throughout
        - Would check condition and jump to if block regardless, at the end of if block would automatically jump to else block
        - Created new function gen_bcondition for these specific changes to have a separte IR syntax than usual conditional jumps
        - Will need to creat BJMP in IR too and later implement in codegen
    - Worked on implementing predicate address values replaced the block labels when generating IR, and adding it onto tree for codegen
- Remaining Tasks
    - We have to make sure all jpnz and predicate divergence related protocols are accounted for in codegen to create the correct assembly when running with -S
    - This will involve generating patterns in instructions.py according to Pranav; this will be something I need to take time to look into
    - Remaining task is also making sure each instruction has the predicate addr of the block it's in to be mapped in its binary when assembling
        - Ideas for this are:
        - 1) Hardcoding each expression in IR to have a predicate addr slot that will be passed onto instructions.py
        - 2) Having a parent block parameter in each instruction and making a hexmap for each predicate addr to each block
    - May not have time to work on packetization this semester
    - Will still require a lot of testing for deep nests and complex codes
    - Still need to figure out predicate address overflow when over 32

## Monday (11/10/25) - Weekly Meeting with Sooraj
- Updating Sooraj on Progress
    - Talked about merging all our work into one branch
    - Current state and limitations of our predicate stack implementation
    - Tasks we have left to do are implementing PJMP and SJMP in codegen; implementing predicates in each instruction; testing
    - It seems Pranav already implemented BJMP successfully
    - Have to get rid of full dependency on CJMP (based on old C Compiler)
- Brought up how SJMP might be needed for if-else code; so only one condition is checked and jumped to directly
    - Must differ from current PJMP which check the condition and its inverse to create two predicates
- Need to decide how we want to implement the predicates per instruction for the assembler
- The only CSRs we need to manage are threadID, blockID, blockDim, cur_dim: x, y, z

## Thursday (11/13/25) - Grinding out PJMP and SJMP
- Spent many hours diagnosing errors and checking out different files and functions of the PPCI repository
- Utilized Gemini AI to explain functions and errors and what files paths I might have to enter
- Kept SJMP as BJMP for now to avoid those errors for now; will deal with after implementing PJMP
- Came up with the following path of compilation for PJMP
    - IR Generation
        - /ppci/lang/c/codegenerator.py def gen_pcondition()
        - /ppci/ir.py/ class PJump
    - Codegen
        - /ppci/codegen/irdag.py def do_p_jump()
        - /ppci/codegen/instructionselector.py
        - /ppci/arch/twig/tokens.py
        - /ppci/arch/twig/instructions.py def make_pb() 
        - Jpnz = make_pb("jpnz", 0b1100000)
        - def pattern_pjmp(context, tree)
    - Codegen basically makes a Directed Acyclic Graph (DAG) with blocks based on going through the IR
    - Tokens utilize keywords like "PJMP" and "BJMP" to associate corresponding assembly code
    - Instructions recognizes patterns based on tokens and gets a specific node from the DAG to get needed data from
    - Appropiate assembly syntax is then determined in in instructions.py 
    - Realized PJMP couldn't get final_block for while loops because that block hasn't been created upon running gen_pcondition
    - Have to manually add to irdag map of blocks if it didn't exist yet (may bring up errors later so must be careful)
    - Type definition issues
        - There were many issues with the type of data being passed through each file
        - This took going back and forth between these files and casting it the right way or sending it through different parameters
        - I utilized the working BJMP code and the initially implemented CJMP as reference to see how I should be formating mines for PJMP
        - Got PJMP working through --ir and -S callings of C code
    - Implementing SJMP was much simpler because it was essentially a copy of BJMP just having one branch instruction instead of two
    - Attempted Cleaning up Unused Parameters
        - Went backwards in stages deleting parameters and commented out code to clear what is not needed
        - This required a bit of back and forth between files just to make sure they all had consistent names and functioning types
        - Managed to clean up a good amount and ensure predicates were being passed in as values rather than labels
    - PJMP, SJMP, and BJMP are now fully working in IR generation and CodeGen
    - The only thing left is to make sure jpnz instructions and predicate address values are translated correctly when binary hex

## Thursday (11/13/25) - Weekly SoCET Meeting
- Michael Mills presenting about Qnity Electronics
- Package ends up comprimising what you've made
- Used to have vertical layering with aluminum, now copper; used to be 3 levels interconnect, now 26 levels
- He spent most time on materials side, metals side; went and talked to senior fellows "worked with optical fibers in thesis" so could maybe help out; and went through within two days (don't be hesitant to say "I've done something like that!"); moved from one group to another
- You're going to have to sell your ideas to move forward with your; take a business class to communicate your ideas (your career depends on if business people will want to invest in you)
- Semiconductor Industry requires a diversity of technical background
    - Engr (cmp, elec, mech, chem, nucl); Sci (cmp, materials, data, polymer); Traditional (chem, phys, bio)
-  Core Products: Copper Barrier, ILD, Tungsten, Advanced Packaging
- When doing design and testing; what's the simplest way to get the chip through
- Qnity is for repetitive nature of making a chip (MANY STEPS TO MAKE CHIP)
- Prepare wafer, doping, build layers, slection, etching; packaging; circuit boards; displays
- Failures in your design will definitely teach you more than your successes; correct, diagnose, and fix
- Advanced Computing Tech (high-performance computing; AI/ML; industrial automation)
- Advanced Connectivity (advanced interconnects; advanced packaging; advanced deriver assistance systems)
- Car is still one module; but imagine orderrs of magnitudes of interconnects to it; customization stage
- A lot of Thermal Management now; over-clocking and will cause overheating astronomically
- 50% of energy that goes into the system leaves as heat

- Validation EDA Tools hasn't been made because structure hasn't been perfected
