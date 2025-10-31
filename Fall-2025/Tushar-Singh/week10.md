Progress:

I am not stuck with anything right now.

GPU subteam: Graphics

## Overview

This week, the main team meeting discussed how we would be programming the GPU. Based off of CUDA, when we want to program, it should be abstracted into blocks with dimensions and IDS, as well as a thread index. We want to do this in the asm. That is my task now with Erhau, and we will make asm files to use as complex tests for the simulators and future verilog with no reliance on a compiler.

For now, I have a psuedocode 
```
csrr x3, csr1 #fictional block id
csrr x4, csr2 #fictional blockDim
csrr x5, csr3 #fictional thread ID
```
The issue is that the csr's haven't actually been defined. It is perfectly ok to have more/less csr's to represent this info, but it needs to be well defined. I haven't discussed with the hardware team how their simulator works from an I/O perspective. What I have discussed is how the assembler will generate code and what I can do to manually stitch together my data section with the assembled binary.

### Kernels

The first kernel being written is a simple saxpy. This routine is only a few instructions but being able to run it will require solving all the problems of going from code with data to simulator outputs. It is also easy to test because of its simple nature. It revealed uncertainties with csr information, and how the simulator would grab data from the binary. This kernel has already been written. With some more work to produce an acceptable binary file, it can be ran on the GPU as soon as Sunday if we agree on the aformentioned CSRs. 

Next, we will write a simple kernel corresponding to a standard graphics routine. It is likely this will be the 3D->2D projection of points. Because this is a real workload in asm, it will have a very meaningful output and demonstrate functionality with more complexity than the simple saxpy program. It is likely we will have a more complex control flow that may reveal issues to debug, either in the simulator or more likely with the cycle accurate variant. 

A recursive program will be helpful. This will demonstrate the correct pushing of registers to memory, and the ability to properly operate with predicate masks. The code should never realistically be recursive, but whatever desired behavior we decide on for running out of space in memory for stacks should be tested. An inefficient infinite fibonacchi sequence will make a good testcase for this purpose.

Beyond this, we will likely focus on C files for the CPU. We want to produce the correct outputs of our asm kernels so that we can compare the output of the simulator. If we have extra time in the semester, we can continue to add more features and ideally implement all of textures, environment mapping, shadow maps, and lighting. This would produce a fairly high quality graphics scene that will continue to look good even with complex objects and operations. 

### Coherency

After some critical thinking, this graphics team has decided we will probably want coherent memory. Our current idea of a triangle kernel, see week 7, can only saturate one kernel. If we tile the plane, we can use all the warps available properly. This does make an issue clear. GPU Programming without memory coherency across the threadblock level is difficult and slow. We just got lucky that the graphics scene is naively parallel and therefore an ideal case for a GPU to execute. If we want alpha support(transparency) then coherency is required. 

The next question is what a good method to do this is. 437 uses a LR SC method for data locks. In the parallel programming scheme, I believe that a memory barrier will be helpful. What I am envisioning is an instruction that all warps in play(within the current threadblock) must reach before any threads are allowed to continue. These can be used when memory is expected to collide, such as writing to framebuffers in a more efficient triangle kernel. The exact implementation should be discussed but we will benefit heavily from being able to program in this manner. This will also enable running multiple different kernels across 2+ threadblocks, as it will be possible to write kernels that can be coherent to each other using these types of instructions. We expect this will be lots of work for Cecilie, but I believe in her.

This goes contrary to what I wrote in week 9, but that was in the context of adding no extra hardware complexity. I believe that since this project will continue to be extended in the future including extra SM's, it makes sense to do as much as possible to prepare existing hardware and avoid a rewrite. We want to make these decisions now before we have to write rtl that would be costly to have to redo.

### Plan and Schedule

By Sunday, the saxpy kernel should be completely ready for the simulator, with the exception of csr management, which I cannot do until I message the hardware team. There will be no evidence of this until I decide it is in a "correct" state and worth pushing.

Within the week after that, we want to write the rest of the kernels we are planning, since there are not very many, and then focus on the production of our C kernels that will actually construct the graphics scene. Each of these asm and C kernels will be paired with a CPU file that emulates the output and can be used as a golden model.