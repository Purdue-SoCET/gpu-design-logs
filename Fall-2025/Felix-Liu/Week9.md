Status: not stuck

Changes implemented:
- Fixed initial errors from path, imports, and confirmed reading of first instruction
- A lot more decoding logic, which can be ported to the functional simulator
- System-level warp/instruction evaluation working with initial sampleASM.s
  - R-type instructions are confirmed to actually perform an operation, as confirmed by the overflow check
NOTE: currently running and evaluating only a single thread at a time. Will need to figure out interfacing with CSR registers and predicate, though it shouldn't be too bad.

TODO: 
- functional unit of MRF and RFC. Maybe have one version run only with the MRF and another version count RFC accesses and the resulting power efficiency?
