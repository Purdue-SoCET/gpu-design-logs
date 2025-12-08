# Explicit Statement: I am not stuck

- Questions for Hassan:  
  - In cycle\_through\_scalar\_regs(), we only elect a single thread to be scalarized, is that what we want to do? Or do we want to elect multiple threads to be scalarized every cycle?  
  - This assumes that every cycle, we are going to issue one thread per warp to be scalarized (assuming the warp contains an eligible thread)  
    - This means that scalar regs will have backpressure no??  
  - **How am I getting a thread ID of 36???**  
    - Syntax error somewhere in the code was messing it all up  
      - Weird error, moving an instruction up or down a few lines causes segfault  
        - I commented “DO NOT MOVE” next to that instruction  
- Need to think about larger implications of thread scalarization per cycle  
  - How is this possible? If we have 8 scalar registers and 32 warps:  
    - Suppose only 4 active warps, then worst case time complexity of scalarizing a thread is undefined because that warp may not issue again\!  
      - This is a huge problem, need to think about this  
      - Is a large delay in thread scalarization a huge problem? What defines a “large delay”?  
    - One option is to include the RR scheduling scheme in the cycle() top level function call so that EVERY warp checks one scalar register each cycle  
      - Overkill? Need to think