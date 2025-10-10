# Week 7 Design Log
## 10/2/25 - 10/9/25
I am not currently stuck or blocked

## Saturday (10/4/25) - Presentation Preparation
- Had 3 hour group call to go through slides and polish everything that is needed
- Chose amongst us to present slides (I volunteered for Packet Optimization, RFC, and Special Registers)
- Discussed the ambiguity of the CSR instructions (do we need it)?
- Who will take care of the initial set up and loading of instructions? 
    - CPU? Graphics? Compilers? Testbench?
    - What even is the Testbench and who is working on that?
    - Compilers should only be run the assignment of threads instruction (like from the CUDA Example)
    - Anything within <<< >>> should not be Compiler's Responsibility
- Ambiguity of Dependency Bit due to suggestion of "fence bit"
    - Will just mention unsureness of bit for now due to "every instruction essentially being dependent on something"
- Went through ISAs and made sure only had ones we needed
- Clarified ThreadID assignment across different warps
- Created examples and diagrams for some concepts/topics for easier comprehension

## Sunday (10/5/25) - Design Review Presentation
- Met up before meeting to quickly go through presentation and to make sure everyone was ready
- Presented Designs with teammates, and it went "okay"
    - For some reason, one of the slides got deleted; probably lost points with this :(
    - Seemed pretty shorter than I thought it'd take
- Was asked to clarify packet optimization policies
    - Was suggested a different way, but we want to stick to the procedure mentioned by hardware
- Listened to graphics, frontend hardware and backend hardware presentations
    - Learned a better concept of what graphics actually do with points, triangles, and camera view
    - Learned that frontend consists of the warp scheduler, instruction fetch, register file (+rfc) and decode
        - Realized had great dependency on us on assigning packets, predication, and rfc)
        - Learned Warp Scheduler would actually be running with two warps simultaneously
    - Learned that backend consists of the ldst and execution units

## Monday (10/6/25) - Weekly Meeting with Sooraj
Notes
- Add introduction and summary
- For packet dependency
- Just packet start bit and packet end bit

- Special Syntaxing Need; ThreadID Operations; Sin/Cos; sizeof()
- No need to import; sizeof(), sin(), cos() should be part of it

- No more inverting bit so pred file now 32 entries
- Just have two branch operations of opposite ones (bge blt)
- Maybe if needed to add instruction where we read pred reg and store it to stack

- Work seems doable for the semester
- Now that ISA is about done, can focus on working with PPCI and start creating the compiler

Tasks
- Create a green card of our ISA
- Put together a proper testing plan of testing our ISA
- Make one for a gentle matrix multiply
- Have unit tests for the different part of the compiler
- For now, don’t worry about packet bits, just make sure it works through
- Inform Hardware about ISA coming out and packet bit decision


## Thursday (10/9/25) - Weekly SoCET Meeting
- AMD my beloved is visiting the class (please take me back __ //\\\ __ )
- Andy Robinson from AMD; SRAM Design Team (John Wuu presentation)
- SRAM refreshes itself; Non-Volatile means no need to refresh
- Area is money, smaller transistor better to fit more data
- Can't be too strong signal; must be stable bit cell as well
- SPICE lied by omission; only answers what you ask for
- Look for process/power supply/timing delay situations
- Cells organized into Row Decoder and Wordline Driver; how dense can you make the design (square most optimal)
- Soft Error Rate (SER); may cause multiple bits to flip around it
- Sensing Unit to check errors is fast and no need to bias, but less reliable and timing is important
- Ensure test logic that you're adding in isn't too much that the clock would be affected
- Being able to mux around defects can save your chip
- How to verify when so much sensitivity; if done enough designs will see failures and will learn from experience
- Find out how failure is caused to prevent in the future
- How do you get the best yield without changing things
- Anna graduaed for May, worked in Product Development (EPIC Server testing)
- Scott (1999) Product Management; started in Product Dev; for Client business
- Tiffany McKay, started as recruiter, now manager
- Could SRAM Design change drastically in future? Fundamentally, basic design process is hard to replace
- Will depend on sensitivity of technologies; any levers pullable, while mitigating risks