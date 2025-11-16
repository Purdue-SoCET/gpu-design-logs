Progress:

I am not stuck with anything right now.

GPU subteam: Graphics

## Overview

This week is lacking due to having had 2 exams.

I wrote a function call assembly file that gives each warp a 1 megabyte stack, pushes a value onto it, pops it, and stores into memory. If the testcase works, we can see every thread ID at addresses starting at 0xB...

We did some work to create the poster for the poster presentation on 11/18. There is also the code review, which pushed up the timeline for making the C files work. Aiden successfully got the graphics pipeline to run on a CPU. When I get the function call and saxpy to work on the CPU, the compiler should then be ready to accept our kernels and produce binaries for the simulator to run. We can take the first spinning cube and get the 2nd spinning cube on sim.

We now aim to review these programs with the whole team so we can share our vision.

## Future Plan

### Other Kernels

I want to write a matrix mult kernel. This is a very common kernel in CUDA, and is good for saturating hardware. In this case, we can compare it with other processors pretty easily since both CPUs and the AI Hardware can execute this type of work. It is also good to have a nongraphical test case which is standalone. We can easily look at the values of the matrix to see if it works properly. MMult is a highly parallel task as well, which makes it a good GPU candidate. Having asked GPT, there are a few more common kernels I can take a look at, but this is the main one.

### Graphics

Additionally, I want to improve the graphics scene. My ideas right now are to implement lighting and/or environment mapping. These both add a lot to the fidelity of a graphics scene. We can investigate programming a raytracing algorithm for the GPU based on CS334's CPU raytracer. These can also implement reflections which are great for more complex scenes. I also want to look into replacing the cube with a teapot(or having both) as a teapot is a classical object in computer graphics. We should also collect the textures we are using and make sure those look decent. We can implement different filtering algorithms and see the results.

Ultimately, these functions can be generalized to produce a sort of library for a CPU to call on like OpenGL. This does not seem particularly worth doing as a very long term goal is LLVM for a compiler, which would directly support programming in OpenCL instead. We think it may be okay to just write kernels specific to our tasks and call them as needed.

### Simulator interaction

It may be helpful if I debug the simulator. With two different kernels, I should be able to see the correct output the CPU files would produce. The saxpy ran on sim would only place a value every 8 bytes and not every 4, which is an issue. Since I am the most aware of what my own code does, I think I can familarize myself with the sim and see what it is doing versus what I think it should be doing. This will let me really know if the sim is wrong or if there is an error in my code.