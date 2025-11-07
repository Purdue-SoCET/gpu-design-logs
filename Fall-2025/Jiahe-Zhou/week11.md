# Week 11
- State: Finished and not encountering any obstacle.
- About this: Summary of week 11

## GPU Meeting 11/02, Sunday
- Add predication to Twig
- Code Review on 11/16
  - Finish our compiler before the date
- Research Expo Poster Presentation on 11/18, 1:30-2:30pm
- Update Teal Card: `slli` was duplicated
- Fix not implemented error in arch/registers.py: def from_num(cls, num)
- Find the call path of command `ppci-cc -m riscv -S file`
  - ppci\cli\compile_base.py: do_compile
  - ppci\api.py: ir_to_stream
  - ppci\codegen\codegen.py: generate
- `-S` for assembly
- `-c` for linker
- `--ir` for ir file

## Compiler Meeting 11/03, Monday
- Try to finish adding predication before code review
- Packets feature becomes optional
  - No affect to current architecture right now
  - Consider as an doable optimization in the future
- Twig cannot be evaluated, main outcome will be complete the Twig
  - Hard to test performance of Twig
- predication for if-else statement has completed
  - switch-case has not yet finished
- csr definition
  - c1: threadId
  - c2: blockId
  - c3: blockDim

## Compiler thoughts
- Will C implicit type conversion break the compiler
- Check how to rewrite/pack our own command
  - make command shorter and more clear
- Do we need to make a simulator for hardware

## Goal for Week 11
- Minimize and merge Twig
  - Merge predication, arch, and frontend
- Define folder path structure
