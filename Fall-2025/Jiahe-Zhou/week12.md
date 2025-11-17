# Week 12
- State: Finished and not encountering any obstacle.
- About this: Summary of week 12

## GPU Meeting 11/09, Sunday
- Merge predication and arch etc.
- Test on PJMP, SJMP, BJMP
- Try to remove CJMP
  - More comprehensive branch conversion
  - CJMP is a JMP type from C language
  - Indicate that some JMP types are not supported by our arch
  - if-else, while, do-while, for loop share different CJMP types

## Compiler Meeting 11/10, Monday
- BJMP is completed
- Try to finish SJMP and PJMP
- Keep removing CJMP dependency
- CSRs needed to manage
  - threadId, blockId, blockDim, currentDim
- Leave packetization to next semester
  - Packetization is a optional optimization
  - Nest can run correctly without packetization

## Compiler Progress
- Create new branch `merge`
  - Merge current work on Preprocessor, AST, IR, and twig
- Create command `twig`
  - Add ppci\cli\twig.py
    - Define customized command `twig`
    - Reuse command `ppci-cc -m twig` and pack
  - Update pyproject.toml
    - twig = "ppci.cli.twig:twig" for python to recognize the command
- Function calls without using `extern`
  - Add ppci\c\builtins.py
    - Builtin functions like `sin`, `cos`, `isqrt`
    - Define function name, parameter list, and return type
    - Helper function `builtin_fty()` for create `FunctionType` Node
  - Update ppci\arch\twig\arch.py
    - Import corresponding instructions: Cos, Sin, Isqrt, ItoF, FtoI
    - Create BUILTIN_TABLE for mapping [function:instruction]
    - Use easier logic in `gen_call()` for possible extension in the future
  - TODO: itof and ftoi shouldn't be the functions visible to users
- Assembler cannot merge into PPCI right now
  - Current predication is generate in IR
  - Need nodes for predication added manually in assembly
  - Require more steps on this, or assembly must always add predications manually

## Goal for Week 12
- Code Review
- Finish and print Poster
- Prepare for Final Presentation
- Review and fix bugs in code
