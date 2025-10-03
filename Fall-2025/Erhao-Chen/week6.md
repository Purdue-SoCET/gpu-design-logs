# Week 6
statement: I am not stuck.
## Progress
- Meeting on Sunday: discuss how to implement texture.
- Meeting on Thursday: prepare for presentation.
### Decisions
- Textures are sampled in pixel stage
- implement a basic z-buffer for visibility 
- drive precompiled kernels on the GPU simulator.
- for execution, a script will load kernels and scene buffers into the Python hardware simulator to run.
### Implementation
- load scene data -> per-vertex transfrom and projection -> cull/clip -> pixel stage with texturing and depth -> write bakc to framebuffer
- The camera stays fixed, the cube rotates each frame
- <img width="400" height="793" alt="1 2025-10-02 230610" src="https://github.com/user-attachments/assets/f97f1bc1-91b5-4299-9838-16aaa902393c" />

