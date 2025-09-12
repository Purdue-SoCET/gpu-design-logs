# **Status**
I am currently not stuck or blocked

# **GPU Notes Shresth Mathur**

Taken on *General-Purpose Graphics Processor Architectures* by Tor Aamodt, Wilson Fung, and Timothy Rogers \- 2018

# **Chapter 4: Memory Subsystem**

#### 4.1 First-Level Memory Structures

* Scratchpad Memory and L1 Data Cache  
  * Explores the design and utilization of scratchpad memory (also known as shared memory) alongside the L1 data cache, highlighting their roles in facilitating low-latency data access for threads within a warp.  
* L1 Texture Cache  
  * Discusses the specialized L1 texture cache, optimized for texture fetching operations, and its impact on memory bandwidth and latency.  
* Unified Texture and Data Cache  
  * Examines architectures that unify texture and data caches to improve resource utilization and simplify memory hierarchies

#### 4.2 On-Chip Interconnection Network

* Analyzes the on-chip networks that interconnect various GPU components, focusing on their topology, bandwidth, and latency characteristics, which are crucial for efficient data movement.​

#### 4.3 Memory Partition Unit

* L2 Cache  
  * Details the structure and function of the L2 cache, which serves as a shared cache among multiple streaming multiprocessors (SMs), and its role in reducing off-chip memory accesses.  
* Atomic Operations  
  * Covers the implementation of atomic operations within the memory hierarchy, essential for synchronization and data consistency in parallel programs.  
* Memory Access Scheduler  
  * Describes the scheduling mechanisms that manage memory requests, aiming to optimize throughput and fairness among concurrent threads.​

#### 4.4 Research Directions for GPU Memory Systems

* Memory Access Scheduling and Interconnection Network Design  
  * Investigates advanced scheduling algorithms and network designs to alleviate contention and improve data transfer efficiency.  
* Caching Effectiveness  
  * Explores strategies to enhance cache utilization, including cache coherence protocols and replacement policies tailored for GPU workloads.  
* Memory Request Prioritization and Cache Bypassing  
  * Discusses techniques to prioritize critical memory requests and selectively bypass caches to reduce latency and prevent cache pollution.  
* Exploiting Inter-Warp Heterogeneity  
  * Examines methods to leverage differences in warp behavior to optimize memory access patterns and resource allocation.  
* Coordinated Cache Bypassing  
  * Looks into coordinated approaches for cache bypassing across multiple warps or thread blocks to improve overall performance.  
* Adaptive Cache Management  
  * Considers dynamic cache management techniques that adjust to workload characteristics in real-time.  
* Cache Prioritization  
  * Analyzes policies for prioritizing cache access among competing threads or data types to enhance performance.  
* Virtual Memory Page Placement  
  * Studies the impact of virtual memory systems on GPU performance, focusing on page placement strategies that minimize latency.  
* Data Placement  
  * Investigates optimal data placement within the memory hierarchy to balance load and reduce access times.  
* Multi-Chip-Module GPUs  
  * Explores the architectural considerations and challenges associated with GPUs composed of multiple interconnected chips, particularly concerning memory coherence and communication.
