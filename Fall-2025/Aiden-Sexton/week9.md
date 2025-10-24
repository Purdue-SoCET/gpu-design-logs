State: I am not stuck with anything

# Progress

## Work Completed:
* Created CPU sim framework for kernels
* Met with hardware to clarify qestions

## Progress:

### Function Calls
* New "Managerial" instructions, i.e. single threaded, needed to handle function calls
  * Manipulate predicate register
    * Shift predicate registers (to clear earlier ones so a function can start at P0)
    * store/load predicated registers to load additional predicates on the stack
  * Manipulate PC, i.e. jump
    * Should already exist
* Will have a **per-warp stack**
  * Each warp will need its own stack pointer, which software can't generate currently
  * **Either** hardware will have to generate the Stack Pointers
    * This would either force fixed stack pointers, or require hardware to take another input of stack size, and the 1st stack pointer
  * **OR** will have to expose a warpID to software to allow per-warp generation

### Memory Map
* Initial thoughts progress was stopped by confusion about the shared CPU/GPU memory map
  * Current decision is to currently not consider a CPU
* Will need a special memory section purely for use as the testbench to place large input data in, and for output data to be written back to
* Need to speak to compilers about the possiblity of giving them a **linker script** of sorts. Would allow programs a lot more versatility in how we lay them out

### Hardware Unit Tests
* Hardware want's test cases for the functional simulator
* As per hardware meeting on 10/23, should be more complex then testing of a single instruction, instead repersenting a few common operations that will be used
* Current thoughts on programs
  * project -> project kernel data
  * interpolcate -> Interpolate a point between 3 vertexs

### Update on our software library
* Need 