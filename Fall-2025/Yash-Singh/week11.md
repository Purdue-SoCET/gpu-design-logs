STATUS: Everything is GOOD and I don't need any external help. The teams doing well.

SUMMARY: This week was focused on working with the refactored version of the func simulator. I found that my method using 'tick' might be too confusing, especially for more timing based stuff. Instead of hoping to advance the timing globally in the SM, the team pivoted to an 
implementation that used more robust handshake signals of 'wait' and 'ready'. Zach primarily worked on this refactoring, and the changes were reintegrated for our individual units by this Thursdays meeting. I tested versions of the decode that also simulates writes and updates to the predicate register file.

EVIDENCE OF WORK: see my changes in the following branch: https://github.com/Purdue-SoCET/gpu/tree/yash_bs/gpu_sim, which used the changes made by Zach in this branch https://github.com/Purdue-SoCET/gpu/tree/zach_latch_forwarding_IFs/gpu_sim.

MEETINGS:
- 02_11_25 Sunday General Meeting: focused on discussing the new implementation and abstraction of how we will test. Instead of focusing on large abstractions of the stages and trying to make hyper-sp[ecific subclasses, we flattened out the hierarchy to the
    pipeline stages and logic. This way, we need only three main classes: stage, latch interface, and forwarding interface.
- 06_11_25 Hardware Meeting: We discussed our prpgress with the func sim and furteh talked about the register file implementations in the software emulation. Metrics wise, things are also working. Waiting on testing to conclude for the individual units.
- General meeting: presentation about multicore testing for the SoCET microprocessor. Super cool!

AGENDA FOR NEXT WEEK:
- I am quite busy so I won't be able to dedicate much time to SOCET until after my 463 and 437 exams on Thursday. It is likely that I will skip the Sunday meeting, and definetily next weeks Thursday meeting.
