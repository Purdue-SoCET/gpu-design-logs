# Week 11
statement: I am not stuck.

## Current status
- first test SAXPY is still waiting the final CSR addresses for blockIdx.x, threadIdx.x
- At the same time, we need to began the next unit test.
  
## Work
- Current test SAXPY
  - the status is that still not finalized the CSR addresses for blockIdx.x, blockDim.x, and threadIdx.x.
  - it only covers basic arithmetic and predication. It does not test function calls or stack management.
  
## Next step
- we need a new unit that tests for function call and if stack is working.
- The hardware will not manage the stack pointer automatically for each thread. 
- So the software must manually calculate each thread's private sp in our assembly code.
- proposed logic
  - sp = (stack_space) + (thread_in_warp_ID * 4)
- The unit test should follows:
  - reads the thread ID from its CSR
  - gets the private sp using div/mul/add
  - saves the return address to that sp
  - restores the return address after function
- pseudocode
```
//reads the thread ID from its CSR
csrr x10, address //x10 = threadidx_x

//gets the private sp using div/mul/add
sp = (stack_space) + (thread_in_warp_ID * 4)

//saves the return address to that sp
sw  x1, 0(x2)  //x1 (ra), x2 (sp)

//jal to new fucntion
jal  x1, func

//restores the return address after function
lw ra, 0(sp)
```





  
