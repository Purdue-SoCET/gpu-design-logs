I am not currently stuck or blocked

Week 4: 9/12/25 - 9/18/25 

Sunday (9/14/25): GPU Team weekly meeting
- Presented my presentation on Register File Virtualization with Jack and were asked thorough questions by the GTAs

- A summary was given about the current architecture of the GPU
- I could understand the flow through these hardware components, but not well enough to be able to it on my own
- After understanding that the software side essentially does look at all the hardware components from above, I decided I would join the software team
- Later got split into the Compilers team along with Pranav Bantval, Jia-he Zhou, and Justin Yasuumi
- After a short talk with Sooraj, we understood the weight of responsibility in our hands as a bridge between graphics and hardware
- We started and almost completed (completed later in the day) our poster slide for what our compiler team was going to be working on
- Our tasks mainly consisted of communicating with the other teams and finding their needs so we can develop our ISA and compiler simulations
- At the end of our GPU Team meeting, we met with someone in the AI Hardware team who was creating their own compiler using Pure Python Compiler Infrastructure (PPCI)
- This showed us that we would have to first look through the PPCI repository to see how the current set functions work, only after that can we implement our own
- We decided as a team through look through PPCI sometime during the week before next Sunday's meeting


Monday (9/15/25): Compilers Team & Sooraj Weekly Meet
- Met with Compilers Team and Sooraj to talk more in detail about our goals
- Understood importance of our role in connecting graphics and hardware
- Took notes about Sooraj's explanation locally on my laptop, but that laptop has stopped working for the past few days (notes below are based on memory)

- Instruction Set: {7bit op code, 6bit src1, 6bit src2, 6bit dest, 4bit mask, 3bit {pack on/off, ... , reg_file_cache}}
- Execution assembly lines divided into packages
- Packages denoted by 0 to start or end, and 1 to be within a packet
- Two consecutive 0s denote two independent packets; 0 1 1 1 0 denotes one packet
- Each packet is essentially a group of assembly executions that have no dependency to other packets
- Ensure to prevent WAR, WAW, and RAW hazards upon executions
- We have to make algorithms that determine which instrs can go into a packet, and how big the packets will be
- We can reorder the packets or the contents within the packets as appropiate and as necessary
- We will be implementing a register file cache that we need to discuss with the hardware team
- We will need to get the ISA done for the hardware team much earlier in the semester
- Currently have 2^7 = 128 instrs available, can decrease 64-bit reg to 32-bit reg if absolutely necessary for 2^8=256 instr instead
- Must await and see what instrs graphics will be using, they are current bottleneck
- Should attempt and familiarize with ppci in the mean time
- Practice implmenting or utilizing easy basic functions from C

- Presentation was moved onto Monday of next week
- Must revise presentation to have the details of today's meeting and what we learn from looking through ppci


Thursday (9/18/25): Learning PPCI
- Started looking through ppci's website and Github
- Viewed the Overview of the C Compiler page to familiarize myself with the syntax
- Learned that preprocessor digests includes into texts which along with the file's tokens and the include files tokens goes into a parsed program, that takes these tokens and translates them, then generates the code appropiately
- There are already a lot of C front end calls available  such as print_ast, parse_text, parse_type, etc...
- Started setting up the ppci library on my laptop, only to have to spend an hour reinstalling Python, reinstalling Git, and learning how to setup ppci with the help of AI tools
- Managed to setup a virtual environment on VSCode to run
- Browsed through the GitHub page of ppci to view the available compiling lanugagues
- Noticed there were demo folders so tried out the execution for riscv, only to find out there were some issues when setting up, so I have to start the whole reinstalling processes again

Thursday (9/18/25): SoCET Meeting
- Attended SoCET Meeting today and listened to talks from Issac Hagedorn for MRAM and a short speech from TI senior fellow Al Griffin
- Issac Hagedorn
- center for secure microelectronics and polymorphic ecosystem
- EMRAN Emetent Memory Risk Aversion and Monitoring Protocol
- Make presentations clean concise, have a purpose for message; take home message one liner/image; results experimentation, expectations, observations, reconciliation
- MRAM: magneto-resistive Random Access Memory (spintronics); parallel or anti parallel state; distinct resistances; different from SRAM; symmetry important
- Application space; low power IOT AI/ML Computer in Memory; Radiation Harsh envis
- Weaknesses to magnet itself; temperature, interaction with other devices or environments due to magnetic field
- MRAM Chip interfaces; checks environment and saves data if in danger
- Implemented utilizing a FPGA
- Monitor by giving heat treatments and testing reaction; success defined if MTJ maintains state regardless of temperature; no significant bit flopping
- Figure out what creates the symmetry; stall reading and see if it can reform model
- When heat present, can make asymmetry make going one state to another state
- summary of desires include gain, sensitization; success now defined as XOR between two reads; giving up some success; whether or not bit flips depends on us or the environment
- write time violation with chip enable signal; looking for change in gain distinct from what we seeing;
- Al Griffin 
- from TI; senior fellow; solve TIs biggest problems; Process Engineer at TI making chips; goes to different factories to solve problems;
- even if knew nothing about problem, just come in and learn it, even if never done it before
- Created red team; process engineer to problem solving team; job in memory is to make sure bits don’t flip; mole supplier swapped ingredients with radioactive that made bits flip
- even had psychologist cause so good at solving problems; try to always have some sort of materials class (if EE)
- 
Thursday (9/18/25): Reading Notes
- Chapter 5.1 Notes
- 5.1 Thread Scheduling
- Threads fuse to form warps
- Work assigned to GPU cores in bulk
- Schedulers decide which warp and what to do
- Scheudling decisions can take place in different kernels

- 5.1.1 assignment of threadblocks to cores
- dynamically throttling; hardware monitoring system checks if core idle
- equalizer; dynamically tunes GPU resources; checks for idle warps and assigns them
- CTA = Cooperative Thread Array

- 5.1.2. cycle by cycle scheduling decisions
- two-level scheduling; first assign fetch groups; warps within group go in round robin
- cache-conscious wavefront scheduling; detects lost locality; ensures minimal cache fetchings

- 5.1.3. scheduling multiple kernels
- running multiple kernels at once a challenge; kernels hard to interrupt
- propose context switching where dynamically chosen threadblock can save context, wait fror complete, stop and restart

- 5.1.4. fine-grain synchronization aware scheduling
- fine-grained synchronization: done in networks in a manner where stability is maintained
- standard SIMT can lead to deadlock; de-prioritizing warps can stall warps(or lock them)
- dynamically detect spin-loops with current path and executed history
- execute backwards branch of spin loop after thread has been held in lock
