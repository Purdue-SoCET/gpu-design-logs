Summary:

This week was focused on catchign up for the design/code review that happened this past Sunday. i
- I undertook making unit tests for the icache, fetch, branch fu, decode, and memory stage units. I developed a bunch of core test cases per unit, and then went ahead and attempted a successful integration test for the fetch which just combined daniel's scheduler and my icache interface.
- I sythesized all of the tests into clean debug outputs onto the terminal, as well as merged my work upstream to the main branch: https://github.com/Purdue-SoCET/gpu/tree/main/gpu_sim/cyclesim/drafts
- Throughout this processes, I ensured to work around the base class provided by Zach Barna, and made modifications in my personal test cases as needed. Implementation wise either, I didn;t need to change much about the RTL. 
- Thus far, I didn't identify a need to modify the logic of the base classes. They worked wonderfully well. I modified the instruction base class to have more fields as needed, but they are pretty flexible, so I don't think that posed significant issues.
- On another note, I updated the conference posted with my material. It went great.

Meetings Summary:
- SUNDAY: Design Review for my unit. I admit, it was painfully short (given 5/6 minutes only) and I wished I had more time to go over the connection of the memory setup (inspired from how emulator has done it).
- TUESDAY: Frontend Research Conference Posted Presentation
- No toehr meetings this week due to labs, and another exam. These are painful times.

Evidence of Work: 
- Meeting presentation: https://docs.google.com/presentation/d/1Vi72xo6eATTp0-FOh_ir8uTIHRGMNLfZLLHTyImkm74/edit?usp=sharing
- Research Conference Poster: https://purdue0-my.sharepoint.com/:p:/g/personal/ee_purdue_edu/EWOFayCiJB5NskunwBJd_a0B5nyZWuc_sXyo6mbYh0eodg?e=uf8lyI
- FuncSim test structure:
- <img width="1111" height="859" alt="sd_review_2 flow diagram drawio" src="https://github.com/user-attachments/assets/464a6d2d-2000-4d02-99aa-06f9036725fb" />


