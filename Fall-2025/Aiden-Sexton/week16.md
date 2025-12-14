State: I am not stuck with anything

# Progress

## Work Completed:
* Got status updates on compiler and emulator
* Wrote intoduction for graphics workflow in report
* Got appendicitus

## Progress

### Compiler status
* Before the current week, did not handle predicates at all, relying on purely placeholders for all predicates
* Got updated with initial predicate allocator
  * currently untested as far as I am aware
* Still does not handle linking
  * Means that while the base file can in theory be used, manual edits must be made to remove symbol headers
  * Means in theory, C code could be turned unto assembly with medium effort
* Currently not joined with the original assembler
  * Compiler output must be modified before putting into the old assembler

### Emulator Status
* Current emulator has a few limitations done to speed up development
* Only handles a single predicate mask, so any conditionals more complex then a single branch
* Current CSR is only one single register which has a linear thread ID between 0-1023
  * Does not handle the actual multiple thread blocks or the argument pointer
* Both of the above issues, as well as other possible issue to be investigated will need to be fixed next semester
  * Possibly taken over by a graphics person?
* Due to the status of the emulator, and the compiler, the "Emulator Main" goal from software must be put on hold

### Intial Report Notes
* Wrote some basic introduction on the graphics workflow for the report (possibly removed for final version)
* Continued work was cut short by health emergency (see below)
* List of problems the graphics team was trying to solve:
  * The in-development cardinal gpGPU needs custom tests to be developed to ensure both **correctness** and **performance** are met
    * limited by the custom ISA, meaning existing tests cannot be used
  * The Twig Compiler limits what forms of programs can be ran, and as such custom programs suited for Twig must be developed
  * The cardinal lacks graphics specific hardware, and as such, those normally fixed hardware pipelines must be replicated in SW

### Appendicitis
* Yeah so this happened this week. Not much to say