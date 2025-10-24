# Week 9
statement: I am not stuck.

## Defined CPU Sim
- Aiden showed implemtation of CPU sim frame work.
- The idea is that we can use the #ifdef to differentiate between our simulation environment, which decideds on C simulator or GPU.
- It simulates multiple executing using run_kernel function which uses for loops to iterate every single thread. 
- It allows to write and test our GPU kernels on the CPU before compiler or hardware functional simulator done.

## Testbench Work flow
<img width="300" height="300" alt="20251023_235644851_iOS" src="https://github.com/user-attachments/assets/87bde2c8-0730-4040-a55a-33fb558b7d22" />

## Overall plan in general   
- create MMIO:
  - CPU mem->0x0000_0000 ->0xffff_ffff
  - Gpu mem-> 0x1000_0000 -> 0x9fff_ffff
- Create basic tests for emulator in asm
- plan library
- create standard kernel
- cpu sim
- Test code for gpu on cpu before function sim

## Todo List for team
We break down the tasks into following part, I will work on for defining library specification. 
- Hardware unit test
- Cpu kernels
- Define library specification




  
