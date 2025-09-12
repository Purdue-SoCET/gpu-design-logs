# Week 3
statement: I am not stuck.
## Progress
Finish reading chapter 4 

## Learning and key concept

### Chapter 4

### Introduction

- Memory difference in CPU and GPU
  - CPU:
    - register file
    - main memory
  - GPU:
    - local memory: private memory for single thread, used when thread out of registers, slow
    - global memory: DRAM accessible for all threads for entire GPU, high latency
    - scratchpad: shared memory, shared by thread block, small but fast
    
### 4.1 First-level memory structures

- Scratchpad Memory and L1 Data Cache
  - bank: bank is the physical hardware that
  - bank conflict: when there are two or more threads in the same warp try to access the same bank at the same time.
  - L1 cache: stores the subset of the global memory memory
  - coalesced access: threads in a warp access locations in a cache block
  - uncoalesced access: threads in a warp access locations in different cache block

- 4.1.1: Unified L1 Data Cache and Shared Memory
<img width="990" height="623" alt="2025-09-11 163337" src="https://github.com/user-attachments/assets/98a75211-200a-46c7-a864-4d5e0c473928" />

  - 1: Load/Store Unit: send memory access request, consists of a set of memory addresses one for each thread om a warp with operation type
  - 2: Arbiter: if (bank_conflict) -> accept the non conflicting part; reject conflicting part -> go to replay mechanism;
  - 3: Tag Unit: if (cache hit) -> the appropriate row of data array is accessed in all banks and data is sent to 6, which is register file; else(cache_miss) -> the request is sent to #7 Pending Request Table, and then send to 8 MMU (memory management unit)
  - 4: Address Crossbar: take the set of address for a warp and sent the individual address to the 5 Data bank.
  - 5: Data: it is the SRAM, which consists of multiple individual banks.
  - 6: Data Crossbar: After passing the data from 5, the data cross bar rearrange the corresponding data for each thread to make it the right lane. Then it is written to Register File.
  - 7: Pending Request Table (PRT): This is where when we encounter cache miss. It records which address is missed.
  - 8: Memory Management Unit (MMU): transform virtual address to physical address
  - 9: Fill Unit: Write the data for cache miss. It took those data and sent to 5 Data array, and tells 2 arbiter after this has been put into data array.
  - 10: Write data buffer (WDB): The data to be written including global memory or shared memory is first put in WDB.

- 4.1.2: L1 textrue cache
<img width="824" height="955" alt=" 2025-09-11 223101" src="https://github.com/user-attachments/assets/1c744375-fceb-443d-a3b8-cdbe56ef8519" />

- This is a special part for graphic textures. The special of this process is that when we encounter a cache miss, which requires time for memory access, the Part 3 Fragemnt FIFO can continuoly working which makes the texture cache busy to make efficient. Although we increase the clock latency, the throughput improve.

### 4.2 On chip interconnection network

- The SIMT core use interconnection network to connects the memory partition.
- NVIDIA calls it crossbar
- AMD calls it ring networks

### 4.3 Memory Partition Unit
<img width="882" height="627" alt=" 2025-09-11 224522" src="https://github.com/user-attachments/assets/ab989a1f-9f7c-4e3d-ad50-e8fbe034539c" />

When memory request was missed in the SM, we need to access this memory partition unit. We first check if it is in L2 cache, if it is, we return the data and sent through corssbar to SM. If L2 cache miss, the request is pass to memory access scheduler. Then it sent the request to the off chip DRAM. When the data return from DRAM, it sent back to L2 cache and then sent to SM. 

### 4.4 Research for memory system
- MEMORY ACCESS SCHEDULING AND INTERCONNECTION NETWORK DESIGN
- CACHING EFFECTIVENESS & MEMORY REQUEST PRIORITIZATION AND CACHE BYPASSING
  - Fetch a large cache block for a single small read is inefficient. Solution is to create a prediction if the memory is used frequetly or not.  








