State: I am not stuck with anything

# Progress

## Work Completed:
* Submitted research abstract
* CPU sim planning

## Planning
### Benchmark File Structure
* Benchmark/
  * Kernels/ -> Contains the various gpu kernels for the benchmark
    * eg: pixel.C, triangle.C, test.C
  * cpu_sim/ -> Top-level CPU C code which can compile kernels and run them serially
    * eg: cpu_main.c
  * gpu_emulator/ -> Top-level script to run emulator
    * eg: esim_main.py
  * gpu_funcsim/ -> Top-level script to run functional simulator
    * eg: fsim_main.py
  * Makefile

### Timeline Issues
* Hard for us to work on C code without a compiler...
  * Initially, can create a **CPU sim** which will replicate the functionality
  * Need to know from compilers:
    * When will we get a finished compiler to test C code

### CPU Sim
* C code which can be compiled with and run .C files as though they were GPU Kernels
* Requirements:
  * Will need preprocesser directives to handle GPU specific code, namely ThreadID, BlockID, DlockDim
  * Need to call kernel repetedly to replicate GPU threads
  * Can have defines in the kernel code with global variables to act as trackers of thread divergence
* Will be very slow/ineffective
  * Will encourage us to develop smaller unit kernels, which should hopefully help us during testing on the slow functional sim or hardware sim

### Basic Graphic Unit Tests:
* Per Vertex kernel tests:
  * Translate a Series of 3D vertexs
    * Will show basic addition, simple case
  * Rotate a Series of points
    * Will involve multiplying all vectors by the same rotation matrix
* Per Triangle tests:
  * Single Triangle Rasterization
    * Working on less perfectly parralizable task
  * Depth Test
    * More complex math, and need to adress possible inter triangle dependencies
* Per Pixel tests:
  * Screen-Space inteprolation
    * Simpler interpolation, will provide simpler test
  * Perspective corrected interpolation
    * Largest complexity of math, but highly parralizable (per pixel)