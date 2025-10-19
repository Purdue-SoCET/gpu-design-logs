# Week 8
- State: Finished and not encountering any obstacle.
- About this: Summary of week 8

## Compiler Chat 10/11, Saturday
- Possibility of having 2 decimals in `sin` and `cos`
- `subi` and logical operations(`andi`, `xori`, etc.) can be discarded
  - `addi` always signed, seems like `subi` is no needed
  - Immidiate logical operations are not often used
  - I-Type has enough space right now, leave it as it is
- For `lui`(load upper imm)/`lmi`(load middle imm)/`lli`(load lower imm)
  - Directly assign the value in immidiate to the regiser
  - Do not AND '0 and OR imm the register for loading, will increase CPI
  - Do not clean the content(RISC-V clean the register when using `lui`)
- Only have `isqrt`(invert square root) in our ISA
  - To obtain `sqrt`(square root), do `isqrt` twice

## GPU Meeting 10/12, Sunday
Fall Break

## Compiler Meeting 10/13, Monday
Fall Break

## Abstract
- Completed on 10/16, Thursday
- Hard to evaluate performance of our compiler
  - Performance depends on hardwares
  - Try to compare compiler with optimization and without optimization
- Have Sooraj's feedback on 10/20, Monday

## Compiler thoughts
- Compiler is named `Twig` now
- Merge current branch we have to simplify the repository
- Minimize Twig, discard funtionalities in PPCI that won't be used
- Figure out how to let Twig work on command line with a custom command
- How GPU memory works
  - For load/store instructions
  - Should memory show like what 437 did

## Goal for Week 8
- Make a assembler for Hardware team
- Check details of packetization and predication
- Implement PPCI compiler -- Twig
- Figure out the possibility of smaller register file
  - NVIDIA papers, 4 register files
  - Lower the power consumption
