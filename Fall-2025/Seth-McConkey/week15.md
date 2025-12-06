# Design Log Week 15

## Status

Not stuck or blocked.

## Cycle-Accurate Simulator Progress

- I started on the integration of EX stage and WB stage
- I was able to finish the code, but I need to create a testbench to verify functionality and check for syntax errors/bugs
- We decided on the Thursday meeting to pause integration work and move on to identifying unit tests needed to verify the Cycle-accurate simulator
- These must be present on the final report as well
- Some quick ideas for unit tests:
  - EX Stage:
    - For each FU/FSU:
      - Multiple instructions in pipeline
      - Stalling due to backpressure from WB stage
      - Overflow/underflow conditions
      - Div by zero, -inf/inf inputs to FP units
      - Operation tests for all supported instructions
      - Invalid instruction handling
      - NOP handling
  - WB Stage:
    - Writeback buffer full condition
    - Arbitration policy tests (round-robin, priority-based)
    - Multiple instructions writing to same bank
    - Multiple instructions writing to different banks
    - Correct data written back to register file
    - Invalid instruction handling
    - NOP handling
    - Some buffers full
    - All buffers full
- Next steps:
  - Finalize list of unit tests needed for each stage
  - Assign tests to each team member
  - Start writing final report (scary!!!)
