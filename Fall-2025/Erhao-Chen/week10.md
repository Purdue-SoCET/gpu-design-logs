# Week 10
statement: I am not stuck.

## Current plan
- Our plan is to continue developing C kernels that mimic an OpenGL-style workflow. We decided that we will not build custom C library
- After the work was assigned, I will be working on the unit test for now.
  
## Work
- For the initial unit test, we will first write on the simplest SAXPY kernel:
  
```
void saxpy(int n, float a, float *x, float *y)
{
  int i = blockIdx.x*blockDim.x + threadIdx.x;
  if (i < n) y[i] = a*x[i] + y[i];
}
```

- Here are some initial uncompleted implementation.
- We need to load the kernel arguments (n, a, *x, *y) into memory so our lw instructions can access them.
- Use LW to manually store data n,a,x,y from memory to register.

```
lw x4, 0(addr1) #n
lw x5, 0(addr2) #a
lw x6, 0(addr3) #x
lw x7, 0(addr4) #y
```

## Next step
There are several questions needed to be solved.
- What are the CSR addresses?
  - We need to finalize how the unit test accesses blockIdx.x, blockDim.x, threadIdx.x, so that we can use csrr instruction correctly.
- How do we load data?
  - At the end, we should have a single memory file like .hex or .bin that simulator can load.  






  
