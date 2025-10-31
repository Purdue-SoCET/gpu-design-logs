State: I am not stuck with anything

# Progress

## Work Completed:
* Finalized stack handling between hardware and compilers
* Divided up tasks
* Developed the Per Vertex Triangle Shader

## Progress:

### Stack Handling
* Finalized decision on stack with hardware and compilers
* Will have a **Per Warp** stack pointer, created by the software (compiler side)
* To give software exposure to the warp side, the software side can assume that the threadIDs will be allocated linearly with warps
  * Meaning 0-31 is warp0, 34-63 is warp1, and so on
* Finally, each threads warp pointer will have a built-in offset for the stack pointer
  * This means thread0's r2=sp, thread0's r2=sp+4, and so on
  * This will reduce the instructions needed before and after each function call
* When thinking about handling the stack pointer, and it not updating for any threads no active, I had concern
  * Shouldn't be an issue, as non-active threads won't ever use their left-behind stack pointer
  * By the time those threads are reconverged, i.e. "turned on," all threads will have set their stack pointer backwards

### Task Division
* Graphics team divided up tasks again this week, now without a need for a heavy focus on a OpenGL style kernel
  * Write C Kernel's -> Aid[ea]n
    * Aiden (Me) -> Triangle Kernel, Vertex Kernel
    * Aidan (Not Me) -> Vertex Kernel, connecting CPU Sim into OpenGL()
  * Develop graphics Assembly for hardware -> Tushar, Erhao

### Triangle Kernel
* Created an initial wip Triangle Kernel for the graphics workload
* Current Design Choices:
  * The kernel is ran once for each triangle
  * Ensures there is no race condition when modifying the depth buffer
  * Will force large under-utilization for workloads with many smaller triangles (common) but not for us
    * Will still look at optimizing it better going forward, using modern methods
  * Was able to pull out the large complex calculation of a per triangle matric used for finding barycentric coordinates
    * Only uses the projected vertexes, and is the same for each pixel of a triangle, hence not parralizable for our current system
