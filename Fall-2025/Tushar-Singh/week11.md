Progress:

I am not stuck with anything right now.

GPU subteam: Graphics

## Overview

I have written the saxpy asm file. We then got to testing it on the simulator, which revealed several issues. The assembler itself was not up to date, and then when we tried to run the corrected version of the saxpy on the GPU.

### Saxpy

Overall, the process to write an asm is very hard. I had to ask the assembler person to add some more functionality(assembler directives) so that I could add data labels to the asm. Currently, I have to manually append the data in order to get an executable. This meant manually calculating memory addresses and using calls of lli, lmi, which were rather difficult to work with. We produced a CPU equivalent to allow us to verify the output of the saxpy. Because CSR's are not being decided on until the next weekend meeting, the correct function of the code cannot yet be asserted. The Saxpy is currently limited to just 1024 elements, when any number in the 32 bit space should be accessible and worked on. If the GPU cannot handle more than 1024 pieces of data at once with basic indexing, we will run into major issues.


### Function call asm

I am also writing an asm that tests a function call. The hardware team has asked for this. I am confused as to why they would ask for this when their simulator cannot verifiably execute code, but nonetheless I am doing it. The idea is that I will write an asm label called "project" that will do a common math routine. It will use its own registers. Then, with a callee saving system, I will save registers that are intended to be used by the routine and then execute the routine. The registers should all be restored when execution is done. The stack status should be identical for all threads when the function is returned from. Even if only some threads execute a function, the final stack state should be the same as before. We require this for proper operation.

The function call must also preserve the predicate. Predicates are hard coded into instructions, but the entries themselves can be manipulated. This should be functional so that we can enable general programmability. Function calls inside of a kernel are not common. One case where they may be used is if certain flags are enabled inside of a kernel. We want to be able to do some extra processing only sometimes, so functions would be very helpful for this as the context may be the same between some functions, making the overhead of starting a kernel avoidable. This would also let us precompile some shaders in the future and insert them as needed. Otherwise, function calls are rather rare and hopefully not particularly needed in favor of aggressive inlining.


### CSR Discussion

Each thread needs to access CSR's to initialize itself correctly. These will allow it to distinguish itself from other threads using its ID. The CSR is set up by the GPU when it is preprocessing for a kernel. In CUDA, there is the threadblock, the warp, and the thread. These can each have 3 dimensions. We are going to make the threadblock 1 dimensional, but then the lowest level of the programming model will retain dimensionality. This adds up to about 5 CSR's. Because no agreement has actually been made, it must be discussed in the next meeting. We need a CSR mapping so that assembly will be useful. The SAXPY program can then be extended from 1 threadblock to many, and the array size from 1024(1 element per thread) to many elements per thread. This functioning correctly would be a great sign for the GPU.

### Other Members

I am responsible for writing some asm kernels. Much of this means I get to find issues in understanding between teams, which is good as it makes us closer to a functional product. 

Aiden and Aidan are making GPU C kernels. These kernels will represent the entire graphics pipeline we are making. The idea is to make an OpenGL version and a cardinal version. The opengl will let us see that our outputs are correct, and then we can be sure that our code will produce the output we want(spinning cube with textures on all faces, lighting, rotating). This will allow us to ensure the compiler outputs are correct if we are certain that the code itself is not broken when those issues do arise. It also gives the compiler team an idea of what syntax and code they must be able to process. 

### Future Progress

I intend to present a function call assembly at the Sunday meeting. I also intend to verify the saxpy output and then extend it past 1024 elements. Verifying these two programs will demonstrate most of what I want. Because the asm for function call will demonstrate a graphics microapplication, it can also be used to test some special functional units.