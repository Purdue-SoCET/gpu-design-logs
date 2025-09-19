State: I am not stuck with anything, don't need help right now. 

# Progress:

## 3: The SIMT Core: Instruction and Register Data Flow
* GPUs require high off-chip memory bandwith, as they are often dealing with to much data to store on file
  * Can deal with this in part through on-chip caches to reduce memory access
* The basic pipeline can be divided into two parts, the SIMD front-end, and the SIMD datapath
* The pipeline can be divided into three distinct loops, an instruction fetch loop, an instruction issue loop, and a register access scheduling loop
  * The instruction fetch loop uses:  Fetch, I-Cache, Decode, and I-Buffer
  * The instruction issue loop uses: I-Buffer, Scoreboard, Issue, and SIMT Stack
  * The register access scheduling loop uses: Operand Collector, ALU, and Memory

### 3.1 - ONE-LOOP APPROXIMATION
* Threads are organized into warps/wavefronts, and is the unit of scheduling
* In every cycle, the hardware selects a single warp to run, and the warps program counter is used to fetch the instruction
* The instruction is decoded, and source registers are fetched alongside the determination of the SIMT-mask
* The single instruction is ran on multiple pieces of data, using a lane of hardware for each thread whose SIMT-mask bit was set
  * This will happen on a chosen function unit for the given instruction. Each Function Unit contains the number of lanes needed (32 or 64)

#### 3.1.1 - SIMT EXECUTION MASKING
* Uses a SIMT stack to allow thread divergence
* Handles control flow as well as skipping control flow where no threads execute
* modern GPUs use special intructions to handle the SIMT stack, however this will be ignored for this aprox.
* Upon every divergence, two SIMT masks are put on the stack to handle control flow
  * contain which threads to run, the PC of reconvergence, as well as the next PC to run for that mask
* To minimize stack depth, masks with the least threads are put onto the stack last, in hope of quicker reconvergence

#### 3.1.2 - SIMT DEADLOCK AND STACKLESS SIMT ARCHITECTURES
* Stack based SIMT-masks can result in SIMT deadlock
  * This occurs when one thread is waiting on a lock to be cleared to continued, while the thread meant to clear that lock is stopped, waiting for the other thread to reconverge
* To fix this, using warp barriers is a simple hardware solution
  * A Barrier Participation Mask is used to track which threads in a warp participate in a given convergence barrier
  * Also tracks if a thread is blocked, ready to execute, or yielded
  * This yielded state is used to allow warps in a thread to continue passed reconvergence and fix SIMT deadlock
* A special add instruction is used to initialize a warp barrier
* A special wait instruction is used to stop threads once they reach a convergence barrier, with threads on continuing once all threads in a given mask have ran the WAIT

#### 3.1.3 WARP SCHEDULING
* In theory, an idle GPU interleave the threads of multiple warps for maximized hardware efficiency
* Could schedule using round robin, would reduce hardware for scheduling, but adds significant register hardware for each warp
* If multiple threads access localized data, round robin is idle, maximing cache hits
* If data is not localized, giving a certain warp more time is idle to maximize cache hits

### 3.2 TWO-LOOP APPROXIMATION
* One loop scheduling prevent beging to run the next instruction while the current one executes, as it has no system to determine if a given instruction has a dependency on a previous one
* An instruction buffer is used alongside a scheduler to determine which instructions to run
* Instruction memory is implemented as first level cache with multiple unified second level caches
* Two tradition approaches to determining dependincies, scoreboards and reservation stations
* Scoreboards - simple
  * In a single threaded CPU, a single bit for each register tracking if any instruction use that register, delaying any instructions that use already marked registers
  * With a GPU, the many warps and number of threads means that there a a much larger number of registers. And with many warps, many more read ports are needed
* Alternative Scoreboards:
  * Each warp has its own 3-4 entries, indetifying a register to be modified bu an issued instruction
  * When a new instruction is placed on the buffer, it is checked against the scoreboard entries, with a bit vector marking its dependencies
  * An instruction will only be ran once the bit vector is cleared. When it is done, it will clear its relavent entries in the scoreboard

### 3.3 THREE-LOOP APPROXIMATION
* A large register file is need to handle the switching of the many warps ran on each card
* Seperate physical register files are made for each warp executing
* Creates a port problem, as a naive register file would have one port per operand per instruction per cycle
* Through an operand collector, used to read from single ported memory, this is simplified.
