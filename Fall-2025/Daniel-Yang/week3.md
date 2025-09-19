Week 3 (Chapter 4 Notes)

Status: Progressing, just working on readings for now

Progress: Reading Chapter 3 of Textbook

Memory System

This chapter is about the memory subsystem of the GPU. Traditionally,
GPUs interface with a couple of different memory spaces (texture,
rendering, etc.) and this chapter will focus on the microarchitecture
required to support them. The two main memory spaces are the register
file and the memory. The memory is further subdivided into local/global
memory, where local memory is private to a thread and global memory is
shared.

**4.1 First-Level Memory Structure**

This section covers the L1 and scratchpad "shared memory" cache and how
these interact.

4.1.1 Scratchpad Memory and L1 Data Cache:

-   Shared memory is on chip low latency memory that is accessible by
    every thread (often referred to as scratchpad)

    -   Usually implemented with SRAM and is explicitly managed by
        programmer

-   L1 cache contains a subset of the global memory address space and
    automatically stores recent data

-   **The following diagram does NOT support cache coherence**

![A diagram of a computer hardware system AI-generated content may be
incorrect.](image9.png){width="4.106830708661417in"
height="2.659662073490814in"}

**Shared Memory Access Operation**

-   The memory arbiter will determine if requested addresses have bank
    conflicts and split up requests into non-conflicting threads and
    conflicting threads

    -   If two or more threads in a warp access the same bank, conflict
        occurs

    -   The conflicting request will be replayed again after the first
        execution

> **Cache Read Operations**

-   L1 cache accesses are hardware only access

-   Memory access is broken down into transactions, with each
    transaction corresponding to contiguous block of addresses

    -   If accesses are aligned throughout threads, the hardware can
        combine them into a coalesced access

-   Cache hit means data was found in the cache and there is no need to
    fetch it, cache miss means data was not in the cache and we need to
    look for it (by searching downwards by hierarchy)

> **Cache Write Operations**

-   Data to be written is pushed into a write buffer

-   The GPU can bypass cache and send the data straight to memory

-   Traditionally the GPU does not support coherence between SMs, which
    causes some architectures to limit the type of data that can be kept
    in the cache

4.1.2 L1 Texture Cache:

-   Recent architectures have combined the l1 and the texture caches

-   Rendering graphics uses images (textures) and surfaces for more
    realism. There is strong spatial locality here (adjacent
    pixels/texels are related)

-   Texture caches use a FIFO between the tag and the data, inserting
    pointers on a hit and inserting into a different (miss) FIFO on a
    miss.

![A diagram of a computer program AI-generated content may be
incorrect.](image10.png){width="5.215545713035871in"
height="5.944749562554681in"}

4.1.3 Unified Texture and Data Cache:

-   Modern GPUs unify L1 Data and texture caches to save chip area and
    simplify design, usually allowing only read-only data to be stored
    to the cache.

**4.2 On-Chip Interconnection Network:**

-   GPUs connect to multiple DRAM chips in parallel via memory partition
    units and memory addresses are distributed across the partition
    units using address interleaving

**4.3 Memory Partition Unit:**

-   Each partition unit contains an L2 cache and a frame buffer/raster
    operation unit

    -   The L2 cache contains both graphics and compute data

![A diagram of a computer component AI-generated content may be
incorrect.](image11.png){width="5.694737532808399in"
height="4.069653324584427in"}

4.3.1 L2 Cache:

-   The L2 cache is logically unified but physically distributed across
    partition units

    -   Parallelism is achieved through this distribution of the L2
        cache

-   L2 acts as a buffer between the cores and off-chip DRAM

-   L2 contains both reads and writes

4.3.2 Atomic Operations:

-   There is a local ROP cache for ROP specific operations

    -   Operations can be used for implementing synchronization across
        threads in different blocks

4.3.3 Memory Access Scheduler:

-   The memory access scheduler decides the order which requests get
    sent to the DRAM

    -   DRAM consists of multiple banks which are costly to access, so
        the scheduler tries to maximize access by reusing rows in DRAM

    -   Requests may be serviced out of order in order to reduce
        conflicts and idles

**4.4 Research Directions for GPU Systems**

-   **Memory Access Scheduling and Interconnection Network Design**

    -   Research explores different schedulers/interconnects to balance
        throughput, fairness, efficiency

    -   Ex: FR-FCFS scheduling which prioritizes row-buffer hits

-   **Caching Effectiveness**

    -   Research studying the effectiveness of caches, workloads with
        poor locality may see no speedup or even slowdown

    -   Ex: Streaming workloads like video decoding will bypass caches

-   **Memory Request Prioritization and Cache Bypassing**

    -   Cache bypassing prevents filling of the cache unnecessarily by
        steering low-locality requests to the DRAM directly

-   **Exploring Inter-Warp Heterogeneity**

    -   Different Warps will exhibit different memory patterns, so
        research aims to change policies on a per warp basis

    -   Ex: Divergent warps with scattered access may bypass the cache,
        aligned warps with coherent caches will exploit caching

-   **Coordinated Cache Bypassing**

    -   Instead of per-SM decisions, coordinated bypassing improves
        global cache utilization

-   **Adaptive Cache Management**

    -   Dynamic runtime systems adjust cache replacement/bypass policies
        based on workload behavior

-   **Cache Prioritization**

    -   Research into setting priority levels to memory requests, so
        latency-sensitive requests gain preference

-   **Virtual Memory Page Placement**

    -   Smarter page placement improves data locality and reduces costly
        migrations

-   **Data Placement**

    -   Compiler/runtime systems predict optimal locations for data to
        minimize serialization and improve reuse

-   **Multi-Chip-Module GPUs**

    -   Research attempts to break GPUs into smaller models to imptove
        scalability and cost
