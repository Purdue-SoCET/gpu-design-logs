# Week 13 Design Log
## 11/14/25 - 11/20/25
I am not currently stuck or blocked

## Saturday (11/15/25) - Preparing for EXPO Poster, Code Review, and Final Presentation
- Met up with team to discuss the components of all three final presentations
- Reviewed through the rubric and what was needed
- EXPO Poster
    - Decided to focus on the Problem Statement, ISA, PPCI, and stages of Compiling
    - Would focus more on Predication for this Presentation because Packetization isn't that thoroughly developed yet
    - Utilized Sooraj's suggestion for abstract for the Problem Statement
    - Main issue of focus for this GPU's Development is to deal with Divergence (with Predication) and Scoreboard Dependency (with Packetization)
    - Assigned roles upon each other to work on components
    - Made diagrams and clean tables for the presentation

- Code Review
    - Moved onto deciding how the Code Review would go and what aspects we'd focus on
    - We recapped on what everyone worked on during the semester
        - I worked on implementing CJMP and PJMP in the IR Generator and the CodeGen
        - Justin worked on implementing the Predication Stack
        - Pranav worked on the Preprocessor front and the Assembler
        - Jack worked on the wrapper file that utilizes the Flag and the Preprocessor
    - To prepare, made sample output files for the main things my PJMP and CJMP were for: loops and conditions
        - Made the examples for the original C input, AST output, IR output, and Assembly Output
    - Opened up all files I edited to make the changes in the order of stages in the compiler

- Final Presentation
    - Decided to make it the same format and content as the EXPO Poster
    - Decided to include "Packetization" in our "Next Steps" section
    - Assigned slides for everyone to work on as well

## Sunday (11/16/25) - GPU Weekly Meeting (Code Review)
- Listened to and took note of graphics code review presentation
- Took notes on what might be relevant and the parts they depend on for the compiler
- Gave our code review presentation
    - Had some remarks about our PJMP having two inverted branch operations
    - Highlighted what a "branch instruction" meant being able to write to the predicate register
    - Was able to demonstrate the loops and conditionals code and ran through the files I altered well
    - Realized during presentation that codegenerator.py still utilized the old gen_conditional and that needs to be fixed
- Listened to the multiple hardware teams' presentation on their emulators
    - Found it really interesting of their approach to replicate SystemVerilog (hardware) functionality through Python
    - There were a lot of different components though that it left me a bit confused on the difference between the "emulator" and "simulator"
- Meeting ended just in trying to finish presentations; talked with teammates at the end about printing the poster
- Jack and I managed to fix and finalize the poster after our feedback and print it at WALC
- Discussed meetup times for Tuesday to make sure things work out

## Monday (11/17/25) - Weekly Meeting with Sooraj
- Talked to Sooraj about upcoming Senior Design Review presentation and what was needed
- Was suggested to emphasize Packetization more at the end of our presentation of next steps
- Also should add a timeline of next steps on that same part of the slide
- Asked for feedback about the Code Review and was told we did okay
- Was asked about projected progress to the end of the semester
    - We should be able to finish predication implementation before the semester ends
    - Might have to fully leave packetization to the next semester
    - Should try and attempt to complete final report before Thanksgiving break to see if we can get feedback on it

## Tuesday (11/18/25) - EXPO Presentation
- EXPO Presentation went smoothly as we only had to be there for an hour
- Poster was able to be set up well as long as a Twig Teal Card sheet
- Had someone from the Mechanical Engineering department come and we explained to them on a surface level
    - Most interesting thing was how we had to bring it down to a fundamental level
    - We broke it down into what "instructions" mean and what it constitutes of
    - The Twig Card was useful for this
    - We made analogies for describing how we interacted between the Graphics Team and Hardware Team
    - We utilized a translator between three different languages
- A professional judge came by and we gave our presentation again
    - We had warmup with the previous person so it went better this time
    - We were definitely more organized in explaining the purpose and goals of our compiler and how we went about doing it
- Jing actually came by and we gave a thorough presentation similar to how we would for our final presentation
- Other than that, not much went on, so we left as soon as our time was up

## Wednesday (11/19/25) - Senior Design Final Presentation
- Final presentations had some issues loading up due to being sent later
- Overall presentation I believe went smoothly, had a small mess up within the Preprocessor slides
- Though I feel that we skimmed over most details to save time, and ended up finishing earlier than expected
- There was a bit of confusion on the predication but I think we were able to clarify it
- Questioning went okay except for the last one which I didn't understand that well
- Had something else right after so I couldn't stay later for the other presentations, will come back later for it

## Thursday (11/20/25) - Weekly SoCET Meeting
- AFTx08
- AHB Interconnect (Faster) and APB Interconnect (Slower)
- RISC-V Core; 3 stage pipeline; L1 cache; Branch Prediction; Parameterizable ISA; Privilege Levels (M S/U)
- Zalrsc; Z = "extension modification"; a = extension modified; lrsc = name of modification
- Z extension is a subset or add on of another ISA extension; don't support whole A Extension
- Privilege Levels: (M)achine, (S)upervisor, U(ser), H(ypervisor); Extension modifying with a "S" for privileged and "Z" for unprivileged
- Zalrsc = Load-Reserved/Store-Conditional Atomics
- C(ompressed) Extenssion Redo; different sized instruction fetches (32b/16b)
- Branch Instruction; BTB; static/1b/2b, gshare
- Multicore with MESI; Could make i-cache incoherent; LR/SC; AMO; Self-Modifying Code with fence.i instruction
- Performance between AFTx07++ and AFTx08; performance on branch predictions and dual core speedup
- Changes in Peripherals; Interrupt Controller (CLINT + PLIC)
- PLIC went from 54 deep to 5 deep
- Memory has big update (ROM preload, on-chip RAM main mem, off-chip SRAM)
- ROM was a case statement before with a bunch of muxes; ROM = Read-Only Memory; Crosspoint grid ROM now
- On-Chip RAM: TrueSRAM; smaller and less selection overhead
- Boot Process; Hardware I2C will do boot process; will start at botom of ROM to see where it should BootIn; Only Core 0 runs boot, Core 1 waits for interrupt
- Future of AFT: Virtual Memory; FP; AXI Bus; Extended Pipeline; RISC-V "P" Extension; L2 Cache; Universal Serial Interface (merge UART, I2C, SPI + SDIO, PSQI, OSPI, 1-Wire, etc)