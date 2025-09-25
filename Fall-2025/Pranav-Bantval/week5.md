# Week 3

State: I am not stuck with anything, don't need help right now. 

Progress: Made procedures to add a custom instruction function call via PPCI (more details below). Need to meet with rest of compilers team to draft an ISA.

Next week: Come to Sunday's meeting with rough draft for ISA. Try to run by it with software/hw

## dev environment
- added ppci to github last week
- clone that one
- pip uninstall ppci (if you already installed it)
- pip install -e ./ppci
- This will allow you to use the ppci you are modifying locally to run python scripts

To go from C to RISCV:
```ppci cc -S -O0 -o [outputfile].s -m riscv [filename].c```

To go from C to IR
```ppci cc --ir -o [outputfile].ir -m riscv [filename].c```

## custom instruction procedure
1. Decided on instruction encoding/format in C/RISC: int cos(int rs1, int rs2)
   
   a. RTYPE: opcode = 0000001, funct7 = 1110000, funct3 = 000
   
   b. RISCV: `customcos` rd, rs1, rs2
   
2. Add instruction `int cos (int, int)` in C to IR compiler
3. Define new classes inheriting from `RiscvInstruction` with custom encoding in ``ppci/arch/riscv/instructions.py``
4. Register `customcos` to the base ISA. Modify `gen_call` Method: Added checks for specific function names to emit custom instructions instead of standard calls.
6. Add an ISA pattern that matches the call to `cos` and emits `customcos`
7. Verify using commands to compile C to IR and C to RISCV

## procedure 2
- this procedure is for in-built instructions e.g. add not function calls
- it is a work in progress.
