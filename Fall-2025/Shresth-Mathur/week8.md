# Explicit Statement: I a	m not stuck

- **void scheduler\_unit::cycle()**  
  - That is where the top level scheduler policy should go (the 2 conditions)  
- We can make the scheduling scheme better   
  - RR cycles through each warp looking for elected threads even if the warps hold no elected threads  
    - Make it choose from active warps  
- Discussed the cycle\_through\_scalar\_registers function  
  - In the current function, each time a warp is issued it checks its warps reg\_cntr and looks at the corresponding register to see if it is dirty so that thread can be elected  
  - Problem is that if there are 8 scalar registers and 32 warps, if we wanted to scalarize reg 8 on warp 32, we’d have to wait for (total warps/warps issued per cycle) x (reg \#) → (32/4)x(8) \= 64 cycles, and 64 cycles where warps are actually issued  
    - In many cycles no warp is issued, meaning no progress in the warp RR scheme for those cycles  
  - Need to understand the tradeoff because if divergence lasts 1000s of cycles, then a couple hundred cycles is not a huge deal in terms of latency from saturating counter reaching sat limit to being pushed to scalar que  
  - **My update (for loop in cycle through scalar regs) makes it so that in one cycle, we perform a priority encoding in hardware to select the first eligible scalar register to be scalarized, and then that scalar reg has least priority in the next cycle**  
    - **This ensures fairness and will never lead to starvation**  
    - **This special type of priority encoder is called a rotating priority encoder**