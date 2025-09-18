Status: no help needed so far

# Crosscutting Research on GPU Computing Architectures
## 5.1 Thread scheduling
1. Assignment of Threads to Warps
Threads are fused together for lock-step execution via warps. Thus, threads with consecutive thread IDs are statically fused into warps.

2. Dynamic Assignments of Threadblocks to cores
Work is assigned in bulk via threadblocks. Baseline has threadblocks assigned in round-robin order. Resources are "subscribed" (accessible?) at thread-block level. Thus, execution is not preempted, running to completion before resources of one threadblock is assigned to another. 

3. Cycle-by-Cycle Scheduling Decisions
Hardware schedulers decide (cycle-by-cycle) which warps to fetch, execute, and read/write operands.

4. Scheduling Multiple Kernels
2 and 3 can happen within a singular kernel and/or access different consecutive kernels.

## 5.1.1 Assignment of Threadblocks to Cores
At kernel launch, threads within each kernel are grouped into threadblocks, which are assigned to SIMT cores based on resource availability. Each core has fixed resources: scratchpad/shared/local memory, number of registers, slots for warps, and slots for threadblocks. Obvious approach is round-robin to maximize number of cores, until at least one resource is exhausted in each core. 

### Throttling at the Threadblock level
(Kayiran et al. [2013])
Done to reduce contention in memory system caused by thread over-subscription. An algorithm monitors core idle and memory delay cycles. It assigns each core half its max thread blocks, then checks for said delay cycles. If a core is mostly waiting for memory, no more threadblocks are assigned and existing threadblocks are potentially paused from issuing instructions. 
This achieves a "course-grained parallelism" throttling mechanism, limiting memory system interference and improving overall application performance with less CTAs active. 

### Dynamically Tuning GPU Resources
(Sethia and Mahlke [2014])
Equalizer: dynamically monitors resource contention. Scales number of threads, core and memory frequency.

#### Four parameters to base decisions
1. number of active warps in an SM
2. number of warps waiting for data from memory
3. number of warps ready for arithmetic instruction
4. number of warps ready for memory instruction
First, it decides number of warps to keep active per SM. Then it decides how to scale frequency of core and memory system. 

#### Two modes of operation
1. Energy-savings mode: scales back under-utilized resource
2. Performance-enhancing mode: boosts the bottleneck resource, increasing performance in an energy-efficient manner.   

#### Types of workloads and method of improving energy without sacrificing performance
1. Compute intensive: lower memory frequency
2. Memory intensive: lower SIMT core frequency
3. Cache sensitive: number of CTAs
4. Unsaturated: number of CTAs

## 5.1.2 Research on Cycle-By-Cycle Scheduling Decisions
See powerpoint below:
[GPGPU Research 5.1.2.pdf](https://github.com/user-attachments/files/22415482/GPGPU.Research.5.1.2.pdf)

## 5.1.3 Research on Scheduling Multiple Kernels
### Supporting Pre-emption on GPUs
(Park et al. [2015])
To enable flushing of computation within a threadblock, it uses a more relaxed definition of "idempotence": detecting whether execution has been "idempotent" from start of execution. 
Idempotent: Something can be applied/executed multiple times without changing much. Ex. pushing the "on" button multiple times for a control panel. 

#### Three approaches to achieve context switch for each threadblock via Chimera
1. full context save/store
2. waiting until threadblock finishes
3. simply stopping threadblock without saving if, due to idempotence, threadblock can be restarted from beginning safely. 
These approaches provide different tradeoffs between latency and throughput. To implement this, an algorithm estimates number of threadblocks which can be stopped with minimal impact on throughput while meeting latency target. 

## 5.1.4 Fine-grain synchronization aware scheduling
(ElTantawy and Aamodt [2018])
Problem: significant overheads occur when threads spin waiting for locks. Backing off execution of warps containing threads that have fails to acquire a lock prevents/slows progress of other threads in same warp already holding lock (SIMT deadlock?). Thus, hardware structure for dynamically identifying spin locks, but made more challenging by use of stack-based reconvergence. 
This structure uses a path history, containing LSB of PC and separate history of predicate register updates to accurately detect spin locks. Reducing priority of warps identified as spin looping, which reduces energy by 1.5x and improves performance. 
