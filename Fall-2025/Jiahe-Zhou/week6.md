# Week 6
- State: Finished and not encountering any obstacle.
- About this: Summary of week 6

## GPU Meeting 9/28, Sunday

Communicate with Graphics, decide to make wave table like 362 to lookup sin/cos value

Design Review on next Sunday(10/5)

## Compiler Meeting 9/29, Monday
<img width="1382" height="510" alt="image" src="https://github.com/user-attachments/assets/3ad13f20-ca61-4884-8e85-750fe9283f81" />

### Summary
- imm6 on rs2
  - memory search: MEM + imm6 to get address of array
- imm12 on rs1, rs2
- 5 bits pred within 1 extra bit to invert the mask
- No float imm
  - use constant lookup table for float imm
- Don't do FMA
  - need 3 registers + 1 rd
  - take FMA will break current instruction structure
- Unconditional jump end up with loop
  - use predicate 
    - special instruction `jpnz`
  - run until all threads are done
    - if pred!=0    loop
    - else          pc + 4  // leave loop
- add instruction for int to float `i2f`
- stack for predicate on software(compiler)
```c
if (A) {            // 1
    if (B) {        // 2
        if (C) {    // 3
            /* 3 */
        }
        /* 2 */↵ pred 3 to pred 2
    }
    /* 1 */↵ pred 2 to pred 1
}

   /* pred 3 */
  /*  pred 2  */
 /*   pred 1   */
```

### Special Reserve Keywords
- software need
  - `addf`, `subf`, `mulf`, `divf`
  - `sin`, `cos`, `i2f`(int to float), `f2i`(float to int), `sqrt`
- load
  - `lmi`(load middle imm), `lli`(load lower imm)
- loop control
  - `jpnz`(jump pred not zero)

## PPCI Progress
### PPCI Kernel Call Frontend: gpuc
- lexer.py
  - `lex_c`: "<<<" and ">>>" to tokens
- parser.py
  - `parse_primary_expression`: if see "<<<", call parse_kernel_call()
  - `parse_kernel_call`: parse structure of kernel
    > type function_name(function_args) function_name<<<gpu_args>>>(function_args)
- semantics.py
  - `on_kernel_call`: Check kernel call for validity
- expression.py
  - `KernelCall`: kernel node definition for AST
  - `LaunchConfig`: packed structure for gpu configs

### PPCI Kernel Call Backend: gpuasm
- \_\_init\_\_.py
  - register "gpuasm" as "GPUASMArch"
- arch.py: `class GPUASMArch`
  - define GPUASMArch with ISA, assembler, asm_printer, registers
  - set types for i8/u8/i16/u16/i32/u32/f32/f64/ptr and C aliases int, long, ptr
  - define calling convention arg0 in r12, arg1 in r13 and return value in r10
- registers.py: `class Gpr`
  - define registers R0-R3, R10, R12, R13
- instructions.py: `class GPUInstruction`, `class Add`, `class Mov`
  - define basic instructions `add` and `mov`
- asm_printer.py
  - reuse riscv `class RiscvAsmPrinter` to print asm(to be modified)

## Goal for Week 6
- Complete presentation for design review and improve based on feedback
- Try to add more instructions to PPCI
