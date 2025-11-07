State: I am not stuck with anything

# Progress

## Work Completed:
* Continued CSR discussions
* Completed Triangle Kernel and completed basic test framework
* SAXBY test program
* Began initial development of Pixel Kernel

## Progress

### CSR Discussions
* To simplfy hardware, the threadIDs and blockIDs will be given as one dimensional values
* To replace this, the program can divide threadID by the blockDims to replicate the dimensionality
* This can then be implemented in one of two ways
  1) Compilers can allow our programmers to refernce threadID.x/y/z and autu compile it into the correct math
  2) Software can only use one dimension, manually cacluating multiple dimensions when needed
  * A finalized decisions has **NOT** been made

### Triangle Kernel Testing
* The triangle kernel was integrated into a CPU_SIM test program, and got compiling
* Simulated with two overlapping triangles, with one shared point and two unique ones
* Small grid of pixels and limited grid used to simulate
  * Results shown with a 2D matrix print -> Appears funcitonal

### SAXPY Test Program
* A basic SAXBY kernel was developed and integrated with the CPU sim
* This Kernel was made to replicate and math the funcitonality of a hand-written test assembly program written by Tushar
* Test output was shared with Tushar and hardware for comparision and testing of results with the original assembly

### Plans for integration
* Once the pixel kernel development is completed, and Aidan gets a basic OpenGL call integrated into the sim, a larger CPU_SIM program can be developed
* This can integrate all of our kernels, and allow us to start doing larger scale, **thorough** testing