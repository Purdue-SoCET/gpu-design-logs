SUMMARY: This week was primarily focused on refactoring the testing branch to make the functional simulator work. A majority of the work was focused on refactoring the current structure of the functional simulator.
WHAT I NEED THIS WEEK: probably more time, but we'll see how it goes.
MEETINGS THIS WEEK:
- [26/10/2025] Sunday Main Meeting was focused on discussing the current setup of the func sim so far. I'd gotten further feedback on things that could be done, and decided to set the deadline for next Sundays meeting.
- [30/11/2025] Thursday main meeting was focused on refactoring our current structure. We decided we need to replace the the cycle based structure to a simple valid-ready based structure. See meeting notes below:
  - MEETING NOTES:
  -     Always valid ready for every interface
  -     Subclass of latches for every interface
  -     Class for every instruction with PC, warp id/gorup id, fields of inputs, current location in the pipeline, clock cycle per stage, etc.
  -     Simplify stage interfaces
  -     Probably need some kind of universal buffer class
  -     Everyone has to handle backpressure individually.
