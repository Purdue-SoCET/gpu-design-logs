Week 4 (Chapter 5.1 Notes)

Status: Finishing up notes, just need a little time to digest
information I think

Progress: Finishing up reading

Chapter 5: Crosscutting Research on GPU Computing Architectures

**5.1 Thread Scheduling**

-   There are three main ways that threads are scheduled within GPUs

    -   Assigning threads to warps (to step together in lockstep)

    -   Warps are bundled together in threadblocks and are scheduled to
        cores in bulk

    -   Cycle-by-cycle schedulers decide which set of warps to fetch
        instructions for, which warps to issue instructions for, when to
        read/write operands or issued instructions

5.1.1 Threadblock Assignment to Cores

-   On kernel launch, threads are grouped into threadblocks, which are
    distributed across cores by a scheduler.

    -   The baseline scheduling policy is round-robin

-   Throttling approach monitors idle cycles and memory delays to
    deliberately limit the number of threads per core.

-   Equalizer approach dynamically adjusts the number of threads, as
    well as frequencies, based on workload demands. It uses counters for
    active warps and memory stalls to balance throughput/energy
    consumption

    -   There is an energy-saving mode and a performance enhancer mode

    -   Equalizer classifies workloads based on compute, memory and
        cahce usage, tailoring frequencies to benefit each type of
        workload

    -   Equalizer makes local decisions and reports to a global
        controller. They often use a majority vote system.

5.1.2 Cycle-by-cycle scheduling decisions

-   For early GPUs, fairness-based warp + DRAM scheduling improved
    performance for balanced workloads by exploiting row-buffer locality

-   A two level scheduler divides warps into active pools and inactive
    pools, active means eligible for issue and inactive means
    temporarily excluded.

    -   Warps move out of the active pool when they stall on
        long-latency operations and rejoin in round-robin order

        -   This design emphasizes energy efficiency

-   Another two level scheme is to group warps into "fetch groups" and
    stagger them when long-latency operations are reached

    -   This preserves cache/DRAM row-buffer locality, reducing
        contention.

        -   This design emphasizes performance

-   Cache conscious warp scheduling observes that in cache-sensitive
    workloads, intra-warp locality (warps reusing the own cached data)
    is way more common than inter-warp locality (sharing data across
    warps) and throttles the number of active warps when too many are
    competing for L1 cache.

    -   There is a mechanism to detect lost-locality, on a cache
        eviction the victim tag is stored in a private array and if the
        warp misses again on the same line, the system recognizes that
        it has lost useful data

![A diagram of a data flow AI-generated content may be
incorrect.](image12.pngpng){width="5.47944772528434in"
height="3.5487937445319333in"}

5.1.3 Multiple Kernel Scheduling

-   Modern GPUs can run multiple kernels at a time, making scheduling
    decisions similar to multiprogramming on CPUs.

-   Each threadblock consumes resources and states are hard to save if
    those resources need to be preempted to use run higher priority
    workloads

-   Chimera is an approach where it dynamically chooses between a full
    context save/restore, waiting until the block finishes, or stopping
    and restarting the kernel

    -   This is implemented with an algorithm

5.1.4 Fine Grain Synchronization Aware Scheduling

-   There have been hardware structures proposed to dynamically identify
    which loops are involved with spin locks

    -   Once a warp is detected as spinning, its scheduling priority is
        reduced to ensure that lock-holding threads can make progress
        and release resources
