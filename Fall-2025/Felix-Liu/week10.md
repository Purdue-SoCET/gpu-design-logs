Status: not stuck

Changes implemented: 
- fixed halt logic
- added a new method to the Instr class: decode. This decodes the instruction and passes the operands into the instruction class itself.
- shared emulator stuff with the functional simulaor. Specifically, had the instr.decode method replace the vibe coded "DecodeStage". 
    - Need to talk to funcsim guys about how certain values/operands are passed. For example, is one of the values passed in for decode for B-type instructions.
- updated the Makefile to take in either a hex or binary meminit.hex file (since the assembler outputs binary). "make run" runs hex, "make run-bin" runs binary.
- testing of all three teams today!
  - The graphics team gave me Saxpy assembly code to run on the emulator. They pass it into the assembler, which then outputs a binary file for the emulator.
  - Our emulator spits out a memsim.hex (like 437), but there is no checking of the memdump just yet. 
