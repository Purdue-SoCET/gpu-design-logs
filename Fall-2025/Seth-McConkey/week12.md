# Design Log Week 12

## Status

Not stuck or blocked.

## Emulator Progress

- I have been working with the graphics and compiler teams to figure out what is going wrong with the SAXBY test case
  - We have figured out that we are handling threadblocks incorrectly in the emulator
  - This is mostly due to the change in how CSRs are handled in HW now
    - Instead of using multiple dimensions for defining thread IDs, we are now using a linear local thread ID from 0-1023, and then the threadblock ID is used to figure out which threadblock the thread belongs to and to also define the global thread ID
    - Dan was originally in charge of implementing CSRs, so he is in charge of updating the emulator to handle this new format

## Cycle-Accurate Simulator Progress

- I have been caught up in the emulator work this week, so I haven't made much progress on the cycle-accurate simulator
- I am still writing the boilerplate for the EX stage architecture
- Once that is done, I can start implementing specific functional units and functional sub-units
 
