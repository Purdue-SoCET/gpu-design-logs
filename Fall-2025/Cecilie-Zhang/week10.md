# Week 10
**State:** I don't need help right now

**Progress:**
- Friday (10/24):
    - Visited Sooraj's office hour to understand the structure of the cache. The tag and data arrays need to be separate. It will take one cycle to do the tag lookup and another cycle to look up the data at that address
    - Checked on the MSHR buffer. I initially thought that the data would move from one latch to another. However, that would cause a lot of wiring. Additionally, the digital logic from the wires would interfere with the fucntionality of the SRAM
    - I need to look into the actual RTL code of Aksath's lockup-free-cache and make questions for Sunday about details or things I don't understand
    - Annotated the lockup_free_cache.sv, cache_bank.sv, and the cache_mshr_buffer.sv. This can be found in ./gpu-design-logs/Fall-2025/Cecilie-Zhang/cache_RTL

Questions: 
1. What is the hit and miss latency?
    - Assume a latency and parametrize it if we want to change it later
2. For lien 115-120, why is it traversing through all banks to see a hit? Why can't we just use bank_id as the index to the bank_hit to see if it hits in that bank? 
3. In cache_banks, cache_bank_busy means that if a bank's MSHR buffer is serving a miss, then the entire bank is busy?
    - Yes the bank is busy in the sense that it can't serve any more miss request but it can serve hit requests 
4. In the MSHR buffer, are the data moved from one latch to another? Is it using a pointer that points to the top of the queue?
    - Data is moved from one latch to another. This was synthesized in the previous semesters and it was fine
5. In cache_banks, I'm having a bit of trouble understanding the condition for when the count_FSM is incremented (line 108)?
6. Why is UUID an output? Isn't UUID generated in the MSHR buffer?
    - The MSHR buffer generates a mem_out_uuid first to the LSU for a missed request. Once that missed request has been servied, the cache will output the shceduler_uuid_out
      and the shceduler_uuid_ready signals. 
7. How does the cache return the missed data? Doesn't it lose its original memory request? The LSU will have to reschedule the memory request?
    - The LSU will have to reschedule read requests but not write requests because the data will be written back when the RAM data is placed into the cache

- Thursday:
    - Dicussed how the interfaces for the pipeline stages and how forwarding would work

- Reworked on the cache to fit the base class structure
- Added comments to the gpt generated code to double check the logic and ensure that I understand what's going on
- Next week:
    - Finish testing the cache by Thursday and connect it with the LSU/rest of the subteam