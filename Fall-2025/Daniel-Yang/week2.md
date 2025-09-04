Week 2 (Chapter 3 Notes)

Status:

Progress: reading chapter 3 of textbook

Chapter 3: SIMT Core: Instruction/Register Data Flow

This chapter is all about examining the architecture/microarchitecture
of the GPU. In traditional graphics, GPU data sets are too big to be
contained in on-chip caches, but caches can still help significantly
with spatial locality between (ex) adjacent pixel operations.

![A diagram of a computer hardware system AI-generated content may be
incorrect.](media/image4.png){width="5.2363801399825025in"
height="1.6945319335083115in"}

Instruction fetch includes the Fetch, I-Cache, Decode, I-Buffer.
Instruction issue includes the I-Buffer, Scoreboard, Issue, SIMT-Stack.
Register access includes the Operand Collector, ALUs and Memory.

**3.1 One-Loop Approximation**

-   For a single warp:

    -   Warp selected for schedule by hardware -\> instruction decoded &
        operand registers fetched from register file & SIMT execution
        mask values determined -\> execution proceeds in SIMD manner and
        each thread executes on the function unit provided by the mask

    -   We can think about the threads' execution as independent of one
        another

3.1.1 SMIT Execution Masking

-   SIMT stack helps handle nested control flow and skipped computation
    when threads execute independently

    -   Nested control flow is when one branch is dependent on another

![A diagram of a computer program AI-generated content may be
incorrect.](media/image5.png){width="5.8127985564304465in"
height="4.632182852143482in"}

-   Serialization of execution is used by GPUs to "mask" the execution
    of threads in a warp, which deals with the issue of independent
    threads executing different branches.

    -   This serialization is achieved by using a stack

3.1.2 SIMT Deadlock & Stackless Architectures

-   SIMT deadlock is something that happens in stack-based
    implementations when some threads reach reconvergence points and are
    unable to "release locks" so that other threads on the top of the
    stack will spin indefinitely.

-   **Below is roughly based on NVIDIA Volta architecture**

![A screenshot of a computer AI-generated content may be
incorrect.](media/image6.png){width="5.861411854768154in"
height="5.81974300087489in"}

-   Barrier Participation Mask is used to track which threads within a
    warp participate in a convergence barrier.

-   Barrier State is used to track which threads have arrived at a
    convergence barrier.

-   Thread State tracks if each thread is ready to execute, blocked at
    convergence barrier (and which one), or has yielded.

-   Thread rPC tracks address of next instruction for each thread

-   Thread Active is flag showing if thread is active or not

-   ADD instruction is used to set bits in the convergence barrier, a
    WAIT instruction is used to stop warp splits when they reach a
    convergence barrier. A warp split is a subset of threads that all
    have the same PC (next instruction)

![A screenshot of a diagram AI-generated content may be
incorrect.](media/image7.png){width="5.8127985564304465in"
height="4.840526027996501in"}

3.1.3: Warp Scheduling

-   For "ideal" memory systems we can schedule warps in "round robin"
    form, were warps are given some fixed ordering. In practice, memory
    latency depends on application locality properties and off-chip
    memory contention, this type of scheduling can be either encouraged
    or discouraged.

**3.2: Two-Loop Approximation**

-   To reduce number of warps we can sometimes start executing
    instructions when previous instructions have not finished. This
    leads to dependencies within a warp (some instructions depend on
    previous instructions), and we can use either reservation stations
    or scoreboards to track dependencies.

    -   Reservation Stations eliminate name dependencies and introduce
        the need for associative logic, but is expensive in terms of
        area/energy

    -   In-order Scoreboard is very simple: each register is represented
        with a bit, a write instruction will set a bit in a register,
        and each read/write instruction must wait for the bit to clear
        before proceeding.

        -   Issues with in-order: too many registers = too many bits we
            need to implement. Lots of read ports required to look up
            operands, which is expensive.

-   In two-loop architecture, the first loop selects a warp that has
    space in the instruction buffer and looks up the next instruction.
    The second loop selects an instruction that has no outstanding
    dependencies and issues it for execution.

