# Design Log Week 6

## Status: 

I am not currently stuck or blocked.

## Work Completed

### Design Review
- [slides](https://docs.google.com/presentation/d/1M33G-WqNQMKs6h0JDbxaD1RH-Oab2VH1/edit?slide=id.p1#slide=id.p1)
- Graphics Library:
  - Features (openGL-like)
  - Pseudo Code for graphics program

### Resources
- https://erkaman.github.io/posts/fast_triangle_rasterization.html
- https://jonathan2251.github.io/lbd/gpu.html#graphics-and-opencl-compilation

### GPU Compute Framework
- **OpenCL vs OpenGL**
  - CL-> computing language
    - General Parallel Compute, not just graphics
    - Versions before 2.1 are C not C++
  - GL -> graphics library
    -  Specific for graphics
    -  Library with function calls for graphics workflow
   
- **SPIR-V**
  - intermediate language for parallel compute
  - uses LLVM
<img width="803" height="283" alt="image" src="https://github.com/user-attachments/assets/ee84c6dd-5499-4741-96e4-2e443d00181d" />

from [The Concept of GPU Compiler](https://jonathan2251.github.io/lbd/gpu.html#graphics-and-opencl-compilation)

- **Custom C-like language**
  -  similar to openCL or CUDA but custom to our build
  -  Current plan as wouldn't require LLVM
 
### Triangle Stage
- Pixel data written by triangle, this means computing all pixels in one triangle then moving to next triangle
- Allows for greater parallelism

### Clipping/Culling
- Can be done on CPU side then just send already processed triangles to GPU
- Backface culling:
  - done on GPU instead
  - remove all triangles that are facing away from camera (norm is away from camera)

 ### OpenCL
 - [Tutorial](https://cgmb-rocm-docs.readthedocs.io/en/latest/Programming_Guides/Opencl-programming-guide.html#example)
 - SAXPY Kernel:

```%%writefile my_kernel.cl
__kernel void saxpy(const int n, const float a, __global const float* x, __global float* y){
  int i = get_global_id(0);

  if(i < n) {
    y[i] = a * x[i] + y[i];
  }
}
```

- Flow:
  1. Pick a platform -> clGetPlatformIDs
  2. Pick device -> clGetDeviceIDs
  3. Create context and queue -> clCreateContext and clCreateCommandQueue
  4. Send program and kernel -> clCreateProgramWithSource, clBuildProgram, clCreateKernel
  5. Setting up data -> clCreateBuffer
  6. Setting Kernel arguments -> clSetKernelArg
  7. Enqueue and Readback -> clEnqueueNDRangeKernel and clEnqueueReadBuffer
     
