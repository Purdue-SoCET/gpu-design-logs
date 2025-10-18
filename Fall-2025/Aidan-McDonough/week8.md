# Design Log Week 8

## Status: 

I am not currently stuck or blocked.

## Work Completed

[Abstract](https://purdue0-my.sharepoint.com/:w:/g/personal/sexton34_purdue_edu/EWirqAIumVRGuM6MN0Rkb54By3XcpBgnUiK_Khsu3ZhpQg?e=PdOnmx) was submitted

**OpenGL: Graphics Shaders vs Compute Shaders**
- Graphics Shader
  - Fixed Graphics Pipeline Stages
  - Implicit thread indexing: GPU automatically runs your code once per vertex or once per pixel
    
- Compute Shader
  - General Purpose and Custom Pipeline
  - Explicit thread indexing: Choose work size
    - glDispatchCompute(x,y,z) = launches compute work groups
    - gl_GlobalInvocationID = blockIdx.* * blockDim.* + threadIdx.* (provided in openGL, computed in cuda)
    - gl_WorkGroupID = blockIdx.x/y/z
    - gl_LocalInvocationID = threadIdx.x/y/z
    
```
layout(local_size_x = 256) in; // 256 threads per workgroup

layout(std430, binding = 0) buffer XBuf { float x[]; };  // SSBO 0 -> SSBO = Shader Storage Buffer Object

layout(std430, binding = 1) buffer YBuf { float y[]; };  // SSBO 1

uniform float a;
uniform int   N;

void main() {
    uint i = gl_GlobalInvocationID.x; // blockIdx*blockDim+threadIdx
    if (i < uint(N)) {
        y[i] = a * x[i] + y[i];
    }
}
```

**Custom Vertex Shader**
- Similar to OpenGl graphics shaders
- Fixed stages of pipeline with possibly implicit thread indexing

**Future Plans**
- First build graphics functions/program for CPU, then for functsim, and lastly for RTL. 
  - CPU Kernel will be C code to be compiled by c compiler to run on a CPU.
  - CPU Kernel can be looped 1024 times to represent running a thread (sequential instead of parallel)
- After, we will modify the kernel C code to run on GPU team compiler for functsim and RTL
  - Will require making the kernel not valid for c compiler
  - Adding keywords to kernel
  - This will require us to work within team to decide what these keywords will be and how they will be used
  - This will also require working with compilers team to understand what each keyword should do
- Benchmark for GPU
