# Week 8
statement: I am not stuck.
## Key points from discussion
- CPU simulation:
  - Our current task is to create a CPU-based simulation framework. This will allow us to write and debug our graphics algorithms in C without waiting for the GPU compiler.
- Functional simulator:
  - The interface is that we could provide a hex file (initial memory state), and receiving a final memory dump as output. 

## CPU simulator
Our primary goal is to build a host program in C that can simulate the GPU exectution.
- parallel simulation: The host program will call our C-based kernel functions with a loop to simulate the execution across all threads.
- control of kernel: The host program will manage the execution flow of the entire process in 3 stages, including vertex, triangle and pixels in sequence. It could handle the memory state between these stages.
## Functional simulator
- Input: We will provide an initial memory state, which is compiled from the C kernels into a hex file. Then, provide the paraemters for the initial lauch such as number of threads.
- Output: We expect that the simulator can have a memory dump at the end of run.
- Automate: might develop a wrapper script to automate the entire testing process. It can do the simluation and also for the result check for each stage. 
