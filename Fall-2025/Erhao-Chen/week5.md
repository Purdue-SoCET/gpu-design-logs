# Week 5
statement: I am not stuck.
## Progress
### Diagram Flow
<img width="1266" height="291" alt="tbdr" src="https://github.com/user-attachments/assets/1f7ec4a6-f6c6-4564-8764-d94fbd8c7942" />

- Overall
  - This is the diagram that was shared by hardware team. 
  - We reviewed the GPU graphics flow as shown in figure. For now, we don't care alpha test and alpha blend since our demo does not require transparency.

### Work Flow
- Input Data Structure
  - Vector List (3D coordinates) -> all vertex positions (e.g. point [0,0,0], [0,1,2], [0,1,3])
  - Triangle List -> indices into vector list, three vertex will form a triangle(e.g.[0,1,2], [1,2,3]...)
  - Pixel List
  - Vector List (2D) -> positions after projection based on camera.

- Stages
  - Step 1: Load 3D vertex + triangle data into memory.
  - Step 2 (Vector Kernel): Rotate and project vertices -> 2D points.
  - Step 3 (Triangle Kernel): Perform clipping and culling -> output 2D triangles.
  - Step 4 (Pixel Kernel): For each pixel, find covering triangles and write to pixel buffer.

- Functional Units  
  - int32 (add, mul, div)
  - fp32 (add, mul, div)
  - ld/st (int32, fp32, memory fence?)
  - trig func (sin, cos)
  - graphics specific (shader core?, z/stencil buffers? rasterizer?)
  - T$?
  - special (sqrt, 3x3 matrix?, Control/Status Registers? hardware performance counters?)

### Further Question
When in our flow should textures be applied/sampled?
