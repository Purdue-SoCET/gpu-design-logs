# Week 15
**State:** I don't need help right now

**Progress:**
- Completed the final design review on Wednesday (3rd December)
- Made changes to the ld/st unit to use the dCacheReqeust and dCacheResponse classes that are defined in base.py. For connection between LSU and dcache, we only need to call the connect_interface method which is part of the LSU object. 
- On Thursday, we decided to slow down and focus on testing each unit rigorously first. Everyone should make a list of unit tests that would test the "basic" functionality as well as edge cases. I think that's a good idea because if each unit is not tested properly, it's going to take almost double the time to identify the issue once the units are integrated because several parts could be breaking at the same time.
- The test cases that I have developed so far:
    1. Reading to all ways in set 0 for bank 0 and bank 1 - Testing miss functionality
    2. Writing to all ways in set 1 for bank 0 and bank 1 - Testing for miss and writing functionality
    3. Reading to all ways in set 0 for bank 0 and bank 1 - Testing hit functionality
    4. Writing to all ways in set 1 for bank 0 and bank 1 - Testing hit functionality
    5. Secondary miss - Read after write. Should merge the read request with the existing write
        - I'm a bit confused about this. Because the read request would have to be replayed and it will read the new value even though the original request intended to read the old value before it was written to
    6. Secondary miss - Write after write
    7. Secondary miss - Write after read
    8. MSHR Full - should stall
    9. Victim ejection of a dirty block - The memsim.hex file should contain the dirty data
    10. A sequence of hits and misses - the hits should be serviced while the misses are being serviced
    11. Seqeuence of hits - The cache stalls as long as the hit latency
    12. Halt - The cache should write back all dirty data and send flushed to LSU

**Next steps:**
- Work on the final report due on friday
- Submit all the various docments for SoCET