Progress:

I am not stuck with anything right now.

GPU subteam: Graphics

## Design Review Presentation

### Results and Feedback

This week included the design review presentation, which was given to the other subteam members and the GTAs. Jing primarily had questions. He was questioning our idea of the triangle level kernel. We had believed that tiling, clipping, and culling, were all going to make for difficult optimizations.

#### Triangle kernel

The issue we find is with writing. When one does culling, triangles that are partially on the edge of the camera are cut up into the portion on screen and off screen. This in turn generates new triangles, which must be added to the existing list of triangles for the mesh being worked on. This is the issue. If each thread is handling one different triangle at a time, there will be a severe deadlock trying to writeback multiple new triangles, presumably all in similar locations at the end of the lists containing the mesh specifications. We had decided that it would be best to do this type of culling on a CPU.

Possible ideas to resolve this issue at the time were either to write a complex data structure, or to try a system based on tiling, where the screen space is partitioned, to avoid these issues. Tiling has the issue that some triangles can be in multiple tiles, which would effectively result in the same issue. The immediate decision was to defer for a later meeting.

One Idea is to parallelize the processing of each triangle rather than attempt to process many triangles at once. When processing just one triangle at a time, it can be fairly fast to figure out which pixels map to the triangle and what depth should be stored. Iterating through the triangles like this may be fairly efficient with good optimzations. 

For culling, GPU culling methods can be different than CPU culling. Back face culling looks at the normal of the triangle. If it faces away from the camera, don't render it. This has no consequences for closed shapes, but may be wrong for open shapes. Notably, it can be processed for all triangles at once. This and other culling methods can write to a bitmask, one per triangle, which should be a good data structure for parallel operations.

## Hardware Discussions

### Scope

When deciding what to support and what not to support, the main discussion has been in texture cache. We have ultimately decided not to have one. It ultimately only accelerates workloads like aliasing, but these can still be done even if only standard Dcache exists. Adding a texture cache would likely be a large amount of work, for a hardware team that already has lots of RTL to design. A plan is to test it in python sim to see if it makes a massive improvement. 

The programming model has been vaguely decided on. There will be one SM, and this SM will support the context of multiple threadblocks. Though only one SM exists, meaning that one threadblock could be ran at a time, supporting multiple will aid future designs. The programming model is effectively not changed, since we may program with a block ID of 1.

Less is understood about kernel launching. It is still vague as to how the GPU begins a kernel, where it grabs informaton from, and who is launching it. The AXI bus has not been specified yet and is likely critical to this. Much more research remains to be done here.

### Operations

As far as custom hardware goes, sin/cos were already decided on. This week, we have decided to replace sqrt with isqrt. Inverse square root, such as the quake algorithm, are massively useful in computing vector normals. A standard square root can be avoided with intelligent code, so it is not particularly important, and can be inversed from isqrt if needed.

## Programming Language Decisions

### Open Compute Language

Notably an entirely different language. Would have a good opportunity to support a wider array of code potentially. Comes at the downside of being based on LLVM. Though I definitely did the most research on this, I am writing the least. Can be considered as a project for a team of 10-20 people on compilers with the course taken.

### Open Graphics Library

This is what we are basing our library off of. OGL is just a library of C functions. This is inherently easier to reuse a standard C compiler compared to LLVM, which would require an understanding of a compiler. We will build our own functions to mimic OpenGL style programming with the goal of being able to program the GPU easily. 


## Future Plan

We need to meet with the compilers team and have a discussion. Keywords need to be decided on. How are they expecting files to be delivered? Is there any actual agreement about hardware between all the teams yet? A python sim repo was made, but I do not think we are ready for the C program quite yet. When we have a proper agreement on how the code will be structured, we can very quickly write GPU shaders that can attempt to adequately test the hardware.

We must build a 3D scene in OpenGL. We can use binaries from this for the GPU's custom scene. Things like the textures and Triangle mesh can be reused. It is important to see the final product before we build it for the Cardinal GPU.