**3.3: Three-Loop Approximation**

-   GPUs need to support many warps per core to combat memory latencies,
    but this means that the register file will be very large (up to 256
    kb for recent NVIDIA GPUs) and with one port per register, SRAM will
    grow proportionally with number of ports. GPUs simulate high port
    counts by dividing up the register file into multiple banks of
    single-ported memories and then use arbitration and crossbars to
    connect to execution units.

-   The operand collector is used to control access to the register file
    banks and is our third loop in our gpu scheduling scheme.

![A diagram of a microarchitecture AI-generated content may be
incorrect.](media/image8.png){width="5.840577427821522in"
height="3.3612839020122482in"}

3.3.1: Operand Collector

-   Each instruction is assigned to a collector unit. Collector units
    will request operands from banks, either fetching immediately or
    waiting for conflicts to resolve. Operands are buffered inside the
    collector until all of them are ready, and then all operands are
    sent to the SIMD execution unit together.

-   The arbitrator coordinates different collectors to spread requests
    to maximize parallel use.

-   The operand collector may encounter WAR (write after read) hazards.
    One way to prevent this is to require instructions from a given warp
    to leave the operand collector in program order.

3.3.2: Handling Structural Hazards

-   GPUs can run into many different structural hazards like running out
    of collector units.

-   To avoid these issues, GPUs implement Instruction Replay, which is
    basically just an instruction waiting if encounters a conflict and
    executing later until it finally succeeds.

**3.4: Branch Divergence Research**

-   One main area of research is on branch divergence-how to handle
    differing instructions in a given warp.

3.4.1: Warp Compaction

-   One way to improve performance in GPUs that suffer from branch
    divergence is to group threads that take the same execute path into
    grouping with each other so that they execute at the same time.

3.4.2: Intra-Warp Divergent Path Management

-   Another solution is to interleave different paths of threads and
    bring merge branches earlier if possible, meaning that you don't
    have to wait if you can reconverge earlier

3.4.3: Adding MIMD Capability

-   Basically the GPU will support two modes, SIMD when branches are
    coherent and then switch back to MIMD when divergence spikes, merge
    back later.

3.4.4: Complexity-Effective Divergence Management

-   Idea is to replace the SIMT stack with other repurposable structures
    when the divergence is infrequent, and thus the area for the stack
    can be used for other things.

**3.5: Scalarization and Affine Execution Research**

-   GPUs can exploit value structure across threads. There are two types
    of value structures, Uniform Variables-a variable that has the same
    constant value for every thread and Affine Variables-a variable with
    values which are linear functions of thread ID for each thread in
    the kernel.

3.5.1: Detection of Uniform / Affine Variables

-   There are two main areas of research, compiler-driven detection and
    hardware detection at runtime.

3.5.2: Exploiting Uniform / Affine Variables in GPU

-   In terms of storage we can use a affine register file and partial
    file access/compression to cut energy costs. We can also keep a
    dedicated affine warp that packs base/stride data

-   For compute we can scalarize operations via a dedicated scalar
    pipeline

-   For memory we can treat affine addresses as base+stride to simplify
    coalescing and enable prefetch/expansion.

**3.6: Register File Architecture Research**

-   There are also active lanes of research that explore how to optimize
    register files to improve energy/area and bandwidth/latency.

3.6.1: Hierarchical Register File

-   We can use a register file cache captures short-lived values so that
    the main RF is not accessed as often.

3.6.2: Drowsy State Register

-   Lowkey don't know whats happening here

3.6.3: Register File Virtualization

-   Allocate physical registers on decode and reclaim them at "final
    read" via metadata (accounting for divergence) to halve RF size
    without performance loss in the evaluated setup.

3.6.4: Partitioned Register File

-   The Pilot RF splits storage into a small fast FRF and large
    near-threshold SRF, uses the operand collector to hide SRF latency,
    and profiles hot registers with a pilot CTA to pin in FRF.

3.6.5: RegLess

-   Replace the RF with an operand staging unit plus memory, preloading
    per-region live operands under a capacity manager and compressing
    (e.g., affine) values to cut traffic.
